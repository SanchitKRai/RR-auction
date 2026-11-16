import pandas as pd
import numpy as np
import os

OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"

# Load the processed delivery summary
df = pd.read_csv(os.path.join(OUT_DIR, "processed_deliveries_summary.csv"), low_memory=False)

# Competitions / weights
# IPL matches: 1.0 weight, T20I matches: 0.92 weight
df['comp_weight'] = np.where(df['match_format'] == 'T20', 1.0, 0.92)

print("Loaded processed deliveries:", len(df))

# ==============================================================================
# BATTING ANALYSIS
# ==============================================================================
print("\n--- Computing Batting Performance Under Pressure vs Baseline ---")

# High Pressure deliveries (batter balls: non-wides)
hp_bat = df[(df['pressure_tier'] == 'HIGH') & df['is_batter_ball']].copy()
base_bat = df[(df['pressure_tier'].isin(['LOW', 'MED'])) & df['is_batter_ball']].copy()
all_bat = df[df['is_batter_ball']].copy()

def aggregate_batting(data, prefix=''):
    agg = data.groupby(['striker_id', 'striker_name']).agg(
        balls=('runs', 'count'),
        runs=('runs', 'sum'),
        fours=('runs', lambda x: (x == 4).sum()),
        sixes=('runs', lambda x: (x == 6).sum()),
        dots=('runs', lambda x: (x == 0).sum()),
        dismissals=('is_wicket', 'sum'),
        wpa=('wpa_bat', 'sum'),
        matches=('match_id', 'nunique')
    ).reset_index()
    
    agg[f'{prefix}balls'] = agg['balls']
    agg[f'{prefix}runs'] = agg['runs']
    agg[f'{prefix}sr'] = (agg['runs'] / np.maximum(1, agg['balls'])) * 100.0
    agg[f'{prefix}avg'] = agg['runs'] / np.maximum(1, agg['dismissals'])
    agg[f'{prefix}dot_pct'] = (agg['dots'] / np.maximum(1, agg['balls'])) * 100.0
    agg[f'{prefix}bound_pct'] = ((agg['fours'] + agg['sixes']) / np.maximum(1, agg['balls'])) * 100.0
    agg[f'{prefix}wpa'] = agg['wpa']
    agg[f'{prefix}wpa_per_100'] = (agg['wpa'] / np.maximum(1, agg['balls'])) * 100.0
    agg[f'{prefix}dismissals'] = agg['dismissals']
    agg[f'{prefix}matches'] = agg['matches']
    
    cols = ['striker_id', 'striker_name', f'{prefix}balls', f'{prefix}runs', f'{prefix}sr', 
            f'{prefix}avg', f'{prefix}dot_pct', f'{prefix}bound_pct', f'{prefix}wpa', 
            f'{prefix}wpa_per_100', f'{prefix}dismissals', f'{prefix}matches']
    return agg[cols]

bat_hp = aggregate_batting(hp_bat, prefix='hp_')
bat_base = aggregate_batting(base_bat, prefix='base_')
bat_all = aggregate_batting(all_bat, prefix='all_')

bat_merged = bat_hp.merge(bat_base, on=['striker_id', 'striker_name'], how='left')
bat_merged = bat_merged.merge(bat_all, on=['striker_id', 'striker_name'], how='left')

# Fill NaNs for players who didn't face balls in base
for col in bat_merged.columns:
    if 'base_' in col or 'all_' in col:
        bat_merged[col] = bat_merged[col].fillna(0)

# Filter qualification: minimum 120 balls faced under HIGH pressure, and minimum 250 total balls
bat_qual = bat_merged[(bat_merged['hp_balls'] >= 120) & (bat_merged['all_balls'] >= 250)].copy()

# Bayesian Shrinkage on HP Strike Rate and HP Average
prior_sr = bat_qual['hp_runs'].sum() / bat_qual['hp_balls'].sum() * 100.0
prior_avg = bat_qual['hp_runs'].sum() / bat_qual['hp_dismissals'].sum()
k_bat_sr = 50.0 # Shrinkage parameter for strike rate
k_bat_avg = 5.0 # Shrinkage parameter for average (in dismissals)

bat_qual['hp_sr_bayes'] = ((bat_qual['hp_balls'] / (bat_qual['hp_balls'] + k_bat_sr)) * bat_qual['hp_sr'] + 
                           (k_bat_sr / (bat_qual['hp_balls'] + k_bat_sr)) * prior_sr)
bat_qual['hp_avg_bayes'] = ((bat_qual['hp_dismissals'] / (bat_qual['hp_dismissals'] + k_bat_avg)) * bat_qual['hp_avg'] + 
                            (k_bat_avg / (bat_qual['hp_dismissals'] + k_bat_avg)) * prior_avg)

# Clutch Deltas
bat_qual['delta_sr'] = bat_qual['hp_sr'] - bat_qual['base_sr']
bat_qual['delta_avg'] = bat_qual['hp_avg'] - bat_qual['base_avg']
bat_qual['delta_dot_pct'] = bat_qual['base_dot_pct'] - bat_qual['hp_dot_pct'] # positive is good

# Match-by-match consistency under pressure
# In matches with HP balls, fraction of matches with positive impact (WPA > 0 or SR > par)
hp_match_bat = hp_bat.groupby(['striker_id', 'match_id']).agg(
    m_runs=('runs', 'sum'),
    m_balls=('runs', 'count'),
    m_wpa=('wpa_bat', 'sum')
).reset_index()
hp_match_bat['pos_impact'] = (hp_match_bat['m_wpa'] > 0.0) | ((hp_match_bat['m_runs'] / hp_match_bat['m_balls'] * 100.0) >= 150.0)
bat_consistency = hp_match_bat.groupby('striker_id')['pos_impact'].mean().rename('hp_consistency_rate').reset_index()

bat_qual = bat_qual.merge(bat_consistency, on='striker_id', how='left')

# Composite Batting Pressure Reliability Score (B-PRS, 0-100)
# Normalize components to z-scores or percentile ranks
def min_max_norm(series):
    return (series - series.min()) / (series.max() - series.min())

bat_qual['norm_sr'] = min_max_norm(bat_qual['hp_sr_bayes'])
bat_qual['norm_avg'] = min_max_norm(bat_qual['hp_avg_bayes'])
bat_qual['norm_dot'] = min_max_norm(100.0 - bat_qual['hp_dot_pct']) # lower dot is better
bat_qual['norm_bound'] = min_max_norm(bat_qual['hp_bound_pct'])
bat_qual['norm_wpa'] = min_max_norm(bat_qual['hp_wpa_per_100'])
bat_qual['norm_delta'] = min_max_norm(bat_qual['delta_sr'])
bat_qual['norm_cons'] = min_max_norm(bat_qual['hp_consistency_rate'])

bat_qual['batting_prs'] = (
    0.25 * bat_qual['norm_sr'] + 
    0.20 * bat_qual['norm_avg'] + 
    0.15 * bat_qual['norm_dot'] + 
    0.15 * bat_qual['norm_bound'] + 
    0.10 * bat_qual['norm_wpa'] + 
    0.08 * bat_qual['norm_delta'] +
    0.07 * bat_qual['norm_cons']
) * 100.0

top_batters = bat_qual.sort_values(by='batting_prs', ascending=False).reset_index(drop=True)
print("\n=== TOP 20 BATTERS UNDER PRESSURE ===")
display_cols_bat = ['striker_name', 'hp_balls', 'hp_runs', 'hp_sr', 'hp_avg', 'base_sr', 'delta_sr', 'hp_dot_pct', 'hp_bound_pct', 'hp_wpa', 'batting_prs']
print(top_batters[display_cols_bat].head(20).to_string(index=True))


# ==============================================================================
# BOWLING ANALYSIS
# ==============================================================================
print("\n--- Computing Bowling Performance Under Pressure vs Baseline ---")

hp_bowl = df[(df['pressure_tier'] == 'HIGH') & df['is_legal']].copy()
base_bowl = df[(df['pressure_tier'].isin(['LOW', 'MED'])) & df['is_legal']].copy()
all_bowl = df[df['is_legal']].copy()

def aggregate_bowling(data, prefix=''):
    agg = data.groupby(['bowler_id', 'bowler_name']).agg(
        legal_balls=('runs', 'count'),
        runs_conceded=('bowler_runs_conceded', 'sum'),
        wickets=('is_bowler_wicket', 'sum'),
        dots=('bowler_runs_conceded', lambda x: (x == 0).sum()),
        boundaries=('runs', lambda x: (x.isin([4, 6])).sum()),
        wpa=('wpa_bowl', 'sum'),
        matches=('match_id', 'nunique')
    ).reset_index()
    
    agg[f'{prefix}balls'] = agg['legal_balls']
    agg[f'{prefix}overs'] = agg['legal_balls'] / 6.0
    agg[f'{prefix}runs'] = agg['runs_conceded']
    agg[f'{prefix}wkts'] = agg['wickets']
    agg[f'{prefix}econ'] = agg['runs_conceded'] / np.maximum(0.1, agg[f'{prefix}overs'])
    agg[f'{prefix}sr'] = agg['legal_balls'] / np.maximum(1, agg['wickets'])
    agg[f'{prefix}avg'] = agg['runs_conceded'] / np.maximum(1, agg['wickets'])
    agg[f'{prefix}dot_pct'] = (agg['dots'] / np.maximum(1, agg['legal_balls'])) * 100.0
    agg[f'{prefix}bound_pct'] = (agg['boundaries'] / np.maximum(1, agg['legal_balls'])) * 100.0
    agg[f'{prefix}wpa'] = agg['wpa']
    agg[f'{prefix}wpa_per_100'] = (agg['wpa'] / np.maximum(1, agg['legal_balls'])) * 100.0
    agg[f'{prefix}matches'] = agg['matches']
    
    cols = ['bowler_id', 'bowler_name', f'{prefix}balls', f'{prefix}overs', f'{prefix}runs', 
            f'{prefix}wkts', f'{prefix}econ', f'{prefix}sr', f'{prefix}avg', f'{prefix}dot_pct', 
            f'{prefix}bound_pct', f'{prefix}wpa', f'{prefix}wpa_per_100', f'{prefix}matches']
    return agg[cols]

bowl_hp = aggregate_bowling(hp_bowl, prefix='hp_')
bowl_base = aggregate_bowling(base_bowl, prefix='base_')
bowl_all = aggregate_bowling(all_bowl, prefix='all_')

bowl_merged = bowl_hp.merge(bowl_base, on=['bowler_id', 'bowler_name'], how='left')
bowl_merged = bowl_merged.merge(bowl_all, on=['bowler_id', 'bowler_name'], how='left')

for col in bowl_merged.columns:
    if 'base_' in col or 'all_' in col:
        bowl_merged[col] = bowl_merged[col].fillna(0)

# Qualification: minimum 120 legal deliveries under HIGH pressure, and minimum 250 total balls
bowl_qual = bowl_merged[(bowl_merged['hp_balls'] >= 120) & (bowl_merged['all_balls'] >= 250)].copy()

# Bayesian Shrinkage on HP Economy and HP Strike Rate
prior_econ = bowl_qual['hp_runs'].sum() / (bowl_qual['hp_balls'].sum() / 6.0)
prior_bowl_sr = bowl_qual['hp_balls'].sum() / bowl_qual['hp_wkts'].sum()
k_bowl_econ = 60.0 # Shrinkage balls
k_bowl_wkt = 6.0 # Shrinkage wickets

bowl_qual['hp_econ_bayes'] = ((bowl_qual['hp_balls'] / (bowl_qual['hp_balls'] + k_bowl_econ)) * bowl_qual['hp_econ'] + 
                             (k_bowl_econ / (bowl_qual['hp_balls'] + k_bowl_econ)) * prior_econ)
bowl_qual['hp_sr_bayes'] = ((bowl_qual['hp_wkts'] / (bowl_qual['hp_wkts'] + k_bowl_wkt)) * bowl_qual['hp_sr'] + 
                            (k_bowl_wkt / (bowl_qual['hp_wkts'] + k_bowl_wkt)) * prior_bowl_sr)

# Clutch Deltas
bowl_qual['delta_econ'] = bowl_qual['base_econ'] - bowl_qual['hp_econ'] # positive means more economical under HP!
bowl_qual['delta_dot_pct'] = bowl_qual['hp_dot_pct'] - bowl_qual['base_dot_pct']
bowl_qual['delta_bound_pct'] = bowl_qual['base_bound_pct'] - bowl_qual['hp_bound_pct'] # positive means fewer boundaries

# Match consistency
hp_match_bowl = hp_bowl.groupby(['bowler_id', 'match_id']).agg(
    m_runs=('bowler_runs_conceded', 'sum'),
    m_balls=('runs', 'count'),
    m_wkts=('is_bowler_wicket', 'sum'),
    m_wpa=('wpa_bowl', 'sum')
).reset_index()
hp_match_bowl['pos_impact'] = (hp_match_bowl['m_wpa'] > 0.0) | (hp_match_bowl['m_wkts'] >= 1) | ((hp_match_bowl['m_runs'] / np.maximum(1, hp_match_bowl['m_balls']/6.0)) <= 8.0)
bowl_consistency = hp_match_bowl.groupby('bowler_id')['pos_impact'].mean().rename('hp_consistency_rate').reset_index()

bowl_qual = bowl_qual.merge(bowl_consistency, on='bowler_id', how='left')

# Composite Bowling Pressure Reliability Score (Bowl-PRS, 0-100)
# Note: for economy, lower is better (so invert)
# for strike rate, lower is better (so invert)
bowl_qual['norm_econ'] = min_max_norm(bowl_qual['hp_econ_bayes'].max() - bowl_qual['hp_econ_bayes'])
bowl_qual['norm_sr'] = min_max_norm(bowl_qual['hp_sr_bayes'].max() - bowl_qual['hp_sr_bayes'])
bowl_qual['norm_dot'] = min_max_norm(bowl_qual['hp_dot_pct'])
bowl_qual['norm_bound'] = min_max_norm(bowl_qual['hp_bound_pct'].max() - bowl_qual['hp_bound_pct']) # lower bound % is better
bowl_qual['norm_wpa'] = min_max_norm(bowl_qual['hp_wpa_per_100'])
bowl_qual['norm_delta_econ'] = min_max_norm(bowl_qual['delta_econ'])
bowl_qual['norm_cons'] = min_max_norm(bowl_qual['hp_consistency_rate'])

bowl_qual['bowling_prs'] = (
    0.25 * bowl_qual['norm_econ'] + 
    0.25 * bowl_qual['norm_sr'] + 
    0.15 * bowl_qual['norm_dot'] + 
    0.15 * bowl_qual['norm_bound'] + 
    0.10 * bowl_qual['norm_wpa'] + 
    0.05 * bowl_qual['norm_delta_econ'] + 
    0.05 * bowl_qual['norm_cons']
) * 100.0

top_bowlers = bowl_qual.sort_values(by='bowling_prs', ascending=False).reset_index(drop=True)
print("\n=== TOP 20 BOWLERS UNDER PRESSURE ===")
display_cols_bowl = ['bowler_name', 'hp_balls', 'hp_overs', 'hp_wkts', 'hp_econ', 'hp_sr', 'base_econ', 'delta_econ', 'hp_dot_pct', 'hp_bound_pct', 'hp_wpa', 'bowling_prs']
print(top_bowlers[display_cols_bowl].head(20).to_string(index=True))

# Save rankings
top_batters.to_csv(os.path.join(OUT_DIR, "batters_pressure_rankings.csv"), index=False)
top_bowlers.to_csv(os.path.join(OUT_DIR, "bowlers_pressure_rankings.csv"), index=False)
print("\nSaved batters and bowlers pressure rankings to CSV.")
