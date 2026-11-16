import pandas as pd
import os

OUT_DIR = r"C:\Users\lenovo\Downloads\rr\Data Pack"
comps = pd.read_csv(os.path.join(OUT_DIR, "competitions.csv"))
matches = pd.read_csv(os.path.join(OUT_DIR, "matches.csv"))
bbb = pd.read_csv(os.path.join(OUT_DIR, "ball_by_ball.csv"))

b_merged = bbb.merge(matches[['match_id', 'comp_id']], on='match_id').merge(comps[['comp_id', 'comp_name', 'match_format', 'season']], on='comp_id')

def inspect_player_comps(player_name, role='batter'):
    if role == 'batter':
        sub = b_merged[b_merged['striker_name'] == player_name]
    else:
        sub = b_merged[b_merged['bowler_name'] == player_name]
    ipl_balls = len(sub[sub['match_format'] == 'T20'])
    t20i_balls = len(sub[sub['match_format'] == 'T20I'])
    c_counts = sub['comp_name'].value_counts().head(5).to_dict()
    print(f"{player_name} ({role}): Total={len(sub)}, IPL={ipl_balls}, T20I={t20i_balls}")
    print(f"  Top Comps: {c_counts}")

print("=== BATTERS ===")
for p in ['Vaibhav Sooryavanshi', 'Ashutosh Sharma', 'Reeza Hendricks', 'Virat Kohli', 
          'Sai Sudharsan', 'Suryakumar Yadav', 'Priyansh Arya', 'Tim David', 
          'Shashank Singh', 'Dinesh Karthik', 'Rinku Singh', 'Yashasvi Jaiswal', 'Heinrich Klaasen']:
    inspect_player_comps(p, 'batter')

print("\n=== BOWLERS ===")
for p in ['Sufiyan Muqeem', 'Salman Mirza', 'Mujeeb Ur Rahman', 'Shaheen Afridi', 
          'Mitchell Santner', 'Taskin Ahmed', 'Sunil Narine', 'Krunal Pandya', 
          'Matheesha Pathirana', 'Varun Chakravarthy', 'Kuldeep Yadav', 'Jasprit Bumrah', 
          'Arshdeep Singh', 'Rashid Khan', 'Sandeep Sharma']:
    inspect_player_comps(p, 'bowler')
