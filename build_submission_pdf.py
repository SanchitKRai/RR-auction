import os
import base64
import subprocess

OUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"
FIG_DIR = os.path.join(OUT_DIR, "figures")

def img_to_b64(filename):
    path = os.path.join(FIG_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

bat_frontier_b64 = img_to_b64("batting_frontier.png")
bowl_frontier_b64 = img_to_b64("bowling_frontier.png")
bat_clutch_b64 = img_to_b64("batting_clutch_delta.png")
rr_bowling_b64 = img_to_b64("rr_bowling_diagnosis.png")

template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Rajasthan Royals SupeRR Selector Season 2 - Pressure Reliability Report</title>
<style>
  @page {
    size: A4;
    margin: 14mm 14mm 14mm 14mm;
    @bottom-right {
      content: counter(page) " / " counter(pages);
      font-size: 8pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #777;
    }
  }
  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #222222;
    background-color: #FFFFFF;
    line-height: 1.45;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }
  .page-break {
    page-break-after: always;
  }
  .header-banner {
    background: linear-gradient(135deg, #001F5B 0%, #08112C 60%, #EA1B86 100%);
    color: white;
    padding: 24px 28px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  .header-tag {
    display: inline-block;
    background-color: #EA1B86;
    color: white;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
  }
  .header-title {
    font-size: 20pt;
    font-weight: 800;
    margin: 4px 0 6px 0;
    letter-spacing: -0.5px;
  }
  .header-subtitle {
    font-size: 11pt;
    color: #E0E7FF;
    font-weight: 400;
    margin: 0;
  }
  .meta-bar {
    display: flex;
    justify-content: space-between;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.2);
    font-size: 8pt;
    color: #CBD5E1;
  }
  h2 {
    color: #001F5B;
    font-size: 13pt;
    font-weight: 800;
    border-bottom: 2px solid #EA1B86;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  h3 {
    color: #0F172A;
    font-size: 10.5pt;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 6px;
  }
  p {
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
  }
  .grid-2 {
    display: flex;
    gap: 14px;
    margin-bottom: 12px;
  }
  .col {
    flex: 1;
  }
  .card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 10px;
  }
  .card-highlight {
    background: #FFF1F7;
    border: 1px solid #FBCFE8;
    border-left: 4px solid #EA1B86;
  }
  .card-blue {
    background: #F0F4FF;
    border: 1px solid #D6E4FF;
    border-left: 4px solid #001F5B;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin-bottom: 12px;
  }
  th {
    background-color: #001F5B;
    color: white;
    font-weight: 700;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #001F5B;
  }
  th.num, td.num {
    text-align: right;
  }
  th.center, td.center {
    text-align: center;
  }
  td {
    padding: 5px 8px;
    border: 1px solid #CBD5E1;
  }
  tr:nth-child(even) {
    background-color: #F8FAFC;
  }
  tr.highlight-row {
    background-color: #FFF1F7;
    font-weight: bold;
  }
  .rank-pill {
    display: inline-block;
    width: 18px;
    height: 18px;
    line-height: 18px;
    text-align: center;
    border-radius: 50%;
    background-color: #001F5B;
    color: white;
    font-size: 7.5pt;
    font-weight: 700;
  }
  .rank-1 { background-color: #D4AF37; color: black; }
  .rank-2 { background-color: #94A3B8; color: black; }
  .rank-3 { background-color: #CD7F32; color: white; }

  .figure-box {
    text-align: center;
    margin: 10px 0 14px 0;
  }
  .figure-box img {
    max-width: 100%;
    height: auto;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }
  .figure-caption {
    font-size: 7.5pt;
    color: #64748B;
    margin-top: 4px;
    font-style: italic;
  }
  .formula-box {
    background-color: #F1F5F9;
    border-left: 3px solid #001F5B;
    padding: 6px 10px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 8pt;
    margin: 6px 0;
  }
</style>
</head>
<body>

<!-- PAGE 1: COVER & EXECUTIVE SUMMARY -->
<div class="header-banner">
  <div class="header-tag">SupeRR Selector Season 2 • War Room Analytics</div>
  <div class="header-title">Identifying the Most Reliable Players Under Pressure</div>
  <div class="header-subtitle">A Multi-Factor Leverage & Survival Model for the Rajasthan Royals IPL 2027 Auction</div>
  <div class="meta-bar">
    <span><b>Author:</b> SupeRR Analytics Taskforce</span>
    <span><b>Data Coverage:</b> 883 Matches • 200,999 Deliveries (IPL & T20I 2022–2026)</span>
    <span><b>Submission Date:</b> November 2026</span>
  </div>
</div>

<h2>1. Executive Summary & Key War Room Takeaways</h2>
<p>
Winning championships in modern T20 cricket requires players who do not merely accumulate stats in benign conditions, but who elevate their output when win probability swings on every ball. This report delivers Rajasthan Royals an objective, data-driven framework to identify, evaluate, and rank the most reliable batters and bowlers under extreme match pressure.
</p>

<div class="grid-2">
  <div class="col card card-highlight">
    <h3 style="color:#EA1B86; margin-top:0;">Top Batting Insight</h3>
    <p><b>Vaibhav Sooryavanshi (B-PRS: 78.62)</b> and <b>Ashutosh Sharma (B-PRS: 67.65)</b> emerge as the game's preeminent pressure elevators. Sooryavanshi achieves a historic <b>240.82 SR</b> under high pressure (42.86% boundaries). Ashutosh Sharma displays the world's highest clutch surge: leaping from a baseline 130.88 SR to <b>189.10 SR (+58.22 Delta)</b> under pressure with a minuscule 27.0% dot ball rate. Master chasers <b>Virat Kohli (51.88 Avg)</b> and <b>Sai Sudharsan (49.17 Avg)</b> represent the gold standard in wicket-preservation under pressure.</p>
  </div>
  <div class="col card card-blue">
    <h3 style="color:#001F5B; margin-top:0;">Top Bowling Insight & RR Diagnosis</h3>
    <p><b>Matheesha Pathirana (Bowl-PRS: 60.75)</b> is the undisputed death-overs assassin: <b>51 wickets under pressure</b> at a blistering strike rate of <b>10.31 balls/wicket</b> and 7.78 economy. Rajasthan Royals' 2026 campaign was severely undermined by pressure bowling failure: Sandeep Sharma (9.70 econ), Tushar Deshpande (9.84 econ), and Sam Curran (10.21 econ) all ranked outside the top 130 under pressure. Acquiring Pathirana and control maestro <b>Mitchell Santner (6.45 econ, +2.25 WPA)</b> is RR's highest-leverage imperative at the 2027 auction.</p>
  </div>
</div>

<h2>2. Defining Pressure: The Multi-Factor Pressure Index (PI)</h2>
<p>
Pressure cannot be treated as a static label like "the 20th over". It is a dynamic state where the margin for tactical error shrinks to zero. We formulate an objective, continuous <b>Pressure Index (PI in [0, 10])</b> evaluated on every single delivery:
</p>

<div class="formula-box">
  <b>Innings 2 (The Chase):</b> PI = 2.0 + Clip(2.2 x LI, 0, 4.5) + Clip(0.6 x (RRR - 7.5), 0, 3.0) + Death_Urgency(balls &le; 30) + Resource_Depletion(wkts &le; 4)<br>
  <b>Innings 1 (Target Setting):</b> PI = Base_Phase + Collapse_Penalty(&ge;3 wkts in PP or &ge;4 wkts in 12 ov) + Death_Stakes(Overs 16-20)<br>
  <b>Playoffs / Knockouts Multiplier:</b> PI = Min(10.0, PI x 1.20) for Finals, Qualifiers, Eliminators, and Semi-Finals.
</div>

<p>
Deliveries are partitioned into three empirical tiers:
<b>High Pressure (PI &ge; 6.0)</b> representing 39.0% of all deliveries (78,374 balls); 
<b>Medium Pressure (3.5 &le; PI &lt; 6.0)</b> representing 19.7% (39,673 balls); and 
<b>Low Pressure / Baseline (PI &lt; 3.5)</b> representing 41.3% (82,952 balls).
</p>

<div class="grid-2">
  <div class="col card">
    <h3 style="margin-top:0;">Innings 2: Win Probability & Leverage (LI)</h3>
    <p>We train a calibrated logistic regression on all second innings states (AUC = 0.8966, Log-Loss = 0.4018) using runs required, balls remaining, wickets in hand, and required run rate. The Leverage Index (LI) calculates the sensitivity of win probability to a boundary (+4 runs) versus a dismissal on the next delivery. High LI flags the exact moments the match hangs in the balance.</p>
  </div>
  <div class="col card">
    <h3 style="margin-top:0;">Innings 1: Crisis & Death Overs Mechanics</h3>
    <p>In setting a total, pressure manifests through (1) Top-Order Collapses: when a side loses &ge; 3 wickets in the Powerplay, empirical final totals collapse from 197.2 to 152.3 runs (-44.9 run deficit); and (2) Death Overs Execution (Overs 16–20), where run rate expectations exceed 10.5 rpo and every dot ball or boundary causes massive equity swings.</p>
  </div>
</div>

<div class="page-break"></div>

<!-- PAGE 2: PERFORMANCE MEASUREMENT & FAIR COMPARISONS -->
<h2>3. Performance Measurement & Rating Methodology</h2>
<p>
To differentiate genuine high-pressure reliability from noise and reputation, we construct composite <b>Pressure Reliability Scores (PRS)</b> for batters and bowlers, combining rate efficiency, boundary execution, dot suppression, match-winning probability, and elevation over baseline.
</p>

<div class="grid-2">
  <div class="col card">
    <h3 style="color:#EA1B86; margin-top:0;">Batting Pressure Reliability Score (B-PRS)</h3>
    <ul style="padding-left:16px; margin:0; font-size:8.5pt;">
      <li><b>Pressure Strike Rate (SR_HP, 28%):</b> Shrunken scoring velocity under high pressure.</li>
      <li><b>Pressure Average (Avg_HP, 22%):</b> Wicket preservation and game-finishing longevity.</li>
      <li><b>Dot Ball Suppression (100 - Dot%_HP, 15%):</b> Avoiding momentum-killing dots in tight chases.</li>
      <li><b>Boundary Percentage (Bound%_HP, 15%):</b> Ability to pierce pressure fields for 4s and 6s.</li>
      <li><b>Win Probability Added (WPA / 100, 10%):</b> Direct equity swing per 100 pressure balls.</li>
      <li><b>Clutch Delta (Delta SR = SR_HP - SR_Base, 10%):</b> Scoring rate elevation under fire.</li>
    </ul>
  </div>
  <div class="col card">
    <h3 style="color:#001F5B; margin-top:0;">Bowling Pressure Reliability Score (Bowl-PRS)</h3>
    <ul style="padding-left:16px; margin:0; font-size:8.5pt;">
      <li><b>Pressure Economy (Econ_HP, 28%):</b> Run restriction when batters are attacking.</li>
      <li><b>Pressure Strike Rate (SR_Bowl_HP, 27%):</b> Breaking partnerships when wickets kill chases.</li>
      <li><b>Pressure Dot Ball % (Dot%_Bowl_HP, 15%):</b> Creating insurmountable scoreboard pressure.</li>
      <li><b>Boundary Suppression (100 - Bound%_Bowl, 15%):</b> Preventing high-leverage 4s and 6s.</li>
      <li><b>Bowling WPA (WPA_Bowl / 100, 10%):</b> Net equity generated by the bowler.</li>
      <li><b>Clutch Economy Delta (Delta Econ = Econ_Base - Econ_HP, 5%):</b> Economy improvement under fire.</li>
    </ul>
  </div>
</div>

<h2>4. Ensuring Fair Comparisons: Sample Sizes & Competition Context</h2>
<p>
A fatal flaw in naive cricket models is treating all matches equally or allowing small samples to distort rankings. Our system enforces three strict fairness protocols:
</p>
<div class="grid-2">
  <div class="col card">
    <h3 style="margin-top:0;">1. Bayesian Shrinkage (Sample Size Fairness)</h3>
    <p>Players facing small samples can experience artificial variance. We require a minimum of <b>140 High-Pressure deliveries</b> and <b>250 total balls</b>, and apply Empirical Bayes shrinkage:
    M_shrunken = (N / (N + K)) * M_obs + (K / (N + K)) * Prior_mean
    where K=60 balls for strike rate/economy and K=6 dismissals for averages. Small samples are pulled toward the population mean, rewarding proven multi-season durability.</p>
  </div>
  <div class="col card">
    <h3 style="margin-top:0;">2. Competition Quality Calibration</h3>
    <p>Our data proves that competition contexts vary drastically: IPL matches average <b>8.46 rpo</b> and 19.5% boundaries, whereas T20Is average <b>7.76 rpo</b>, and Emerging tournaments average <b>7.24 rpo</b>. We apply a quality weighting:
    <b>Tier 1 (IPL): 1.00x</b> | <b>Tier 2 (T20I): 0.90x</b> | <b>Tier 3 (Emerging/Associate): 0.75x</b>. This prevents bowlers fattening stats on associate tracks from topping elite IPL rankings.</p>
  </div>
</div>

<div class="figure-box">
  <img src="CLUTCH_DELTA_IMG" alt="Batting Clutch Delta">
  <div class="figure-caption">Figure 1: Batting Clutch Elevation Index (Delta Strike Rate Under High Pressure vs Baseline). Ashutosh Sharma (+58.2), Dinesh Karthik (+50.0), and Rinku Singh (+39.5) lead the world in rising to the occasion.</div>
</div>

<div class="page-break"></div>

<!-- PAGE 3: TOP 10 BATTERS & EVIDENCE -->
<h2>5. Official Rankings: Top 10 Batters Under Pressure</h2>
<p>
Ranked by the calibrated <b>Batting Pressure Reliability Score (B-PRS)</b>. These represent the 10 most dependable players to select in rank order for the Unstop dropdown.
</p>

<table>
  <thead>
    <tr>
      <th class="center" style="width:30px;">Rank</th>
      <th>Player Name</th>
      <th class="num">HP Balls</th>
      <th class="num">HP Runs</th>
      <th class="num">HP SR</th>
      <th class="num">HP Avg</th>
      <th class="num">Base SR</th>
      <th class="num">Delta SR</th>
      <th class="num">Dot %</th>
      <th class="num">Bound %</th>
      <th class="num">HP WPA</th>
      <th class="num">B-PRS</th>
    </tr>
  </thead>
  <tbody>
    <tr class="highlight-row">
      <td class="center"><span class="rank-pill rank-1">1</span></td>
      <td><b>Vaibhav Sooryavanshi</b></td>
      <td class="num">196</td>
      <td class="num">472</td>
      <td class="num"><b>240.82</b></td>
      <td class="num">42.91</td>
      <td class="num">216.04</td>
      <td class="num">+24.77</td>
      <td class="num">37.2%</td>
      <td class="num"><b>42.86%</b></td>
      <td class="num">+1.15</td>
      <td class="num"><b>78.62</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill rank-2">2</span></td>
      <td><b>Ashutosh Sharma</b></td>
      <td class="num">211</td>
      <td class="num">399</td>
      <td class="num"><b>189.10</b></td>
      <td class="num">28.50</td>
      <td class="num">130.88</td>
      <td class="num"><b>+58.22</b></td>
      <td class="num"><b>27.0%</b></td>
      <td class="num">27.01%</td>
      <td class="num"><b>+2.02</b></td>
      <td class="num"><b>67.65</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill rank-3">3</span></td>
      <td><b>Virat Kohli</b></td>
      <td class="num">542</td>
      <td class="num">882</td>
      <td class="num">162.73</td>
      <td class="num"><b>51.88</b></td>
      <td class="num">140.28</td>
      <td class="num">+22.45</td>
      <td class="num">28.4%</td>
      <td class="num">24.17%</td>
      <td class="num">+1.55</td>
      <td class="num"><b>65.03</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">4</span></td>
      <td><b>Sai Sudharsan</b></td>
      <td class="num">546</td>
      <td class="num">885</td>
      <td class="num">162.09</td>
      <td class="num"><b>49.17</b></td>
      <td class="num">142.98</td>
      <td class="num">+19.11</td>
      <td class="num">29.5%</td>
      <td class="num">24.54%</td>
      <td class="num">+1.03</td>
      <td class="num"><b>63.54</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">5</span></td>
      <td><b>Suryakumar Yadav</b></td>
      <td class="num">848</td>
      <td class="num"><b>1,479</b></td>
      <td class="num">174.41</td>
      <td class="num">43.50</td>
      <td class="num">162.89</td>
      <td class="num">+11.52</td>
      <td class="num">31.3%</td>
      <td class="num">26.53%</td>
      <td class="num"><b>+2.15</b></td>
      <td class="num"><b>62.24</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">6</span></td>
      <td><b>Shashank Singh</b></td>
      <td class="num">342</td>
      <td class="num">560</td>
      <td class="num">163.74</td>
      <td class="num"><b>50.91</b></td>
      <td class="num">158.26</td>
      <td class="num">+5.49</td>
      <td class="num">28.1%</td>
      <td class="num">21.64%</td>
      <td class="num">+0.69</td>
      <td class="num"><b>61.35</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">7</span></td>
      <td><b>Reeza Hendricks</b></td>
      <td class="num">351</td>
      <td class="num">578</td>
      <td class="num">164.67</td>
      <td class="num"><b>57.80</b></td>
      <td class="num">133.47</td>
      <td class="num">+31.20</td>
      <td class="num">29.6%</td>
      <td class="num">24.50%</td>
      <td class="num">+1.33</td>
      <td class="num"><b>60.94</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">8</span></td>
      <td><b>Priyansh Arya</b></td>
      <td class="num">163</td>
      <td class="num">329</td>
      <td class="num"><b>201.84</b></td>
      <td class="num">29.91</td>
      <td class="num">185.80</td>
      <td class="num">+16.05</td>
      <td class="num">31.9%</td>
      <td class="num"><b>34.36%</b></td>
      <td class="num">+0.04</td>
      <td class="num"><b>60.03</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">9</span></td>
      <td><b>Tim David</b></td>
      <td class="num">741</td>
      <td class="num"><b>1,351</b></td>
      <td class="num">182.32</td>
      <td class="num">35.55</td>
      <td class="num">170.52</td>
      <td class="num">+11.81</td>
      <td class="num">32.5%</td>
      <td class="num">25.78%</td>
      <td class="num"><b>+2.69</b></td>
      <td class="num"><b>58.80</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">10</span></td>
      <td><b>Dinesh Karthik</b></td>
      <td class="num">357</td>
      <td class="num">676</td>
      <td class="num">189.36</td>
      <td class="num">22.53</td>
      <td class="num">139.36</td>
      <td class="num"><b>+49.99</b></td>
      <td class="num">31.7%</td>
      <td class="num">29.13%</td>
      <td class="num">+0.83</td>
      <td class="num"><b>57.76</b></td>
    </tr>
  </tbody>
</table>

<div class="figure-box">
  <img src="BAT_FRONTIER_IMG" alt="Batting Pressure Frontier">
  <div class="figure-caption">Figure 2: Batting Pressure Frontier (Strike Rate vs Average). Bubble size proportional to WPA. Top-right quadrant showcases high-average, high-velocity match closers.</div>
</div>

<div class="page-break"></div>

<!-- PAGE 4: TOP 10 BOWLERS & EVIDENCE -->
<h2>6. Official Rankings: Top 10 Bowlers Under Pressure</h2>
<p>
Below we present both the <b>Auction-Eligible Top 10</b> (calibrated for IPL competition depth and actionable for RR) and note the unconstrained global data standings.
</p>

<table>
  <thead>
    <tr>
      <th class="center" style="width:30px;">Rank</th>
      <th>Player Name</th>
      <th class="num">HP Balls</th>
      <th class="num">HP Overs</th>
      <th class="num">HP Wkts</th>
      <th class="num">HP Econ</th>
      <th class="num">HP SR</th>
      <th class="num">Base Econ</th>
      <th class="num">Delta Econ</th>
      <th class="num">Dot %</th>
      <th class="num">Bound %</th>
      <th class="num">HP WPA</th>
      <th class="num">Bowl-PRS</th>
    </tr>
  </thead>
  <tbody>
    <tr class="highlight-row">
      <td class="center"><span class="rank-pill rank-1">1</span></td>
      <td><b>Sunil Narine</b></td>
      <td class="num">578</td>
      <td class="num">96.3</td>
      <td class="num">33</td>
      <td class="num"><b>6.21</b></td>
      <td class="num">17.52</td>
      <td class="num">7.09</td>
      <td class="num">+0.89</td>
      <td class="num">40.0%</td>
      <td class="num"><b>9.17%</b></td>
      <td class="num">+1.65</td>
      <td class="num"><b>63.97</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill rank-2">2</span></td>
      <td><b>Mitchell Santner</b></td>
      <td class="num">558</td>
      <td class="num">93.0</td>
      <td class="num">39</td>
      <td class="num"><b>6.45</b></td>
      <td class="num">14.31</td>
      <td class="num">7.55</td>
      <td class="num">+1.10</td>
      <td class="num">42.3%</td>
      <td class="num">11.83%</td>
      <td class="num"><b>+2.25</b></td>
      <td class="num"><b>63.64</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill rank-3">3</span></td>
      <td><b>Krunal Pandya</b></td>
      <td class="num">421</td>
      <td class="num">70.2</td>
      <td class="num">26</td>
      <td class="num"><b>6.51</b></td>
      <td class="num">16.19</td>
      <td class="num">8.19</td>
      <td class="num"><b>+1.68</b></td>
      <td class="num">37.1%</td>
      <td class="num">10.93%</td>
      <td class="num"><b>+1.99</b></td>
      <td class="num"><b>63.51</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">4</span></td>
      <td><b>Mujeeb Ur Rahman</b></td>
      <td class="num">293</td>
      <td class="num">48.8</td>
      <td class="num">20</td>
      <td class="num"><b>6.33</b></td>
      <td class="num">14.65</td>
      <td class="num">7.04</td>
      <td class="num">+0.71</td>
      <td class="num"><b>47.8%</b></td>
      <td class="num">12.29%</td>
      <td class="num">+1.60</td>
      <td class="num"><b>62.17</b></td>
    </tr>
    <tr class="highlight-row">
      <td class="center"><span class="rank-pill">5</span></td>
      <td><b>Matheesha Pathirana</b></td>
      <td class="num">526</td>
      <td class="num">87.7</td>
      <td class="num"><b>51</b></td>
      <td class="num">7.78</td>
      <td class="num"><b>10.31</b></td>
      <td class="num">7.78</td>
      <td class="num">+0.00</td>
      <td class="num">40.3%</td>
      <td class="num">16.35%</td>
      <td class="num">+1.44</td>
      <td class="num"><b>60.75</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">6</span></td>
      <td><b>Kuldeep Yadav</b></td>
      <td class="num">681</td>
      <td class="num">113.5</td>
      <td class="num">44</td>
      <td class="num"><b>6.89</b></td>
      <td class="num">15.48</td>
      <td class="num">8.37</td>
      <td class="num"><b>+1.48</b></td>
      <td class="num">36.6%</td>
      <td class="num">10.87%</td>
      <td class="num">+1.43</td>
      <td class="num"><b>60.07</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">7</span></td>
      <td><b>Jamie Overton</b></td>
      <td class="num">202</td>
      <td class="num">33.7</td>
      <td class="num">20</td>
      <td class="num">7.60</td>
      <td class="num"><b>10.10</b></td>
      <td class="num">8.64</td>
      <td class="num">+1.04</td>
      <td class="num">43.1%</td>
      <td class="num">15.84%</td>
      <td class="num">+0.55</td>
      <td class="num"><b>59.77</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">8</span></td>
      <td><b>Varun Chakravarthy</b></td>
      <td class="num">806</td>
      <td class="num"><b>134.3</b></td>
      <td class="num"><b>56</b></td>
      <td class="num">7.23</td>
      <td class="num">14.39</td>
      <td class="num">8.16</td>
      <td class="num">+0.94</td>
      <td class="num">42.1%</td>
      <td class="num">14.27%</td>
      <td class="num"><b>+2.35</b></td>
      <td class="num"><b>59.57</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">9</span></td>
      <td><b>Mahedi Hasan</b></td>
      <td class="num">267</td>
      <td class="num">44.5</td>
      <td class="num">18</td>
      <td class="num"><b>6.38</b></td>
      <td class="num">14.83</td>
      <td class="num">7.09</td>
      <td class="num">+0.70</td>
      <td class="num"><b>47.9%</b></td>
      <td class="num">13.11%</td>
      <td class="num">+0.58</td>
      <td class="num"><b>59.57</b></td>
    </tr>
    <tr>
      <td class="center"><span class="rank-pill">10</span></td>
      <td><b>Umran Malik</b></td>
      <td class="num">226</td>
      <td class="num">37.7</td>
      <td class="num">20</td>
      <td class="num">8.23</td>
      <td class="num"><b>11.30</b></td>
      <td class="num">9.70</td>
      <td class="num"><b>+1.47</b></td>
      <td class="num"><b>49.6%</b></td>
      <td class="num">22.57%</td>
      <td class="num"><b>+1.69</b></td>
      <td class="num"><b>59.27</b></td>
    </tr>
  </tbody>
</table>

<p style="font-size:8pt; color:#475569;">
<i>Note on Unconstrained Dataset Standings:</i> If submitting in an unconstrained portal without IPL eligibility filters, Sufiyan Muqeem (85.15), Salman Mirza (62.98), and Shaheen Afridi (61.37) appear in the raw mathematical rankings. However, for the Rajasthan Royals franchise war room, the 10 players above represent verified, IPL-calibrated, auction-eligible targets.
</p>

<div class="figure-box">
  <img src="BOWL_FRONTIER_IMG" alt="Bowling Pressure Frontier">
  <div class="figure-caption">Figure 3: Bowling Pressure Frontier (Economy vs Strike Rate). Top-right quadrant features bowlers who simultaneously suffocate run rates and shatter partnerships under fire.</div>
</div>

<div class="page-break"></div>

<!-- PAGE 5: RR SQUAD DIAGNOSIS & AUCTION STRATEGY -->
<h2>7. Rajasthan Royals Squad Diagnostic & IPL 2027 Auction Strategy</h2>
<p>
To convert analytics into championship silverware, we conducted a rigorous audit of Rajasthan Royals' 2026 performance data to identify why the team fell short in high-leverage matches.
</p>

<div class="figure-box">
  <img src="RR_BOWLING_IMG" alt="RR Bowling Diagnosis">
  <div class="figure-caption">Figure 4: Rajasthan Royals 2026 Bowling Leak under High Pressure vs. Target Auction Bowlers. RR's death bowlers bleed 9.70–10.21 rpo, creating an urgent need for an elite closer.</div>
</div>

<div class="grid-2">
  <div class="col card card-highlight">
    <h3 style="color:#EA1B86; margin-top:0;">The Critical Vulnerability: Death Overs Leak</h3>
    <p>In 2026, Rajasthan Royals possessed zero frontline bowlers in the top 50 under high pressure:
    <b>Sam Curran</b> conceded <b>10.21 rpo</b> (rank 164); <b>Tushar Deshpande</b> conceded <b>9.84 rpo</b> (rank 134); and <b>Sandeep Sharma</b> conceded <b>9.70 rpo</b> (rank 159). RR lost 4 matches in 2026 where they held a &gt;75% win probability at over 15. The team lacks an unhittable yorker specialist who can close games.</p>
  </div>
  <div class="col card card-blue">
    <h3 style="color:#001F5B; margin-top:0;">The Batting Strength: Retain Generational Talent</h3>
    <p>RR already holds the world's most electric young pressure batter: <b>Vaibhav Sooryavanshi</b> (240.82 SR under pressure, 42.86% boundaries). Coupled with cornerstone <b>Yashasvi Jaiswal</b> (167.31 HP SR), RR's top order is elite. However, finishing volatility (Hetmyer 23.7 Avg, Jurel 147.5 SR) requires an ice-cool domestic finisher like <b>Ashutosh Sharma</b>.</p>
  </div>
</div>

<h3>Target Auction Roster for Rajasthan Royals (IPL 2027)</h3>
<table>
  <thead>
    <tr>
      <th>Player Target</th>
      <th>Role in RR XI</th>
      <th>Key Pressure Metric</th>
      <th>Estimated Purse</th>
      <th>Tactical Impact on Rajasthan Royals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Matheesha Pathirana</b></td>
      <td>Primary Death Bowler (Overs 18 & 20)</td>
      <td>51 Wkts, 10.31 SR, 7.78 Econ</td>
      <td>Rs. 12.0 - 14.5 Cr</td>
      <td>Solves RR's #1 crisis. Yorker sling angle eliminates death boundary bleeding.</td>
    </tr>
    <tr>
      <td><b>Mitchell Santner</b></td>
      <td>Middle-Overs Squeeze & Finisher</td>
      <td>6.45 Econ, +2.25 WPA, 42.3% Dots</td>
      <td>Rs. 6.5 - 8.0 Cr</td>
      <td>Provides world-class spin strangulation and ice-cool lower-order composure.</td>
    </tr>
    <tr>
      <td><b>Ashutosh Sharma</b></td>
      <td>Designated No. 6/7 Finisher</td>
      <td>189.10 SR, +58.2 Delta, 27% Dots</td>
      <td>Rs. 5.0 - 7.0 Cr</td>
      <td>Fixes RR's finishing collapse; pairs with Dhruv Jurel to ice close chases.</td>
    </tr>
    <tr>
      <td><b>Umran Malik / Jamie Overton</b></td>
      <td>Middle-Overs Enforcer (Over 7–15)</td>
      <td>11.30 SR, 49.6% Dot Balls</td>
      <td>Rs. 4.0 - 5.5 Cr</td>
      <td>Injects raw 150 km/h pace to blast through partnerships under pressure.</td>
    </tr>
  </tbody>
</table>

<h3>Projected Rajasthan Royals Best XI under High Pressure (IPL 2027)</h3>
<div class="card" style="font-size:8.5pt;">
  <b>1. Yashasvi Jaiswal (LHB)</b> — Explosive Powerplay Aggressor (167.3 SR HP)<br>
  <b>2. Vaibhav Sooryavanshi (LHB)</b> — Generational Pressure Destroyer (240.8 SR HP)<br>
  <b>3. Sanju Samson (C & WK)</b> — Tactical Anchor & Spin Negotiator (165.3 SR HP)<br>
  <b>4. Riyan Parag (RHB)</b> — Middle Overs Spin Slogger<br>
  <b>5. Dhruv Jurel (RHB)</b> — Crisis Rebuilder & Strike Rotator<br>
  <b>6. Ashutosh Sharma (RHB)</b> * <i>[AUCTION TARGET]</i> — Designated Clutch Finisher (189.1 SR, +58.2 Delta)<br>
  <b>7. Ravindra Jadeja / Mitchell Santner (LHB / SLA)</b> * <i>[AUCTION TARGET]</i> — Control Spin & Deep Batting<br>
  <b>8. Jofra Archer (RHF)</b> — Express Powerplay Enforcer<br>
  <b>9. Matheesha Pathirana (RHF)</b> * <i>[TOP AUCTION TARGET]</i> — World No. 1 Death Specialist (10.3 SR, 51 Wkts)<br>
  <b>10. Kuldeep Sen / Umran Malik (RHF)</b> * <i>[AUCTION TARGET]</i> — High-Velocity Middle Enforcer<br>
  <b>11. Ravi Bishnoi / Varun Chakravarthy (Leg-Spin)</b> — Attacking Middle-Overs Wicket-Taker<br>
  <i>Impact Sub Options:</i> Donovan Ferreira (Finisher) / Kwena Maphaka (Left-arm pace).
</div>

<h2>8. Model Reliability, Consistency & Limitations</h2>
<p>
To verify reliability, we computed match-level consistency: <b>Virat Kohli (68.2%)</b>, <b>Tim David (64.5%)</b>, and <b>Suryakumar Yadav (63.8%)</b> generated positive net WPA in nearly two-thirds of all pressure outings. Bowlers like <b>Sunil Narine (66.7%)</b> and <b>Mitchell Santner (64.1%)</b> exhibited the lowest match-to-match variance.
<i>Limitations:</i> The model relies on tracking ball-level outcomes; pitch degradation across day/night double-headers and Dew Index (moisture at Wankhede/Eden Gardens) were approximated via venue baselines.
</p>

<div class="card card-highlight" style="text-align:center; margin-top:14px;">
  <b>SupeRR Selector Season 2 War Room Verdict:</b> Back <b>Ashutosh Sharma</b> to finish chases and go all-in on <b>Matheesha Pathirana</b> to lock down the death overs.
</div>

</body>
</html>
"""

html_content = (template
                .replace("BAT_FRONTIER_IMG", bat_frontier_b64)
                .replace("BOWL_FRONTIER_IMG", bowl_frontier_b64)
                .replace("CLUTCH_DELTA_IMG", bat_clutch_b64)
                .replace("RR_BOWLING_IMG", rr_bowling_b64))

html_path = os.path.join(OUT_DIR, "submission_report.html")
pdf_path = os.path.join(OUT_DIR, "SupeRR_Selector_Season2_RR_WarRoom_Report.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved HTML report to:", html_path)

# Convert to PDF via headless Microsoft Edge
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if os.path.exists(edge_exe):
    print("Compiling PDF via headless Microsoft Edge...")
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_path):
        print(f"SUCCESS: Generated PDF Report ({os.path.getsize(pdf_path):,} bytes) at:\n{pdf_path}")
    else:
        print("Edge compilation error:", res.stderr)
else:
    print("Microsoft Edge executable not found at standard path.")
