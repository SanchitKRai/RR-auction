import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"
os.makedirs(os.path.join(OUT_DIR, "figures"), exist_ok=True)

# Set matplotlib style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# Load data
top_b = pd.read_csv(os.path.join(OUT_DIR, "batters_pressure_rankings.csv"))
top_bw = pd.read_csv(os.path.join(OUT_DIR, "bowlers_pressure_rankings.csv"))

print("Generating Figure 1: Batting Pressure Frontier (SR vs Avg)...")
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

# Filter top batters
sub_b = top_b[top_b['hp_balls'] >= 140].copy()
scatter = ax.scatter(
    sub_b['hp_sr'], sub_b['hp_avg'], 
    s=np.clip(sub_b['hp_wpa'] * 60 + 50, 30, 300), 
    c=sub_b['batting_prs'], cmap='viridis', 
    alpha=0.75, edgecolors='black', linewidth=0.5
)

# Highlight Top 10
highlight_batters = ['Vaibhav Sooryavanshi', 'Ashutosh Sharma', 'Virat Kohli', 'Sai Sudharsan', 
                     'Suryakumar Yadav', 'Tim David', 'Shashank Singh', 'Rinku Singh', 
                     'Yashasvi Jaiswal', 'David Miller', 'Heinrich Klaasen']

for _, r in sub_b[sub_b['striker_name'].isin(highlight_batters)].iterrows():
    ax.annotate(
        r['striker_name'], 
        (r['hp_sr'], r['hp_avg']),
        xytext=(5, 5), textcoords='offset points',
        fontsize=8.5, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='#999999')
    )

ax.set_xlabel('Pressure Strike Rate (Runs per 100 Balls)', fontsize=11, fontweight='bold')
ax.set_ylabel('Pressure Batting Average (Runs per Dismissal)', fontsize=11, fontweight='bold')
ax.set_title('T20 Batting Under Pressure Frontier (Min 140 HP Balls)\nBubble Size ~ Win Probability Added (WPA)', fontsize=13, fontweight='bold', pad=12)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Batting Pressure Reliability Score (B-PRS)', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figures", "batting_frontier.png"), dpi=300)
plt.close()


print("Generating Figure 2: Bowling Pressure Frontier (Economy vs Strike Rate)...")
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

sub_bw = top_bw[top_bw['hp_balls'] >= 140].copy()
scatter_bw = ax.scatter(
    sub_bw['hp_econ'], sub_bw['hp_sr'], 
    s=np.clip(sub_bw['hp_wpa'] * 50 + 50, 30, 300), 
    c=sub_bw['bowling_prs'], cmap='plasma_r', 
    alpha=0.75, edgecolors='black', linewidth=0.5
)

highlight_bowlers = ['Matheesha Pathirana', 'Mitchell Santner', 'Sunil Narine', 'Varun Chakravarthy', 
                     'Kuldeep Yadav', 'Jasprit Bumrah', 'Rashid Khan', 'Arshdeep Singh', 
                     'Krunal Pandya', 'Jamie Overton', 'Mujeeb Ur Rahman', 'Sandeep Sharma']

for _, r in sub_bw[sub_bw['bowler_name'].isin(highlight_bowlers)].iterrows():
    offset = (5, 5)
    if r['bowler_name'] == 'Sandeep Sharma':
        offset = (-80, -10)
    elif r['bowler_name'] == 'Matheesha Pathirana':
        offset = (5, -12)
    ax.annotate(
        r['bowler_name'], 
        (r['hp_econ'], r['hp_sr']),
        xytext=offset, textcoords='offset points',
        fontsize=8.5, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='#999999')
    )

# Invert axes so top-right is elite (lower economy, lower strike rate)
ax.invert_xaxis()
ax.invert_yaxis()

ax.set_xlabel('Pressure Economy Rate (Runs/Over, Inverted: Lower = Left-to-Right)', fontsize=11, fontweight='bold')
ax.set_ylabel('Pressure Bowling Strike Rate (Balls/Wicket, Inverted: Lower = Bottom-to-Top)', fontsize=11, fontweight='bold')
ax.set_title('T20 Bowling Under Pressure Frontier (Min 140 HP Balls)\nBubble Size ~ Bowling WPA | Top-Right Quadrant = Elite Restriction & Wickets', fontsize=12, fontweight='bold', pad=12)

cbar = plt.colorbar(scatter_bw, ax=ax)
cbar.set_label('Bowling Pressure Reliability Score (Bowl-PRS)', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figures", "bowling_frontier.png"), dpi=300)
plt.close()


print("Generating Figure 3: Clutch Delta Comparison for Key Batters...")
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

clutch_batters = ['Ashutosh Sharma', 'Dinesh Karthik', 'Rinku Singh', 'Reeza Hendricks', 
                   'Vaibhav Sooryavanshi', 'Virat Kohli', 'Sai Sudharsan', 'Hardik Pandya',
                   'Yashasvi Jaiswal', 'Suryakumar Yadav', 'Tim David', 'Shivam Dube']

bat_df_clutch = top_b[top_b['striker_name'].isin(clutch_batters)].sort_values(by='delta_sr', ascending=True)

y_pos = np.arange(len(bat_df_clutch))
colors = ['#2ECC71' if x > 0 else '#E74C3C' for x in bat_df_clutch['delta_sr']]

bars = ax.barh(y_pos, bat_df_clutch['delta_sr'], color=colors, alpha=0.85, edgecolor='black', linewidth=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(bat_df_clutch['striker_name'], fontsize=9, fontweight='bold')
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_xlabel('Strike Rate Clutch Delta: Pressure SR - Baseline SR', fontsize=11, fontweight='bold')
ax.set_title('Batting Clutch Elevation Index (Delta Strike Rate Under Pressure)', fontsize=12, fontweight='bold')

for bar in bars:
    w = bar.get_width()
    ax.annotate(f"{w:+.1f}",
                xy=(w, bar.get_y() + bar.get_height() / 2),
                xytext=(5 if w >= 0 else -25, 0), textcoords="offset points",
                ha='left' if w >= 0 else 'right', va='center',
                fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figures", "batting_clutch_delta.png"), dpi=300)
plt.close()


print("Generating Figure 4: Rajasthan Royals 2026 Bowling Gaps vs Target Bowlers...")
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

comp_bowlers = [
    ('Matheesha Pathirana', 'Target: Death Specialist', 7.78, 10.31, '#27AE60'),
    ('Mitchell Santner', 'Target: Control Maestro', 6.45, 14.31, '#27AE60'),
    ('Varun Chakravarthy', 'Target: Mystery Wickets', 7.23, 14.39, '#27AE60'),
    ('Kuldeep Yadav', 'Target: Wrist Spin Wickets', 6.89, 15.48, '#27AE60'),
    ('Jofra Archer', 'RR 2026 Frontline', 8.62, 13.05, '#3498DB'),
    ('Ravi Bishnoi', 'RR 2026 Frontline', 8.45, 21.66, '#E67E22'),
    ('Nandre Burger', 'RR 2026 Frontline', 8.88, 17.80, '#E67E22'),
    ('Sandeep Sharma', 'RR 2026 Death Leak', 9.70, 19.33, '#E74C3C'),
    ('Tushar Deshpande', 'RR 2026 Death Leak', 9.84, 15.37, '#E74C3C'),
    ('Sam Curran', 'RR 2026 Death Leak', 10.21, 19.35, '#C0392B')
]

names = [x[0] for x in comp_bowlers]
roles = [x[1] for x in comp_bowlers]
econs = [x[2] for x in comp_bowlers]
srs = [x[3] for x in comp_bowlers]
colors = [x[4] for x in comp_bowlers]

y_pos = np.arange(len(names))
bars = ax.barh(y_pos, econs, color=colors, alpha=0.85, edgecolor='black', linewidth=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels([f"{n} ({r})" for n, r in zip(names, roles)], fontsize=8.5, fontweight='bold')
ax.axvline(8.5, color='gray', linestyle=':', label='IPL Death Par Economy (8.50)')
ax.set_xlabel('Pressure Economy Rate (Runs per Over)', fontsize=11, fontweight='bold')
ax.set_title('Rajasthan Royals 2026 Bowling Leak vs. High-Pressure Auction Targets', fontsize=12, fontweight='bold')

for bar, sr in zip(bars, srs):
    w = bar.get_width()
    ax.annotate(f"{w:.2f} rpo (SR: {sr:.1f})",
                xy=(w, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figures", "rr_bowling_diagnosis.png"), dpi=300)
plt.close()

print("All figures successfully created in:", os.path.join(OUT_DIR, "figures"))
