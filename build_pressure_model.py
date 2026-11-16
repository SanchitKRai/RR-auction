import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

DATA_DIR = r"C:\Users\lenovo\Downloads\rr\Data Pack"
OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"

print("1. Loading datasets...")
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"))
teams = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))
ctpm = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))

print(f"Loaded {len(matches)} matches, {len(bbb)} balls.")

# Merge match metadata
match_meta = matches.merge(comps[['comp_id', 'match_format', 'season']], on='comp_id', how='left')
bbb = bbb.merge(match_meta[['match_id', 'comp_id', 'match_format', 'season', 'stage', 'knock_out', 
                             'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'win_team_id']], 
                on='match_id', how='left')

bbb = bbb.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

# Determine legal ball
bbb['is_illegal'] = bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['is_legal'] = ~bbb['is_illegal']
bbb['is_batter_ball'] = ~bbb['extras_type'].isin(['wide']) # Batter faces all balls except wides

# Team runs on this ball
bbb['team_ball_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']

# Bowler conceded runs & wickets
bbb['bowler_runs_conceded'] = bbb['runs']
bbb.loc[bbb['extras_type'].isin(['wide', 'Overstep', 'other']), 'bowler_runs_conceded'] += bbb['extras1_runs']
non_bowler_dismissals = ['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field']
bbb['is_bowler_wicket'] = bbb['is_wicket'] & (~bbb['dismissal_type'].isin(non_bowler_dismissals))

# Cumulative metrics before delivery
bbb['cum_runs_before'] = bbb.groupby(['match_id', 'innings'])['team_ball_runs'].cumsum() - bbb['team_ball_runs']
bbb['cum_wickets_before'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket'].astype(int)
bbb['legal_balls_before'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal'].astype(int)

# Scheduled balls in innings
bbb['scheduled_balls_inn'] = 120
bbb.loc[(bbb['innings'] == 1) & bbb['first_inn_revised_overs'].notna(), 'scheduled_balls_inn'] = bbb['first_inn_revised_overs']
bbb.loc[(bbb['innings'] == 2) & bbb['second_inn_revised_overs'].notna(), 'scheduled_balls_inn'] = bbb['second_inn_revised_overs']

bbb['balls_remaining'] = np.maximum(0, bbb['scheduled_balls_inn'] - bbb['legal_balls_before'])
bbb['wickets_in_hand'] = np.maximum(0, 10 - bbb['cum_wickets_before'])

# Innings 1 total score
inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['team_ball_runs'].sum().rename('inn1_total')
bbb = bbb.merge(inn1_totals, on='match_id', how='left')

bbb['target'] = np.where(bbb['revised_target'].notna(), bbb['revised_target'], bbb['inn1_total'] + 1)
bbb['runs_required'] = np.where(bbb['innings'] == 2, np.maximum(0, bbb['target'] - bbb['cum_runs_before']), np.nan)

bbb['rrr'] = np.where(
    (bbb['innings'] == 2) & (bbb['balls_remaining'] > 0),
    (bbb['runs_required'] / bbb['balls_remaining']) * 6.0,
    np.nan
)
bbb['crr'] = np.where(bbb['legal_balls_before'] > 0, (bbb['cum_runs_before'] / bbb['legal_balls_before']) * 6.0, 0.0)

print("2. Training Win Probability Model for Innings 2...")
inn2_mask = (bbb['innings'] == 2) & (bbb['balls_remaining'] > 0) & (bbb['wickets_in_hand'] > 0) & (bbb['runs_required'] > 0) & bbb['win_team_id'].notna()
train_df = bbb[inn2_mask].copy()
train_df['chase_won'] = (train_df['batting_team_id'] == train_df['win_team_id']).astype(int)
train_df['required_per_wicket'] = train_df['runs_required'] / train_df['wickets_in_hand']

features = ['runs_required', 'balls_remaining', 'wickets_in_hand', 'rrr', 'required_per_wicket']
wp_model = LogisticRegression(max_iter=1000)
wp_model.fit(train_df[features], train_df['chase_won'])
print(f"Win Probability Model AUC: {roc_auc_score(train_df['chase_won'], wp_model.predict_proba(train_df[features])[:, 1]):.4f}")

# Calculate Win Probability on Innings 2
bbb['wp_before'] = np.nan
bbb.loc[inn2_mask, 'wp_before'] = wp_model.predict_proba(train_df[features])[:, 1]
# If chase already won: wp = 1.0; if all out: wp = 0.0
bbb.loc[(bbb['innings'] == 2) & (bbb['runs_required'] <= 0), 'wp_before'] = 1.0
bbb.loc[(bbb['innings'] == 2) & (bbb['wickets_in_hand'] <= 0), 'wp_before'] = 0.0

# Calculate Leverage Index (LI) for Innings 2
# LI = difference in WP between a boundary (4 runs, 1 ball) and a wicket (0 runs, 1 wicket, 1 ball)
sim_bound = train_df.copy()
sim_bound['runs_required'] = np.maximum(0, sim_bound['runs_required'] - 4)
sim_bound['balls_remaining'] = np.maximum(0, sim_bound['balls_remaining'] - 1)
sim_bound['rrr'] = np.where(sim_bound['balls_remaining'] > 0, (sim_bound['runs_required'] / sim_bound['balls_remaining']) * 6.0, 36.0)
sim_bound['required_per_wicket'] = sim_bound['runs_required'] / sim_bound['wickets_in_hand']
wp_bound = wp_model.predict_proba(sim_bound[features])[:, 1]

sim_wkt = train_df.copy()
sim_wkt['balls_remaining'] = np.maximum(0, sim_wkt['balls_remaining'] - 1)
sim_wkt['wickets_in_hand'] = np.maximum(1, sim_wkt['wickets_in_hand'] - 1)
sim_wkt['rrr'] = np.where(sim_wkt['balls_remaining'] > 0, (sim_wkt['runs_required'] / sim_wkt['balls_remaining']) * 6.0, 36.0)
sim_wkt['required_per_wicket'] = sim_wkt['runs_required'] / sim_wkt['wickets_in_hand']
wp_wkt = wp_model.predict_proba(sim_wkt[features])[:, 1]

swing = np.abs(wp_bound - wp_wkt)
mean_swing = np.mean(swing)
leverage_idx = swing / mean_swing

bbb['leverage_index'] = np.nan
bbb.loc[inn2_mask, 'leverage_index'] = leverage_idx

# Calculate WP After delivery to compute WPA
bbb['cum_runs_after'] = bbb['cum_runs_before'] + bbb['team_ball_runs']
bbb['cum_wickets_after'] = bbb['cum_wickets_before'] + bbb['is_wicket'].astype(int)
bbb['legal_balls_after'] = bbb['legal_balls_before'] + bbb['is_legal'].astype(int)
bbb['balls_rem_after'] = np.maximum(0, bbb['scheduled_balls_inn'] - bbb['legal_balls_after'])
bbb['wickets_hand_after'] = np.maximum(0, 10 - bbb['cum_wickets_after'])
bbb['runs_req_after'] = np.maximum(0, bbb['target'] - bbb['cum_runs_after'])

# Predict WP after
after_eval_mask = (bbb['innings'] == 2) & (bbb['balls_rem_after'] > 0) & (bbb['wickets_hand_after'] > 0) & (bbb['runs_req_after'] > 0)
eval_after = bbb[after_eval_mask].copy()
eval_after['rrr'] = (eval_after['runs_req_after'] / eval_after['balls_rem_after']) * 6.0
eval_after['required_per_wicket'] = eval_after['runs_req_after'] / eval_after['wickets_hand_after']
features_after = eval_after[['runs_req_after', 'balls_rem_after', 'wickets_hand_after', 'rrr', 'required_per_wicket']].rename(
    columns={'runs_req_after': 'runs_required', 'balls_rem_after': 'balls_remaining', 'wickets_hand_after': 'wickets_in_hand'}
)

bbb['wp_after'] = np.nan
bbb.loc[after_eval_mask, 'wp_after'] = wp_model.predict_proba(features_after[features])[:, 1]
bbb.loc[(bbb['innings'] == 2) & (bbb['runs_req_after'] <= 0), 'wp_after'] = 1.0
bbb.loc[(bbb['innings'] == 2) & (bbb['wickets_hand_after'] <= 0), 'wp_after'] = 0.0

bbb['wpa_bat'] = bbb['wp_after'] - bbb['wp_before']
bbb['wpa_bowl'] = -bbb['wpa_bat']

print("3. Constructing Composite Pressure Index (PI)...")
# Initialize Pressure Index
bbb['pressure_score'] = 2.0 # Baseline low pressure

# Super overs = 10.0
bbb.loc[bbb['innings'].isin([3, 4]), 'pressure_score'] = 10.0

# INNINGS 1 PRESSURE CALCULATION:
inn1_idx = bbb[bbb['innings'] == 1].index

# 1. Death overs in Innings 1 (overs 16-20): Base pressure 5.5 to 7.5
death_inn1 = (bbb['innings'] == 1) & (bbb['overid'] >= 16)
bbb.loc[death_inn1, 'pressure_score'] = 5.5 + (bbb.loc[death_inn1, 'overid'] - 16) * 0.5

# 2. Collapse / Crisis in Innings 1:
# - Early crisis: >= 2 wickets lost in overs 1-3
crisis_early = (bbb['innings'] == 1) & (bbb['overid'] <= 3) & (bbb['cum_wickets_before'] >= 2)
bbb.loc[crisis_early, 'pressure_score'] = np.maximum(bbb.loc[crisis_early, 'pressure_score'], 6.5)

# - Powerplay collapse: >= 3 wickets lost in overs 1-6
crisis_pp = (bbb['innings'] == 1) & (bbb['overid'] <= 6) & (bbb['cum_wickets_before'] >= 3)
bbb.loc[crisis_pp, 'pressure_score'] = np.maximum(bbb.loc[crisis_pp, 'pressure_score'], 7.0)

# - Mid-innings collapse: >= 4 wickets lost before over 12
crisis_mid = (bbb['innings'] == 1) & (bbb['overid'] <= 12) & (bbb['cum_wickets_before'] >= 4)
bbb.loc[crisis_mid, 'pressure_score'] = np.maximum(bbb.loc[crisis_mid, 'pressure_score'], 6.8)

# - Tail pressure: >= 6 wickets lost
crisis_tail = (bbb['innings'] == 1) & (bbb['cum_wickets_before'] >= 6)
bbb.loc[crisis_tail, 'pressure_score'] = np.maximum(bbb.loc[crisis_tail, 'pressure_score'], 6.5)


# INNINGS 2 PRESSURE CALCULATION:
# Pressure in chase combines:
# - Leverage Index (scaled 0-5)
# - RRR Stress (scaled 0-4)
# - Proximity/Death urgency (balls <= 30)
# - Wickets in hand stress
inn2_idx = bbb[bbb['innings'] == 2].index

li = bbb.loc[inn2_idx, 'leverage_index'].fillna(1.0)
rrr = bbb.loc[inn2_idx, 'rrr'].fillna(8.0)
balls_rem = bbb.loc[inn2_idx, 'balls_remaining'].fillna(60)
wkts_hand = bbb.loc[inn2_idx, 'wickets_in_hand'].fillna(6)

# Continuous formula for chase pressure
chase_pi = (
    2.0 + 
    np.clip(li * 2.2, 0, 4.5) + # Leverage contribution (0 to 4.5)
    np.clip((rrr - 7.5) * 0.6, 0, 3.0) + # RRR stress (0 to 3.0)
    np.where(balls_rem <= 30, (30 - balls_rem) / 30.0 * 1.5, 0.0) + # Death urgency (0 to 1.5)
    np.where(wkts_hand <= 4, (4 - wkts_hand) * 0.4, 0.0) # Resource depletion (0 to 1.6)
)

# Also account for chase collapse (early wickets in powerplay)
chase_collapse = (bbb.loc[inn2_idx, 'overid'] <= 6) & (bbb.loc[inn2_idx, 'cum_wickets_before'] >= 3)
chase_pi = np.where(chase_collapse, np.maximum(chase_pi, 7.0), chase_pi)

bbb.loc[inn2_idx, 'pressure_score'] = np.clip(chase_pi, 1.0, 10.0)

# TOURNAMENT STAKES MULTIPLIER:
# Knockout games (Finals, Qualifiers, Eliminators, Semi-Finals)
knockout_mask = (bbb['knock_out'] == 1) | (bbb['stage'].isin(['Final', 'Qualifier', 'Eliminator', 'Semi Final', 'Super 4']))
bbb.loc[knockout_mask, 'pressure_score'] = np.clip(bbb.loc[knockout_mask, 'pressure_score'] * 1.20, 1.0, 10.0)

# Assign Pressure Categories
# HIGH: >= 6.0 (Crucial pressure delivery)
# MED: 3.5 to 6.0
# LOW: < 3.5
bbb['pressure_tier'] = pd.cut(
    bbb['pressure_score'], 
    bins=[-0.1, 3.5, 6.0, 10.1], 
    labels=['LOW', 'MED', 'HIGH']
)

print("\nPressure Tier Breakdown:")
print(bbb['pressure_tier'].value_counts(normalize=True) * 100)
print(bbb['pressure_tier'].value_counts())

print("\nMean Pressure Score by Phase (Innings 1 vs 2):")
bbb['phase'] = pd.cut(bbb['overid'], bins=[0, 6, 15, 20], labels=['Powerplay', 'Middle', 'Death'])
print(bbb.groupby(['innings', 'phase'])['pressure_score'].mean())

# Save enhanced ball_by_ball metadata to feather or parquet or csv for rapid reuse
print("\nSaving processed dataset summary...")
bbb[['match_id', 'innings', 'overid', 'striker_id', 'striker_name', 'bowler_id', 'bowler_name', 
     'runs', 'is_batter_ball', 'is_legal', 'is_wicket', 'is_bowler_wicket', 'bowler_runs_conceded',
     'wpa_bat', 'wpa_bowl', 'pressure_score', 'pressure_tier', 'comp_id', 'match_format', 'season']].to_csv(
    os.path.join(OUT_DIR, "processed_deliveries_summary.csv"), index=False
)
print("Done saving summary.")
