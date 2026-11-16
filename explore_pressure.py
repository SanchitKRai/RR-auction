import pandas as pd
import numpy as np
import os

DATA_DIR = r"C:\Users\lenovo\Downloads\rr\Data Pack"

print("Loading data...")
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"))

print(f"Loaded {len(matches)} matches, {len(bbb)} balls.")

# Merge match metadata
match_meta = matches.merge(comps[['comp_id', 'match_format', 'season']], on='comp_id', how='left')
bbb = bbb.merge(match_meta[['match_id', 'comp_id', 'match_format', 'season', 'stage', 'knock_out', 
                             'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'win_team_id']], 
                on='match_id', how='left')

# Sort chronologically by match, innings, overid, over_ball_num
bbb = bbb.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

# Determine legal delivery: not wide, not overstep, not other (waist high no-ball)
bbb['is_illegal'] = bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['is_legal'] = ~bbb['is_illegal']

# Team runs on this ball
bbb['team_ball_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']

# Bowler conceded runs: runs off bat + wide + overstep/other extras
# Note: byes and legbyes and penalty are not conceded by bowler
bbb['bowler_runs_conceded'] = bbb['runs']
bbb.loc[bbb['extras_type'].isin(['wide', 'Overstep', 'other']), 'bowler_runs_conceded'] += bbb['extras1_runs']

# Bowler wicket: is_wicket True and not non-bowler dismissal
non_bowler_dismissals = ['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field']
bbb['is_bowler_wicket'] = bbb['is_wicket'] & (~bbb['dismissal_type'].isin(non_bowler_dismissals))

# Calculate cumulative runs, wickets, legal balls BEFORE each ball in the innings
bbb['cum_runs_before'] = bbb.groupby(['match_id', 'innings'])['team_ball_runs'].cumsum() - bbb['team_ball_runs']
bbb['cum_wickets_before'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket'].astype(int)
bbb['legal_balls_before'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal'].astype(int)

# Scheduled balls in innings
# For inn 1: default 120, or first_inn_revised_overs
bbb['scheduled_balls_inn'] = 120
mask_rev_inn1 = (bbb['innings'] == 1) & bbb['first_inn_revised_overs'].notna()
bbb.loc[mask_rev_inn1, 'scheduled_balls_inn'] = bbb.loc[mask_rev_inn1, 'first_inn_revised_overs']

mask_rev_inn2 = (bbb['innings'] == 2) & bbb['second_inn_revised_overs'].notna()
bbb.loc[mask_rev_inn2, 'scheduled_balls_inn'] = bbb.loc[mask_rev_inn2, 'second_inn_revised_overs']

bbb['balls_remaining'] = np.maximum(0, bbb['scheduled_balls_inn'] - bbb['legal_balls_before'])
bbb['wickets_in_hand'] = np.maximum(0, 10 - bbb['cum_wickets_before'])

# Innings 1 total score for target calculation
inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['team_ball_runs'].sum().rename('inn1_total')
bbb = bbb.merge(inn1_totals, on='match_id', how='left')

# Target for Innings 2: revised_target if notna, else inn1_total + 1
bbb['target'] = np.where(bbb['revised_target'].notna(), bbb['revised_target'], bbb['inn1_total'] + 1)
bbb['runs_required'] = np.where(bbb['innings'] == 2, np.maximum(0, bbb['target'] - bbb['cum_runs_before']), np.nan)

# Required Run Rate
bbb['rrr'] = np.where(
    (bbb['innings'] == 2) & (bbb['balls_remaining'] > 0),
    (bbb['runs_required'] / bbb['balls_remaining']) * 6.0,
    np.nan
)

# Current Run Rate
bbb['crr'] = np.where(
    bbb['legal_balls_before'] > 0,
    (bbb['cum_runs_before'] / bbb['legal_balls_before']) * 6.0,
    0.0
)

print("Computed match states.")
print(bbb[['match_id', 'innings', 'overid', 'cum_runs_before', 'cum_wickets_before', 'balls_remaining', 'runs_required', 'rrr']].head(10))
