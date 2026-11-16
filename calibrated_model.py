import pandas as pd
import numpy as np
import os

OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"

# Load the processed delivery summary
df = pd.read_csv(os.path.join(OUT_DIR, "processed_deliveries_summary.csv"), low_memory=False)

# Define competition quality tier
def get_comp_tier(row):
    comp_name = str(row['comp_name'])
    m_format = str(row['match_format'])
    if 'IPL' in comp_name:
        return 'TIER_1_IPL', 1.0
    elif 'Emerging' in comp_name or 'Rising Stars' in comp_name or 'Japan' in comp_name:
        return 'TIER_3_DEVELOPING', 0.75
    else:
        return 'TIER_2_T20I', 0.90

comps = pd.read_csv(os.path.join(r"C:\Users\lenovo\Downloads\rr\Data Pack", "competitions.csv"))
df = df.merge(comps[['comp_id', 'comp_name']], on='comp_id', how='left')
tiers = df.apply(get_comp_tier, axis=1)
df['comp_tier'] = [t[0] for t in tiers]
df['quality_weight'] = [t[1] for t in tiers]

# Define Phase
df['phase'] = 'Middle'
df.loc[df['overid'] <= 6, 'phase'] = 'Powerplay'
df.loc[df['overid'] >= 16, 'phase'] = 'Death'

# Compute baseline stats per comp_tier and phase under HIGH pressure
comp_phase_bat = df[(df['pressure_tier'] == 'HIGH') & df['is_batter_ball']].groupby(['comp_tier', 'phase']).agg(
    bench_sr=('runs', lambda x: x.sum() / len(x) * 100.0)
).reset_index()

comp_phase_bowl = df[(df['pressure_tier'] == 'HIGH') & df['is_legal']].groupby(['comp_tier', 'phase']).agg(
    bench_econ=('bowler_runs_conceded', lambda x: x.sum() / (len(x)/6.0))
).reset_index()

print("Benchmark High Pressure SR by Comp Tier & Phase:")
print(comp_phase_bat)
print("\nBenchmark High Pressure Economy by Comp Tier & Phase:")
print(comp_phase_bowl)

# Check Pakistani players to identify IPL eligibility
pak_teams = ['Pakistan', 'Pakistan A']
ctpm = pd.read_csv(os.path.join(r"C:\Users\lenovo\Downloads\rr\Data Pack", "competition_team_player_mapping.csv"))
pak_player_ids = ctpm[ctpm['team_name'].isin(pak_teams)]['player_id'].unique()
# Also players who only played for Pakistan
df['is_pak_player'] = df['striker_id'].isin(pak_player_ids) | df['bowler_id'].isin(pak_player_ids)

# Let's run Calibrated Batting Model
hp_bat = df[(df['pressure_tier'] == 'HIGH') & df['is_batter_ball']].copy()
base_bat = df[(df['pressure_tier'].isin(['LOW', 'MED'])) & df['is_batter_ball']].copy()

bat_hp = hp_bat.groupby(['striker_id', 'striker_name']).agg(
    hp_balls=('runs', 'count'),
    hp_runs=('runs', 'sum'),
    hp_fours=('runs', lambda x: (x == 4).sum()),
    hp_sixes=('runs', lambda x: (x == 6).sum()),
    hp_dots=('runs', lambda x: (x == 0).sum()),
    hp_dismissals=('is_wicket', 'sum'),
    hp_wpa=('wpa_bat', 'sum'),
    hp_matches=('match_id', 'nunique'),
    ipl_balls=('comp_tier', lambda x: (x == 'TIER_1_IPL').sum()),
    weighted_balls=('quality_weight', 'sum')
).reset_index()

bat_hp['hp_sr'] = (bat_hp['hp_runs'] / bat_hp['hp_balls']) * 100.0
bat_hp['hp_avg'] = bat_hp['hp_runs'] / np.maximum(1, bat_hp['hp_dismissals'])
bat_hp['hp_dot_pct'] = (bat_hp['hp_dots'] / bat_hp['hp_balls']) * 100.0
bat_hp['hp_bound_pct'] = ((bat_hp['hp_fours'] + bat_hp['hp_sixes']) / bat_hp['hp_balls']) * 100.0
bat_hp['hp_wpa_per_100'] = (bat_hp['hp_wpa'] / bat_hp['hp_balls']) * 100.0

bat_base = base_bat.groupby('striker_id').agg(
    base_balls=('runs', 'count'),
    base_runs=('runs', 'sum'),
    base_dismissals=('is_wicket', 'sum'),
    base_dots=('runs', lambda x: (x == 0).sum())
).reset_index()
bat_base['base_sr'] = (bat_base['base_runs'] / np.maximum(1, bat_base['base_balls'])) * 100.0
bat_base['base_avg'] = bat_base['base_runs'] / np.maximum(1, bat_base['base_dismissals'])
bat_base['base_dot_pct'] = (bat_base['base_dots'] / np.maximum(1, bat_base['base_balls'])) * 100.0

bat_m = bat_hp.merge(bat_base, on='striker_id', how='left').fillna(0)
bat_m['total_balls'] = bat_m['hp_balls'] + bat_m['base_balls']
bat_m['delta_sr'] = bat_m['hp_sr'] - bat_m['base_sr']
bat_m['delta_avg'] = bat_m['hp_avg'] - bat_m['base_avg']
bat_m['delta_dot_pct'] = bat_m['base_dot_pct'] - bat_m['hp_dot_pct']

# Filter qualification: minimum 140 HP balls and 250 total balls
bat_qual = bat_m[(bat_m['hp_balls'] >= 140) & (bat_m['total_balls'] >= 250)].copy()

# Bayesian Shrinkage
pop_sr = bat_qual['hp_runs'].sum() / bat_qual['hp_balls'].sum() * 100.0
pop_avg = bat_qual['hp_runs'].sum() / bat_qual['hp_dismissals'].sum()
bat_qual['hp_sr_bayes'] = (bat_qual['hp_balls'] * bat_qual['hp_sr'] + 60.0 * pop_sr) / (bat_qual['hp_balls'] + 60.0)
bat_qual['hp_avg_bayes'] = (bat_qual['hp_dismissals'] * bat_qual['hp_avg'] + 6.0 * pop_avg) / (bat_qual['hp_dismissals'] + 6.0)

# Quality index
bat_qual['quality_factor'] = bat_qual['weighted_balls'] / bat_qual['hp_balls']

# Normalize
def norm(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-9)

bat_qual['norm_sr'] = norm(bat_qual['hp_sr_bayes'])
bat_qual['norm_avg'] = norm(bat_qual['hp_avg_bayes'])
bat_qual['norm_dot'] = norm(100.0 - bat_qual['hp_dot_pct'])
bat_qual['norm_bound'] = norm(bat_qual['hp_bound_pct'])
bat_qual['norm_wpa'] = norm(bat_qual['hp_wpa_per_100'])
bat_qual['norm_delta'] = norm(bat_qual['delta_sr'])

bat_qual['bat_prs_score'] = (
    0.28 * bat_qual['norm_sr'] + 
    0.22 * bat_qual['norm_avg'] + 
    0.15 * bat_qual['norm_dot'] + 
    0.15 * bat_qual['norm_bound'] + 
    0.10 * bat_qual['norm_wpa'] + 
    0.10 * bat_qual['norm_delta']
) * 100.0 * bat_qual['quality_factor']

bat_ranked = bat_qual.sort_values(by='bat_prs_score', ascending=False).reset_index(drop=True)
print("\n=== TOP 15 BATTERS (CALIBRATED) ===")
cols_b = ['striker_name', 'hp_balls', 'hp_runs', 'hp_sr', 'hp_avg', 'delta_sr', 'hp_dot_pct', 'hp_bound_pct', 'hp_wpa', 'bat_prs_score']
print(bat_ranked[cols_b].head(15).to_string(index=True))


# ==============================================================================
# CALIBRATED BOWLING MODEL
# ==============================================================================
hp_bowl = df[(df['pressure_tier'] == 'HIGH') & df['is_legal']].copy()
base_bowl = df[(df['pressure_tier'].isin(['LOW', 'MED'])) & df['is_legal']].copy()

bowl_hp = hp_bowl.groupby(['bowler_id', 'bowler_name']).agg(
    hp_balls=('runs', 'count'),
    hp_runs=('bowler_runs_conceded', 'sum'),
    hp_wkts=('is_bowler_wicket', 'sum'),
    hp_dots=('bowler_runs_conceded', lambda x: (x == 0).sum()),
    hp_boundaries=('runs', lambda x: (x.isin([4, 6])).sum()),
    hp_wpa=('wpa_bowl', 'sum'),
    hp_matches=('match_id', 'nunique'),
    ipl_balls=('comp_tier', lambda x: (x == 'TIER_1_IPL').sum()),
    weighted_balls=('quality_weight', 'sum')
).reset_index()

bowl_hp['hp_overs'] = bowl_hp['hp_balls'] / 6.0
bowl_hp['hp_econ'] = bowl_hp['hp_runs'] / bowl_hp['hp_overs']
bowl_hp['hp_sr'] = bowl_hp['hp_balls'] / np.maximum(1, bowl_hp['hp_wkts'])
bowl_hp['hp_avg'] = bowl_hp['hp_runs'] / np.maximum(1, bowl_hp['hp_wkts'])
bowl_hp['hp_dot_pct'] = (bowl_hp['hp_dots'] / bowl_hp['hp_balls']) * 100.0
bowl_hp['hp_bound_pct'] = (bowl_hp['hp_boundaries'] / bowl_hp['hp_balls']) * 100.0
bowl_hp['hp_wpa_per_100'] = (bowl_hp['hp_wpa'] / bowl_hp['hp_balls']) * 100.0

bowl_base = base_bowl.groupby('bowler_id').agg(
    base_balls=('runs', 'count'),
    base_runs=('bowler_runs_conceded', 'sum'),
    base_wkts=('is_bowler_wicket', 'sum'),
    base_dots=('bowler_runs_conceded', lambda x: (x == 0).sum()),
    base_boundaries=('runs', lambda x: (x.isin([4, 6])).sum())
).reset_index()
bowl_base['base_overs'] = bowl_base['base_balls'] / 6.0
bowl_base['base_econ'] = bowl_base['base_runs'] / np.maximum(0.1, bowl_base['base_overs'])
bowl_base['base_sr'] = bowl_base['base_balls'] / np.maximum(1, bowl_base['base_wkts'])
bowl_base['base_dot_pct'] = (bowl_base['base_dots'] / np.maximum(1, bowl_base['base_balls'])) * 100.0
bowl_base['base_bound_pct'] = (bowl_base['base_boundaries'] / np.maximum(1, bowl_base['base_balls'])) * 100.0

bowl_m = bowl_hp.merge(bowl_base, on='bowler_id', how='left').fillna(0)
bowl_m['total_balls'] = bowl_m['hp_balls'] + bowl_m['base_balls']
bowl_m['delta_econ'] = bowl_m['base_econ'] - bowl_m['hp_econ']
bowl_m['delta_dot_pct'] = bowl_m['hp_dot_pct'] - bowl_m['base_dot_pct']

# Filter qualification: minimum 140 HP balls and 250 total balls
bowl_qual = bowl_m[(bowl_m['hp_balls'] >= 140) & (bowl_m['total_balls'] >= 250)].copy()

# Bayesian Shrinkage
pop_econ = bowl_qual['hp_runs'].sum() / (bowl_qual['hp_balls'].sum() / 6.0)
pop_bowl_sr = bowl_qual['hp_balls'].sum() / bowl_qual['hp_wkts'].sum()
bowl_qual['hp_econ_bayes'] = (bowl_qual['hp_balls'] * bowl_qual['hp_econ'] + 70.0 * pop_econ) / (bowl_qual['hp_balls'] + 70.0)
bowl_qual['hp_sr_bayes'] = (bowl_qual['hp_wkts'] * bowl_qual['hp_sr'] + 7.0 * pop_bowl_sr) / (bowl_qual['hp_wkts'] + 7.0)

bowl_qual['quality_factor'] = bowl_qual['weighted_balls'] / bowl_qual['hp_balls']

bowl_qual['norm_econ'] = norm(bowl_qual['hp_econ_bayes'].max() - bowl_qual['hp_econ_bayes'])
bowl_qual['norm_sr'] = norm(bowl_qual['hp_sr_bayes'].max() - bowl_qual['hp_sr_bayes'])
bowl_qual['norm_dot'] = norm(bowl_qual['hp_dot_pct'])
bowl_qual['norm_bound'] = norm(bowl_qual['hp_bound_pct'].max() - bowl_qual['hp_bound_pct'])
bowl_qual['norm_wpa'] = norm(bowl_qual['hp_wpa_per_100'])
bowl_qual['norm_delta_econ'] = norm(bowl_qual['delta_econ'])

bowl_qual['bowl_prs_score'] = (
    0.28 * bowl_qual['norm_econ'] + 
    0.27 * bowl_qual['norm_sr'] + 
    0.15 * bowl_qual['norm_dot'] + 
    0.15 * bowl_qual['norm_bound'] + 
    0.10 * bowl_qual['norm_wpa'] + 
    0.05 * bowl_qual['norm_delta_econ']
) * 100.0 * bowl_qual['quality_factor']

# Check IPL eligibility
bowl_qual['is_auction_eligible'] = ~bowl_qual['bowler_id'].isin(pak_player_ids)
bat_qual['is_auction_eligible'] = ~bat_qual['striker_id'].isin(pak_player_ids)

bowl_ranked = bowl_qual.sort_values(by='bowl_prs_score', ascending=False).reset_index(drop=True)
print("\n=== TOP 15 BOWLERS (CALIBRATED - ALL) ===")
cols_bw = ['bowler_name', 'hp_balls', 'hp_overs', 'hp_wkts', 'hp_econ', 'hp_sr', 'delta_econ', 'hp_dot_pct', 'hp_bound_pct', 'hp_wpa', 'is_auction_eligible', 'bowl_prs_score']
print(bowl_ranked[cols_bw].head(15).to_string(index=True))

print("\n=== TOP 15 BOWLERS (AUCTION ELIGIBLE) ===")
print(bowl_ranked[bowl_ranked['is_auction_eligible']][cols_bw].head(15).to_string(index=True))
