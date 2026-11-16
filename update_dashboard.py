import pandas as pd
import json
import os

OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"

top_b = pd.read_csv(os.path.join(OUT_DIR, "batters_pressure_rankings.csv"))
top_bw = pd.read_csv(os.path.join(OUT_DIR, "bowlers_pressure_rankings.csv"))

batters_data = top_b.head(40)[[
    'striker_name', 'hp_balls', 'hp_runs', 'hp_sr', 'hp_avg', 
    'base_sr', 'delta_sr', 'hp_dot_pct', 'hp_bound_pct', 'hp_wpa', 'batting_prs'
]].to_dict(orient='records')

bowlers_data = top_bw.head(40)[[
    'bowler_name', 'hp_balls', 'hp_overs', 'hp_wkts', 'hp_econ', 
    'hp_sr', 'base_econ', 'delta_econ', 'hp_dot_pct', 'hp_bound_pct', 'hp_wpa', 'bowling_prs'
]].to_dict(orient='records')

dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rajasthan Royals War Room • SupeRR Selector Dashboard</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
  .tab-active {{ border-bottom: 3px solid #EA1B86; color: #EA1B86; font-weight: 700; }}
</style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">

<!-- NAVBAR -->
<header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <div class="w-10 h-10 rounded-full bg-[#001F5B] border-2 border-amber-400 flex items-center justify-center font-black text-xl text-white shadow-lg shadow-pink-500/20">RR</div>
      <div>
        <h1 class="text-base font-extrabold tracking-tight text-white flex items-center gap-2">
          Rajasthan Royals War Room <span class="text-xs px-2 py-0.5 rounded bg-pink-500/20 text-pink-400 border border-pink-500/30">SupeRR Selector S2</span>
        </h1>
        <p class="text-xs text-slate-400">Independent Research • Pressure Reliability &amp; IPL 2027 Auction Engine</p>
      </div>
    </div>
    <div class="flex items-center space-x-2 text-xs">
      <span class="px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">883 Matches</span>
      <span class="px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">200,999 Balls</span>
      <a href="SupeRR_Selector_Season2_RR_WarRoom_Report.pdf" target="_blank" class="px-3 py-1 rounded-full bg-pink-600 hover:bg-pink-500 text-white font-bold transition flex items-center gap-1 shadow-lg shadow-pink-600/30">
        <span>Download PDF Report (9 Pages)</span> &rarr;
      </a>
    </div>
  </div>
</header>

<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

  <!-- TOP SUMMARY CARDS -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
      <div class="absolute top-0 right-0 w-24 h-24 bg-pink-500/10 rounded-bl-full pointer-events-none"></div>
      <span class="text-xs uppercase tracking-wider text-pink-400 font-bold">#1 Pressure Batter</span>
      <div class="text-lg font-black text-white mt-1">Vaibhav Sooryavanshi</div>
      <div class="text-xs text-slate-300 mt-1">SR: <b class="text-pink-400">240.82</b> • Avg: <b>42.91</b> • 42.9% Bounds</div>
      <div class="mt-2 text-[11px] text-emerald-400 font-semibold flex items-center gap-1">★ In RR Squad (Retain &amp; Back)</div>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
      <div class="absolute top-0 right-0 w-24 h-24 bg-amber-500/10 rounded-bl-full pointer-events-none"></div>
      <span class="text-xs uppercase tracking-wider text-amber-400 font-bold">#1 Clutch Finisher Target</span>
      <div class="text-lg font-black text-white mt-1">Ashutosh Sharma</div>
      <div class="text-xs text-slate-300 mt-1">SR: <b class="text-amber-400">189.10</b> • Delta SR: <b class="text-emerald-400">+58.22</b></div>
      <div class="mt-2 text-[11px] text-amber-300 font-semibold">Target Budget: ₹5.0 – 7.0 Cr</div>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
      <div class="absolute top-0 right-0 w-24 h-24 bg-pink-500/10 rounded-bl-full pointer-events-none"></div>
      <span class="text-xs uppercase tracking-wider text-pink-400 font-bold">#1 Death Specialist Target</span>
      <div class="text-lg font-black text-white mt-1">Matheesha Pathirana</div>
      <div class="text-xs text-slate-300 mt-1">51 Wkts • SR: <b class="text-pink-400">10.31</b> • Econ: <b>7.78</b></div>
      <div class="mt-2 text-[11px] text-pink-400 font-semibold">Priority 1 Target: ₹12.0 – 14.5 Cr</div>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
      <div class="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 rounded-bl-full pointer-events-none"></div>
      <span class="text-xs uppercase tracking-wider text-blue-400 font-bold">#1 Spin Controller Target</span>
      <div class="text-lg font-black text-white mt-1">Mitchell Santner</div>
      <div class="text-xs text-slate-300 mt-1">Econ: <b class="text-emerald-400">6.45</b> • WPA: <b class="text-blue-400">+2.25</b> • 42.3% Dots</div>
      <div class="mt-2 text-[11px] text-blue-300 font-semibold">Target Budget: ₹6.5 – 8.0 Cr</div>
    </div>
  </div>

  <!-- TABS & TABLE -->
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
    <div class="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-800 pb-3">
      <div class="flex space-x-6 text-sm">
        <button id="tab-batters" onclick="switchTab('batters')" class="tab-active pb-2 transition">Top Batters Under Pressure</button>
        <button id="tab-bowlers" onclick="switchTab('bowlers')" class="text-slate-400 hover:text-white pb-2 transition">Top Bowlers Under Pressure</button>
        <button id="tab-rr-squad" onclick="switchTab('rr-squad')" class="text-slate-400 hover:text-white pb-2 transition">RR 2027 Auction War Room</button>
      </div>
      <div class="w-full sm:w-72">
        <input type="text" id="search-input" onkeyup="filterTable()" placeholder="Search player name..." 
               class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-pink-500">
      </div>
    </div>

    <!-- BATTERS TABLE -->
    <div id="section-batters" class="mt-4 overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead class="text-slate-400 border-b border-slate-800 uppercase tracking-wider text-[11px] bg-slate-950/60">
          <tr>
            <th class="py-2.5 px-3">Rank</th>
            <th class="py-2.5 px-3">Batter</th>
            <th class="py-2.5 px-3 text-right">HP Balls</th>
            <th class="py-2.5 px-3 text-right">HP Runs</th>
            <th class="py-2.5 px-3 text-right">HP Strike Rate</th>
            <th class="py-2.5 px-3 text-right">HP Average</th>
            <th class="py-2.5 px-3 text-right">Base SR</th>
            <th class="py-2.5 px-3 text-right">Delta SR</th>
            <th class="py-2.5 px-3 text-right">Dot %</th>
            <th class="py-2.5 px-3 text-right">Boundary %</th>
            <th class="py-2.5 px-3 text-right">HP WPA</th>
            <th class="py-2.5 px-3 text-right">B-PRS</th>
          </tr>
        </thead>
        <tbody id="batters-tbody" class="divide-y divide-slate-800/60">
        </tbody>
      </table>
    </div>

    <!-- BOWLERS TABLE -->
    <div id="section-bowlers" class="mt-4 overflow-x-auto hidden">
      <table class="w-full text-left text-xs">
        <thead class="text-slate-400 border-b border-slate-800 uppercase tracking-wider text-[11px] bg-slate-950/60">
          <tr>
            <th class="py-2.5 px-3">Rank</th>
            <th class="py-2.5 px-3">Bowler</th>
            <th class="py-2.5 px-3 text-right">HP Balls</th>
            <th class="py-2.5 px-3 text-right">HP Overs</th>
            <th class="py-2.5 px-3 text-right">HP Wickets</th>
            <th class="py-2.5 px-3 text-right">HP Economy</th>
            <th class="py-2.5 px-3 text-right">HP Strike Rate</th>
            <th class="py-2.5 px-3 text-right">Delta Econ</th>
            <th class="py-2.5 px-3 text-right">Dot %</th>
            <th class="py-2.5 px-3 text-right">Boundary %</th>
            <th class="py-2.5 px-3 text-right">HP WPA</th>
            <th class="py-2.5 px-3 text-right">Bowl-PRS</th>
          </tr>
        </thead>
        <tbody id="bowlers-tbody" class="divide-y divide-slate-800/60">
        </tbody>
      </table>
    </div>

    <!-- RR SQUAD STRATEGY SECTION -->
    <div id="section-rr-squad" class="mt-4 hidden space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
          <h3 class="text-sm font-bold text-pink-400 uppercase tracking-wider mb-2">RR 2026 Bowling Failure Diagnostic</h3>
          <p class="text-xs text-slate-300 leading-relaxed">
            In 2026, Rajasthan Royals possessed no frontline bowlers in the world top 50 under high pressure. Sam Curran bled <b class="text-red-400">10.21 rpo</b> (rank 164), Tushar Deshpande bled <b class="text-red-400">9.84 rpo</b> (rank 134), and Sandeep Sharma bled <b class="text-red-400">9.70 rpo</b> (rank 159). RR lost 4 matches where they entered the 16th over with a &gt;75% win probability.
          </p>
          <div class="mt-4 space-y-2 text-xs">
            <div class="flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800">
              <span>Sam Curran (RR 2026)</span>
              <span class="font-bold text-red-400">10.21 Econ (Rank 164)</span>
            </div>
            <div class="flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800">
              <span>Tushar Deshpande (RR 2026)</span>
              <span class="font-bold text-red-400">9.84 Econ (Rank 134)</span>
            </div>
            <div class="flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800">
              <span>Sandeep Sharma (RR 2026)</span>
              <span class="font-bold text-red-400">9.70 Econ (Rank 159)</span>
            </div>
            <div class="flex justify-between items-center p-2 rounded bg-emerald-950/40 border border-emerald-500/30">
              <span class="text-emerald-300 font-bold">Matheesha Pathirana (Top Target)</span>
              <span class="font-bold text-emerald-400">7.78 Econ • 10.31 SR (51 Wkts)</span>
            </div>
          </div>
        </div>

        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
          <h3 class="text-sm font-bold text-pink-400 uppercase tracking-wider mb-2">Simulated RR Playing XI (IPL 2027)</h3>
          <div class="space-y-1.5 text-xs">
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>1. Yashasvi Jaiswal (LHB)</span>
              <span class="text-slate-400">Powerplay Enforcer (167.3 SR HP)</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>2. Vaibhav Sooryavanshi (LHB)</span>
              <span class="text-pink-400 font-bold">World #1 Pressure Batter (240.8 SR HP)</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>3. Sanju Samson (C &amp; WK)</span>
              <span class="text-slate-400">Anchor &amp; Spin Smasher</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>4. Riyan Parag (RHB)</span>
              <span class="text-slate-400">Middle Overs Hitter</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>5. Dhruv Jurel (RHB)</span>
              <span class="text-slate-400">Crisis Stabilizer &amp; Rotator</span>
            </div>
            <div class="p-2 rounded bg-amber-950/40 border border-amber-500/30 flex justify-between">
              <span class="text-amber-300 font-bold">6. Ashutosh Sharma (RHB) ★ Target</span>
              <span class="text-amber-400 font-bold">World #1 Clutch Finisher (+58.2 Delta SR)</span>
            </div>
            <div class="p-2 rounded bg-blue-950/40 border border-blue-500/30 flex justify-between">
              <span class="text-blue-300 font-bold">7. Mitchell Santner / Jadeja (SLA) ★ Target</span>
              <span class="text-blue-400 font-bold">Control Spin (6.45 Econ, +2.25 WPA)</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>8. Jofra Archer (RHF)</span>
              <span class="text-slate-400">Express Powerplay Pace</span>
            </div>
            <div class="p-2 rounded bg-pink-950/40 border border-pink-500/30 flex justify-between">
              <span class="text-pink-300 font-bold">9. Matheesha Pathirana (RHF) ★ Top Pick</span>
              <span class="text-pink-400 font-bold">51 Wkts • 10.31 SR (World No. 1 Closer)</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>10. Kuldeep Sen / Umran Malik (RHF)</span>
              <span class="text-slate-400">150 km/h Middle Enforcer</span>
            </div>
            <div class="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between">
              <span>11. Ravi Bishnoi (Leg-Spin)</span>
              <span class="text-slate-400">Middle-Overs Attacking Wrist Spin</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</main>

<script>
const batters = {json.dumps(batters_data)};
const bowlers = {json.dumps(bowlers_data)};

function populateBatters(data) {{
  const tbody = document.getElementById('batters-tbody');
  tbody.innerHTML = '';
  data.forEach((p, idx) => {{
    const tr = document.createElement('tr');
    tr.className = idx < 3 ? 'bg-pink-500/10 hover:bg-pink-500/20' : 'hover:bg-slate-800/40';
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-bold">${{idx + 1}}</td>
      <td class="py-2.5 px-3 font-semibold text-white">${{p.striker_name}}</td>
      <td class="py-2.5 px-3 text-right text-slate-300">${{p.hp_balls}}</td>
      <td class="py-2.5 px-3 text-right text-slate-300">${{p.hp_runs}}</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.hp_sr >= 170 ? 'text-pink-400' : 'text-slate-200'}}">${{p.hp_sr.toFixed(1)}}</td>
      <td class="py-2.5 px-3 text-right font-bold text-slate-200">${{p.hp_avg.toFixed(1)}}</td>
      <td class="py-2.5 px-3 text-right text-slate-400">${{p.base_sr.toFixed(1)}}</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.delta_sr > 0 ? 'text-emerald-400' : 'text-red-400'}}">${{p.delta_sr > 0 ? '+' : ''}}${{p.delta_sr.toFixed(1)}}</td>
      <td class="py-2.5 px-3 text-right text-slate-400">${{p.hp_dot_pct.toFixed(1)}}%</td>
      <td class="py-2.5 px-3 text-right text-slate-300 font-medium">${{p.hp_bound_pct.toFixed(1)}}%</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.hp_wpa > 0 ? 'text-emerald-400' : 'text-slate-400'}}">${{p.hp_wpa > 0 ? '+' : ''}}${{p.hp_wpa.toFixed(2)}}</td>
      <td class="py-2.5 px-3 text-right font-black text-pink-400">${{p.batting_prs.toFixed(1)}}</td>
    `;
    tbody.appendChild(tr);
  }});
}}

function populateBowlers(data) {{
  const tbody = document.getElementById('bowlers-tbody');
  tbody.innerHTML = '';
  data.forEach((p, idx) => {{
    const tr = document.createElement('tr');
    tr.className = idx < 3 ? 'bg-blue-500/10 hover:bg-blue-500/20' : 'hover:bg-slate-800/40';
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-bold">${{idx + 1}}</td>
      <td class="py-2.5 px-3 font-semibold text-white">${{p.bowler_name}}</td>
      <td class="py-2.5 px-3 text-right text-slate-300">${{p.hp_balls}}</td>
      <td class="py-2.5 px-3 text-right text-slate-300">${{p.hp_overs.toFixed(1)}}</td>
      <td class="py-2.5 px-3 text-right font-bold text-white">${{p.hp_wkts}}</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.hp_econ <= 7.0 ? 'text-emerald-400' : 'text-slate-200'}}">${{p.hp_econ.toFixed(2)}}</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.hp_sr <= 12.0 ? 'text-pink-400' : 'text-slate-200'}}">${{p.hp_sr.toFixed(1)}}</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.delta_econ > 0 ? 'text-emerald-400' : 'text-red-400'}}">${{p.delta_econ > 0 ? '+' : ''}}${{p.delta_econ.toFixed(2)}}</td>
      <td class="py-2.5 px-3 text-right text-slate-400">${{p.hp_dot_pct.toFixed(1)}}%</td>
      <td class="py-2.5 px-3 text-right text-slate-300">${{p.hp_bound_pct.toFixed(1)}}%</td>
      <td class="py-2.5 px-3 text-right font-bold ${{p.hp_wpa > 0 ? 'text-emerald-400' : 'text-slate-400'}}">${{p.hp_wpa > 0 ? '+' : ''}}${{p.hp_wpa.toFixed(2)}}</td>
      <td class="py-2.5 px-3 text-right font-black text-blue-400">${{p.bowling_prs.toFixed(1)}}</td>
    `;
    tbody.appendChild(tr);
  }});
}}

let currentTab = 'batters';

function switchTab(tab) {{
  currentTab = tab;
  document.getElementById('tab-batters').className = tab === 'batters' ? 'tab-active pb-2 transition' : 'text-slate-400 hover:text-white pb-2 transition';
  document.getElementById('tab-bowlers').className = tab === 'bowlers' ? 'tab-active pb-2 transition' : 'text-slate-400 hover:text-white pb-2 transition';
  document.getElementById('tab-rr-squad').className = tab === 'rr-squad' ? 'tab-active pb-2 transition' : 'text-slate-400 hover:text-white pb-2 transition';

  document.getElementById('section-batters').classList.toggle('hidden', tab !== 'batters');
  document.getElementById('section-bowlers').classList.toggle('hidden', tab !== 'bowlers');
  document.getElementById('section-rr-squad').classList.toggle('hidden', tab !== 'rr-squad');
}}

function filterTable() {{
  const q = document.getElementById('search-input').value.toLowerCase();
  if (currentTab === 'batters') {{
    const filtered = batters.filter(p => p.striker_name.toLowerCase().includes(q));
    populateBatters(filtered);
  }} else if (currentTab === 'bowlers') {{
    const filtered = bowlers.filter(p => p.bowler_name.toLowerCase().includes(q));
    populateBowlers(filtered);
  }}
}}

populateBatters(batters);
populateBowlers(bowlers);
</script>
</body>
</html>
"""

with open(os.path.join(OUT_DIR, "dashboard.html"), "w", encoding="utf-8") as f:
    f.write(dashboard_html)
print("Updated dashboard.html with refined UI and download link.")
