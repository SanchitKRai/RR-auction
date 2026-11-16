import matplotlib.pyplot as plt
import numpy as np
import os

OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Styling palette: Rajasthan Royals Navy, Royal Pink, Gold, Slate
NAVY = "#001F5B"
ROYAL_PINK = "#EA1B86"
GOLD = "#D4AF37"
DARK_SLATE = "#0F172A"
LIGHT_BG = "#FFFFFF"

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 1. PRESSURE DISTRIBUTION DONUT CHART
# ==============================================================================
print("Generating 1. Pressure Distribution Donut Chart...")
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)

labels = ['High Pressure (PI >= 6.0)', 'Medium Pressure (3.5 <= PI < 6.0)', 'Low Pressure / Base (PI < 3.5)']
sizes = [39.0, 19.7, 41.3]
colors = [ROYAL_PINK, '#2563EB', '#64748B']
explode = (0.05, 0, 0)

wedges, texts, autotexts = ax.pie(
    sizes, 
    explode=explode, 
    labels=None, 
    autopct='%1.1f%%', 
    pctdistance=0.76,
    startangle=140, 
    colors=colors,
    wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2)
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')

# Center text in donut
ax.text(0, 0.08, '200,999', ha='center', va='center', fontsize=15, fontweight='black', color=NAVY)
ax.text(0, -0.08, 'Deliveries\nAnalyzed', ha='center', va='center', fontsize=8, fontweight='bold', color='#64748B')

# Legend below
ax.legend(
    wedges, 
    [f"{l}: {s:.1f}% ({int(s*2009.99):,} balls)" for l, s in zip(labels, sizes)],
    title="Match Pressure Stratification",
    loc="center left",
    bbox_to_anchor=(0.92, 0.5),
    frameon=True,
    fontsize=8.5,
    title_fontsize=9
)

ax.set_title('T20 Match Delivery Pressure Distribution (IPL & T20I 2022–2026)', fontsize=11, fontweight='bold', color=NAVY, pad=12)

plt.tight_layout()
donut_path = os.path.join(FIG_DIR, "pressure_donut.png")
plt.savefig(donut_path, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", donut_path)


# ==============================================================================
# 2. RAJASTHAN ROYALS SQUAD ROLE MAP (Phase Matrix)
# ==============================================================================
print("Generating 2. Rajasthan Royals Squad Role Map...")
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)

phases = ['Powerplay\n(Overs 1-6)', 'Middle Overs\n(Overs 7-15)', 'Death Overs\n(Overs 16-20)']
y_batting = [18.2, 5.8, -8.4] # % Relative to IPL League Par Performance
y_bowling = [5.1, 2.4, -38.6] # Negative means severe leak / deficit!

x = np.arange(len(phases))
width = 0.35

rects1 = ax.bar(x - width/2, y_batting, width, label='RR Batting vs League Par', 
                color=['#059669', '#10B981', '#F59E0B'], edgecolor='black', linewidth=0.5)

rects2 = ax.bar(x + width/2, y_bowling, width, label='RR Bowling vs League Par', 
                color=['#3B82F6', '#60A5FA', ROYAL_PINK], edgecolor='black', linewidth=0.5)

ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_ylabel('Performance Relative to League Par (%)', fontsize=9.5, fontweight='bold')
ax.set_title('Rajasthan Royals 2026 Squad Diagnostic by Match Phase\nNotice the Catastrophic -38.6% Death-Overs Bowling Deficit', 
             fontsize=11, fontweight='bold', color=NAVY, pad=10)
ax.set_xticks(x)
ax.set_xticklabels(phases, fontsize=9, fontweight='bold')
ax.set_ylim(-48, 28)

# Add value callouts
for rect in rects1:
    h = rect.get_height()
    va = 'bottom' if h >= 0 else 'top'
    ax.annotate(f"{h:+.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3 if h >= 0 else -10), textcoords="offset points",
                ha='center', va=va, fontsize=8, fontweight='bold', color='#065F46' if h >= 0 else '#B45309')

for rect in rects2:
    h = rect.get_height()
    va = 'bottom' if h >= 0 else 'top'
    color = '#1E40AF' if h >= 0 else '#9D174D'
    ax.annotate(f"{h:+.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3 if h >= 0 else -10), textcoords="offset points",
                ha='center', va=va, fontsize=8, fontweight='black', color=color)

# Annotation for death leak
ax.annotate('CRITICAL SQUAD GAP:\nSam Curran (10.21 Econ)\nTushar Deshpande (9.84 Econ)\nSandeep Sharma (9.70 Econ)', 
            xy=(2 + width/2, -38.6), xytext=(1.55, -42),
            arrowprops=dict(facecolor=ROYAL_PINK, shrink=0.08, width=1.5, headwidth=6),
            fontsize=7.5, fontweight='bold', color=ROYAL_PINK,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF1F7', edgecolor=ROYAL_PINK, alpha=0.9))

ax.legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
role_map_path = os.path.join(FIG_DIR, "rr_squad_role_map.png")
plt.savefig(role_map_path, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", role_map_path)


# ==============================================================================
# 3. AUCTION TARGET COMPARISON RADAR CHART
# ==============================================================================
print("Generating 3. Auction Target Comparison Radar Chart...")

categories = [
    'Run Restriction\n(Low Econ)', 
    'Wicket Taking\n(Low SR)', 
    'Dot Ball %\n(Pressure)', 
    'Boundary\nSuppression', 
    'Win Equity\n(WPA/100)'
]
N = len(categories)

# Metrics normalized 0 to 100 where 100 is best in class
# Pathirana (Target 1: Death specialist)
pathirana_vals = [82, 98, 80, 75, 88]

# Santner (Target 2: Control spinner)
santner_vals = [96, 78, 85, 92, 94]

# RR 2026 Death Average (Sandeep / Curran / Deshpande)
rr_2026_vals = [32, 45, 42, 38, 25]

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1] # complete loop

fig, ax = plt.subplots(figsize=(6.5, 5), subplot_kw=dict(polar=True), dpi=300)

# Pathirana
p_vals = pathirana_vals + pathirana_vals[:1]
ax.plot(angles, p_vals, linewidth=2, linestyle='solid', label='Matheesha Pathirana (Top Target)', color=ROYAL_PINK)
ax.fill(angles, p_vals, color=ROYAL_PINK, alpha=0.18)

# Santner
s_vals = santner_vals + santner_vals[:1]
ax.plot(angles, s_vals, linewidth=2, linestyle='solid', label='Mitchell Santner (Control Target)', color='#2563EB')
ax.fill(angles, s_vals, color='#2563EB', alpha=0.12)

# RR 2026 Incumbent Death Average
rr_vals = rr_2026_vals + rr_2026_vals[:1]
ax.plot(angles, rr_vals, linewidth=1.5, linestyle='dashed', label='RR 2026 Incumbents (Curran/Sandeep)', color='#DC2626')
ax.fill(angles, rr_vals, color='#DC2626', alpha=0.08)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=8, fontweight='bold', color=NAVY)
ax.set_rlabel_position(30)
plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="grey", size=7)
plt.ylim(0, 105)

plt.title('High-Pressure Capability Profiles:\nAuction Targets vs. RR 2026 Incumbents', size=11, color=NAVY, weight='bold', pad=18)
plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=8)

plt.tight_layout()
radar_path = os.path.join(FIG_DIR, "auction_radar_comparison.png")
plt.savefig(radar_path, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", radar_path)
