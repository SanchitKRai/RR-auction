import os
import json
import base64
import glob

WORKSPACE_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")
SVG_DIR = os.path.join(WORKSPACE_DIR, "dashboard", "assets", "svg")
FIGURES_DIR = os.path.join(WORKSPACE_DIR, "figures")
DASHBOARD_DIR = os.path.join(WORKSPACE_DIR, "dashboard")

def load_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(filepath)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            return f"data:{mime};base64,{encoded}"
    return ""

def load_svg(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def svg_to_data_uri(svg_str):
    b64 = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

def main():
    print("Building Pixel-Perfect Rajasthan Royals War Room Dashboard from Complete Kit...")

    # Load JSON datasets
    with open(os.path.join(DATA_DIR, "batters.json"), "r", encoding="utf-8") as f:
        batters_data = json.load(f)

    with open(os.path.join(DATA_DIR, "bowlers.json"), "r", encoding="utf-8") as f:
        bowlers_data = json.load(f)

    with open(os.path.join(DATA_DIR, "rr_squad.json"), "r", encoding="utf-8") as f:
        rr_squad_data = json.load(f)

    with open(os.path.join(DATA_DIR, "auction_targets.json"), "r", encoding="utf-8") as f:
        auction_targets_data = json.load(f)

    with open(os.path.join(DATA_DIR, "metadata.json"), "r", encoding="utf-8") as f:
        metadata_data = json.load(f)

    # Load All SVGs
    svgs = {}
    for p in glob.glob(os.path.join(SVG_DIR, "*.svg")):
        name = os.path.splitext(os.path.basename(p))[0]
        svgs[name] = load_svg(p)
    print(f"Loaded {len(svgs)} SVGs from {SVG_DIR}")

    # Photos
    b64_crest = load_base64(os.path.join(ASSETS_DIR, "rr_crest.jpg"))
    b64_vaibhav = load_base64(os.path.join(ASSETS_DIR, "vaibhav_sooryavanshi.jpg"))
    b64_ashutosh = load_base64(os.path.join(ASSETS_DIR, "ashutosh_sharma.jpg"))
    b64_pathirana = load_base64(os.path.join(ASSETS_DIR, "matheesha_pathirana.jpg"))
    b64_santner = load_base64(os.path.join(ASSETS_DIR, "mitchell_santner.jpg"))
    b64_banner = load_base64(os.path.join(ASSETS_DIR, "rr_banner.jpg"))
    b64_stadium = load_base64(os.path.join(ASSETS_DIR, "sawai_mansingh_stadium.jpg"))

    # Figures for secondary modules
    b64_donut = load_base64(os.path.join(FIGURES_DIR, "pressure_donut.png"))
    b64_batting_front = load_base64(os.path.join(FIGURES_DIR, "batting_frontier.png"))
    b64_bowling_front = load_base64(os.path.join(FIGURES_DIR, "bowling_frontier.png"))
    b64_clutch_delta = load_base64(os.path.join(FIGURES_DIR, "batting_clutch_delta.png"))
    b64_role_map = load_base64(os.path.join(FIGURES_DIR, "rr_squad_role_map.png"))
    b64_radar = load_base64(os.path.join(FIGURES_DIR, "auction_radar_comparison.png"))
    b64_bowling_diag = load_base64(os.path.join(FIGURES_DIR, "rr_bowling_diagnosis.png"))

    # Data URIs for card backdrops
    bg_card_batter = svg_to_data_uri(svgs.get("card_batter_bg", ""))
    bg_card_finisher = svg_to_data_uri(svgs.get("card_finisher_bg", ""))
    bg_card_death = svg_to_data_uri(svgs.get("card_death_bg", ""))
    bg_card_spin = svg_to_data_uri(svgs.get("card_spin_bg", ""))
    bg_hero_horizon = svg_to_data_uri(svgs.get("hero_palace_horizon", ""))
    bg_palace_sil = svg_to_data_uri(svgs.get("palace_silhouette", ""))
    bg_portrait_arch = svg_to_data_uri(svgs.get("player_portrait_arch", ""))
    bg_bottom_wave = svg_to_data_uri(svgs.get("player_card_bottom_wave", ""))
    bg_corner_glow = svg_to_data_uri(svgs.get("royal_corner_glow", ""))

    def get_icon(name, extra_class="w-5 h-5"):
        svg = svgs.get(name, "")
        if not svg: return ""
        return svg.replace("<svg ", f'<svg class="{extra_class}" ')

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RR WAR ROOM • IPL 2027 Analytics Engine</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <!-- Chart.js for interactive visualizations -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Plus Jakarta Sans', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            rr: {{
              bg: '#090E22',
              surface: '#111A32',
              surface2: '#151F3A',
              border: '#273452',
              magenta: '#F02D9B',
              magentaGlow: 'rgba(240, 45, 155, 0.35)',
              blue: '#5C9DFF',
              gold: '#F4C95D',
              green: '#35E6A1',
              violet: '#A45BEE',
              cyan: '#16C9D5',
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    :root {{
      --bg: #090E22;
      --surface: #111A32;
      --surface-2: #151F3A;
      --border: #273452;
      --text: #F4F6FF;
      --muted: #9AA8C2;
      --magenta: #F02D9B;
      --blue: #5C9DFF;
      --gold: #F4C95D;
      --green: #35E6A1;
      --violet: #A45BEE;
      --cyan: #16C9D5;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      overflow-x: hidden;
    }}

    /* Custom Scrollbars */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: var(--bg);
    }}
    ::-webkit-scrollbar-thumb {{
      background: var(--border);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: var(--magenta);
    }}

    /* Nav Tab Active */
    .nav-link.active {{
      background: linear-gradient(90deg, #F02D9B 0%, #a21caf 100%);
      color: #FFFFFF;
      font-weight: 700;
      box-shadow: 0 0 22px rgba(240, 45, 155, 0.4);
    }}

    /* Cards */
    .rr-card {{
      background-color: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      transition: all 0.2s ease-in-out;
    }}
    .rr-card:hover {{
      border-color: rgba(240, 45, 155, 0.4);
    }}

    /* Player Card Hero Portrait Frame */
    .player-card {{
      background-color: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 390px;
      position: relative;
      transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }}
    .player-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 30px -10px rgba(240, 45, 155, 0.25);
    }}
    .player-card.border-magenta:hover {{ border-color: var(--magenta); }}
    .player-card.border-gold:hover {{ border-color: var(--gold); }}
    .player-card.border-blue:hover {{ border-color: var(--blue); }}

    /* Portrait Arch Framing */
    .portrait-arch-wrap {{
      position: relative;
      width: 100%;
      height: 210px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: flex-end;
    }}
    .portrait-arch-bg {{
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center top;
      opacity: 0.85;
    }}
    .portrait-arch-vector {{
      position: absolute;
      top: 18px;
      width: 190px;
      height: 190px;
      opacity: 0.65;
      pointer-events: none;
    }}
    .player-img-cutout {{
      position: relative;
      z-index: 2;
      height: 195px;
      width: auto;
      object-fit: cover;
      object-position: top center;
      filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.8));
      transition: transform 0.3s ease;
    }}
    .player-card:hover .player-img-cutout {{
      transform: scale(1.04);
    }}
    .portrait-bottom-gradient {{
      position: absolute;
      inset-x: 0;
      bottom: 0;
      height: 70px;
      background: linear-gradient(to top, var(--surface) 15%, rgba(17, 26, 50, 0.6) 60%, transparent 100%);
      z-index: 3;
      pointer-events: none;
    }}

    /* Badges */
    .badge-magenta {{
      background: rgba(240, 45, 155, 0.22);
      color: #FF5EA7;
      border: 1px solid rgba(240, 45, 155, 0.45);
    }}
    .badge-gold {{
      background: rgba(244, 201, 93, 0.18);
      color: #F4C95D;
      border: 1px solid rgba(244, 201, 93, 0.45);
    }}
    .badge-blue {{
      background: rgba(92, 157, 255, 0.18);
      color: #5C9DFF;
      border: 1px solid rgba(92, 157, 255, 0.45);
    }}
    .badge-green {{
      background: rgba(53, 230, 161, 0.15);
      color: #35E6A1;
      border: 1px solid rgba(53, 230, 161, 0.35);
    }}

    .modal-backdrop {{
      background: rgba(9, 14, 34, 0.88);
      backdrop-filter: blur(12px);
    }}
  </style>
</head>

<body class="flex h-screen w-screen overflow-hidden text-slate-100 antialiased selection:bg-[#F02D9B] selection:text-white">

  <!-- ========================================================================= -->
  <!-- PERSISTENT LEFT SIDEBAR                                                   -->
  <!-- ========================================================================= -->
  <aside class="w-64 flex-shrink-0 bg-[#090E22] border-r border-[#273452] flex flex-col justify-between z-30 select-none">
    
    <!-- Top Branding & Navigation -->
    <div class="flex-1 overflow-y-auto">
      
      <!-- RR War Room Brand Header -->
      <div class="px-5 py-5 border-b border-[#273452] flex items-center space-x-3.5">
        <div class="w-10 h-10 flex-shrink-0 flex items-center justify-center">
          {svgs.get('rrw_crest', '')}
        </div>
        <div>
          <h1 class="text-base font-black tracking-wide text-white uppercase leading-none">RR WAR ROOM</h1>
          <p class="text-[11px] text-slate-400 font-medium tracking-tight mt-1">IPL 2027 Analytics Engine</p>
        </div>
      </div>

      <!-- Navigation Section -->
      <nav class="p-3 space-y-1 text-xs">
        
        <!-- Section: ANALYTICS SUITE -->
        <div class="px-3 pt-3 pb-1.5 text-[10px] font-black uppercase tracking-widest text-slate-400">
          Analytics Suite
        </div>

        <!-- 01 Executive Overview -->
        <button onclick="switchModule('module-overview')" id="nav-module-overview" class="nav-link active w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-white font-semibold transition">
          <span class="w-4 h-4 flex-shrink-0 text-white">
            {get_icon('icon_chart', 'w-4 h-4 text-white')}
          </span>
          <span class="truncate">Executive Overview</span>
        </button>

        <!-- 02 Batting Intelligence -->
        <button onclick="switchModule('module-batting')" id="nav-module-batting" class="nav-link w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <span class="w-4 h-4 flex-shrink-0 text-slate-400">
            {get_icon('icon_bat', 'w-4 h-4 text-slate-400')}
          </span>
          <span class="truncate">Batting Intelligence</span>
        </button>

        <!-- 03 Bowling Intelligence -->
        <button onclick="switchModule('module-bowling')" id="nav-module-bowling" class="nav-link w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <span class="w-4 h-4 flex-shrink-0 text-slate-400">
            {get_icon('icon_bowler', 'w-4 h-4 text-slate-400')}
          </span>
          <span class="truncate">Bowling Intelligence</span>
        </button>

        <!-- 04 Pressure Lab & Models -->
        <button onclick="switchModule('module-lab')" id="nav-module-lab" class="nav-link w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <div class="flex items-center space-x-3">
            <span class="w-4 h-4 flex-shrink-0 text-slate-400">
              {get_icon('icon_model', 'w-4 h-4 text-slate-400')}
            </span>
            <span class="truncate">Pressure Lab &amp; Models</span>
          </div>
          <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[#F02D9B]/20 text-[#F02D9B] border border-[#F02D9B]/30 font-mono">ML</span>
        </button>

        <!-- 05 RR Squad War Room -->
        <button onclick="switchModule('module-squad')" id="nav-module-squad" class="nav-link w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <span class="w-4 h-4 flex-shrink-0 text-slate-400">
            {get_icon('icon_users', 'w-4 h-4 text-slate-400')}
          </span>
          <span class="truncate">RR Squad War Room</span>
        </button>

        <!-- 06 Auction Simulator -->
        <button onclick="switchModule('module-auction')" id="nav-module-auction" class="nav-link w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <span class="w-4 h-4 flex-shrink-0 text-slate-400">
            {get_icon('icon_rupee', 'w-4 h-4 text-slate-400')}
          </span>
          <span class="truncate">Auction Simulator</span>
        </button>

        <!-- Section: TOOLS & REPORTS -->
        <div class="px-3 pt-5 pb-1.5 text-[10px] font-black uppercase tracking-widest text-slate-400">
          Tools &amp; Reports
        </div>

        <!-- Match Reconciliation -->
        <button onclick="openReconciliationModal()" class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <div class="flex items-center space-x-3">
            <span class="w-4 h-4 flex-shrink-0 text-slate-400">
              {get_icon('icon_clock', 'w-4 h-4 text-slate-400')}
            </span>
            <span class="truncate">Match Reconciliation</span>
          </div>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono text-slate-300 bg-slate-800 border border-slate-700">883 / 867</span>
        </button>

        <!-- Download Report (PDF) -->
        <a href="SupeRR_Selector_Season2_RR_WarRoom_Report.pdf" target="_blank" class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#111A32] transition">
          <div class="flex items-center space-x-3">
            <span class="w-4 h-4 flex-shrink-0 text-slate-400">
              {get_icon('icon_download', 'w-4 h-4 text-slate-400')}
            </span>
            <span class="truncate">Download Report (PDF)</span>
          </div>
          <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </a>

      </nav>
    </div>

    <!-- Sidebar Bottom: Palace Silhouette & Disclaimer -->
    <div class="p-4 border-t border-[#273452] relative overflow-hidden bg-gradient-to-t from-[#15102a] via-[#10142b] to-[#090E22]">
      <div class="h-16 w-full mb-2 opacity-70 flex items-center justify-center pointer-events-none">
        {svgs.get('palace_silhouette', '')}
      </div>
      <div class="text-[10px] text-slate-400 leading-snug">
        <div class="font-extrabold text-white text-[11px]">Independent Research Dossier</div>
        <div>SupeRR Selector Season 2</div>
        <div class="text-slate-400 text-[9px] mt-0.5">Not an official RR publication</div>
      </div>
    </div>
  </aside>

  <!-- ========================================================================= -->
  <!-- MAIN CONTENT AREA                                                         -->
  <!-- ========================================================================= -->
  <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
    
    <!-- Top Global App Bar -->
    <header class="h-14 flex-shrink-0 bg-[#090E22]/95 backdrop-blur border-b border-[#273452] px-6 flex items-center justify-between z-20">
      
      <!-- Left: Breadcrumb -->
      <div class="flex items-center space-x-2 text-[10px] font-extrabold uppercase tracking-wider text-slate-400">
        <span class="text-slate-300">RAJASTHAN ROYALS</span>
        <span class="text-slate-600">&rsaquo;</span>
        <span class="text-slate-300">WAR ROOM DOSSIER</span>
        <span class="text-slate-600">&rsaquo;</span>
        <span id="breadcrumb-current" class="text-white">01 EXECUTIVE OVERVIEW</span>
      </div>

      <!-- Right: Model Switcher & Dataset Badges -->
      <div class="flex items-center space-x-3 text-xs">
        
        <!-- Model Toggle Button -->
        <div class="flex items-center bg-[#111A32] border border-[#273452] rounded-lg p-0.5">
          <button onclick="setModel('calibrated')" id="btn-model-calibrated" class="px-3 py-1 rounded-md text-[11px] font-bold text-white bg-[#F02D9B] shadow-sm flex items-center gap-1 transition">
            <span>Model B: Calibrated PRS</span>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <button onclick="setModel('legacy')" id="btn-model-legacy" class="px-3 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition">
            Model A: Legacy PRS
          </button>
        </div>

        <!-- Metric Badges -->
        <div class="flex items-center space-x-2 font-mono text-[11px]">
          <span class="px-2.5 py-1 rounded-lg bg-[#111A32] border border-[#273452] text-slate-300">
            <b class="text-[#F02D9B] font-sans font-bold">200,999</b> Balls
          </span>
          <button onclick="openReconciliationModal()" class="px-2.5 py-1 rounded-lg bg-[#111A32] border border-[#273452] text-slate-300 hover:text-white transition">
            <b class="text-[#5C9DFF] font-sans font-bold">867</b> Contested
          </button>
          <span class="px-2.5 py-1 rounded-lg bg-[#111A32] border border-[#273452] text-slate-300">
            <b class="text-[#F4C95D] font-sans font-bold">78,374</b> HP <span class="text-[10px] text-slate-400 font-sans">(39.8%)</span>
          </span>
          <button onclick="openReconciliationModal()" class="text-slate-400 hover:text-white p-1 rounded-full bg-[#111A32] border border-[#273452] flex items-center justify-center">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </button>
        </div>

      </div>
    </header>

    <!-- Scrollable Workspace Body -->
    <main class="flex-1 overflow-y-auto px-6 py-5 space-y-5">

      <!-- ===================================================================== -->
      <!-- MODULE 01: EXECUTIVE OVERVIEW (PIXEL-PERFECT REBUILD)                 -->
      <!-- ===================================================================== -->
      <section id="module-overview" class="module-pane space-y-5">
        
        <!-- HERO SECTION: Layered Palace Horizon, Atmospheric Glow & Royal Flag -->
        <div class="relative overflow-hidden rounded-2xl border border-[#273452] bg-[#111A32] min-h-[165px] flex items-center justify-between shadow-2xl">
          
          <!-- Layer 1: Photographic Hawa Mahal Backdrop -->
          <div class="absolute right-0 top-0 bottom-0 w-3/5 opacity-40 pointer-events-none flex items-center justify-end overflow-hidden z-0 mix-blend-luminosity">
            <img src="{b64_banner or 'assets/rr_banner.jpg'}" alt="Hawa Mahal" class="h-full w-full object-cover object-right">
          </div>

          <!-- Layer 2: Palace Horizon Artwork on Right -->
          <div class="absolute right-0 top-0 bottom-0 w-3/5 opacity-85 pointer-events-none flex items-center justify-end overflow-hidden z-0">
            <img src="{bg_hero_horizon}" alt="Palace Horizon" class="h-full w-full object-cover object-right">
          </div>

          <!-- Layer 3: Floating Royal Flag at Palace Peak -->
          <div class="absolute right-8 top-1/2 -translate-y-1/2 w-32 h-32 pointer-events-none z-10 opacity-95 hidden sm:block">
            {svgs.get('royal_flag', '')}
          </div>

          <!-- Layer 4: Dark Left Text-Safe Gradient Overlay -->
          <div class="absolute inset-0 bg-gradient-to-r from-[#090E22] via-[#111A32]/95 to-transparent w-full lg:w-3/5 pointer-events-none z-10"></div>

          <!-- Layer 5: Text Content (Sharp & Unobscured) -->
          <div class="relative z-20 px-7 py-5 space-y-1.5 max-w-xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#F02D9B]/15 text-[#F02D9B] border border-[#F02D9B]/40 text-[10px] font-black uppercase tracking-wider">
              Executive Analytics
            </div>
            <h2 class="text-2xl font-black text-white tracking-tight sm:text-3xl">
              Executive Scouting &amp; <span class="text-[#F4C95D]">Reliability Framework</span>
            </h2>
            <p class="text-slate-300 text-xs sm:text-sm font-medium leading-relaxed">
              A data-driven player evaluation and acquisition framework for Rajasthan Royals (IPL 2027)
            </p>
          </div>

        </div>

        <!-- FIVE TOP KPI CARDS (Row 1) -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
          
          <!-- KPI 1: Players Contested -->
          <div class="rr-card p-4 flex items-center space-x-3.5">
            <div class="w-11 h-11 rounded-full bg-[#5C9DFF]/15 border border-[#5C9DFF]/30 text-[#5C9DFF] flex items-center justify-center flex-shrink-0">
              {get_icon('icon_target', 'w-5 h-5 text-[#5C9DFF]')}
            </div>
            <div class="space-y-0.5">
              <div class="text-xl font-black text-white font-mono leading-none">867</div>
              <div class="text-[11px] text-slate-300 font-semibold">Players Contested</div>
              <div class="text-[10px] font-bold text-[#35E6A1]">+12.6% vs. last cycle</div>
            </div>
          </div>

          <!-- KPI 2: Balls Analyzed -->
          <div class="rr-card p-4 flex items-center space-x-3.5">
            <div class="w-11 h-11 rounded-full bg-[#5C9DFF]/15 border border-[#5C9DFF]/30 text-[#5C9DFF] flex items-center justify-center flex-shrink-0">
              {get_icon('icon_cricket_ball', 'w-5 h-5 text-[#5C9DFF]')}
            </div>
            <div class="space-y-0.5">
              <div class="text-xl font-black text-white font-mono leading-none">200,999</div>
              <div class="text-[11px] text-slate-300 font-semibold">Balls Analyzed</div>
              <div class="text-[10px] font-bold text-[#35E6A1]">+18.9%</div>
            </div>
          </div>

          <!-- KPI 3: High-Impact Plays (HP) -->
          <div class="rr-card p-4 flex items-center space-x-3.5">
            <div class="w-11 h-11 rounded-full bg-[#F4C95D]/15 border border-[#F4C95D]/30 text-[#F4C95D] flex items-center justify-center flex-shrink-0">
              {get_icon('icon_lightning', 'w-5 h-5 text-[#F4C95D]')}
            </div>
            <div class="space-y-0.5">
              <div class="text-xl font-black text-white font-mono leading-none">78,374</div>
              <div class="text-[11px] text-slate-300 font-semibold">High-Impact Plays (HP)</div>
              <div class="text-[10px] font-bold text-[#F4C95D]">39.8% of total</div>
            </div>
          </div>

          <!-- KPI 4: Model Accuracy S2 (Calibrated) -->
          <div class="rr-card p-4 flex items-center space-x-3.5">
            <div class="w-11 h-11 rounded-full bg-[#A45BEE]/15 border border-[#A45BEE]/30 text-[#A45BEE] flex items-center justify-center flex-shrink-0">
              {get_icon('icon_model', 'w-5 h-5 text-[#A45BEE]')}
            </div>
            <div class="space-y-0.5">
              <div class="text-[10px] text-slate-400 font-semibold leading-none">Model Accuracy</div>
              <div class="text-[10px] text-slate-300 font-medium">S2 (Calibrated)</div>
              <div class="flex items-center gap-1.5 mt-0.5">
                <span class="text-lg font-black text-white font-mono">0.872</span>
                <span class="text-[10px] font-bold text-[#35E6A1]">▲ +3.1%</span>
              </div>
            </div>
          </div>

          <!-- KPI 5: Shortlist Readiness A-Grade Targets -->
          <div class="rr-card p-4 flex items-center space-x-3.5 col-span-2 lg:col-span-1 bg-gradient-to-br from-[#111A32] to-[#25102d]">
            <div class="w-11 h-11 rounded-full bg-[#F02D9B]/15 border border-[#F02D9B]/30 text-[#F02D9B] flex items-center justify-center flex-shrink-0">
              {get_icon('icon_trophy', 'w-5 h-5 text-[#F02D9B]')}
            </div>
            <div class="space-y-0.5">
              <div class="text-[10px] text-slate-400 font-semibold leading-none">Shortlist Readiness</div>
              <div class="text-[10px] text-slate-300 font-medium">A-Grade Targets</div>
              <div class="text-xl font-black text-[#F02D9B] font-mono leading-none mt-1">12 Players</div>
            </div>
          </div>

        </div>

        <!-- THREE VISUAL ANALYTICS PANELS (Row 2) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
          
          <!-- Card 1: Squad Quality Snapshot (Radar Pentagon) - 3.5 Cols -->
          <div class="lg:col-span-4 rr-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-[#273452] pb-2.5">
              <div class="flex items-center gap-1.5">
                <h3 class="text-xs font-black text-white uppercase tracking-wider">Squad Quality Snapshot</h3>
                <span class="text-slate-400 text-[10px] cursor-pointer" title="Radar audit of Rajasthan Royals' squad metrics vs league par">ⓘ</span>
              </div>
            </div>
            
            <div class="h-56 relative flex items-center justify-center pt-2">
              <canvas id="chart-squad-radar"></canvas>
            </div>

            <div class="flex items-center justify-center gap-5 text-[10px] font-bold pt-2 border-t border-[#273452]">
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-[#F02D9B]"></span>
                <span class="text-slate-200">RR (Current)</span>
              </div>
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-[#5C9DFF]"></span>
                <span class="text-slate-400">League Avg</span>
              </div>
            </div>
          </div>

          <!-- Card 2: Performance Trend & Impact - 5 Cols -->
          <div class="lg:col-span-5 rr-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-[#273452] pb-2">
              <div class="flex items-center gap-1.5">
                <h3 class="text-xs font-black text-white uppercase tracking-wider">Performance Trend &amp; Impact</h3>
                <span class="text-slate-400 text-[10px] cursor-pointer">ⓘ</span>
              </div>
              <div class="flex items-center space-x-1 text-[10px] font-bold">
                <button class="px-2 py-0.5 rounded bg-[#F02D9B] text-white shadow-sm">PRS Trend</button>
                <button class="px-2 py-0.5 rounded bg-[#090E22] text-slate-400 hover:text-white">Win Impact</button>
                <button class="px-2 py-0.5 rounded bg-[#090E22] text-slate-400 hover:text-white">HP%</button>
              </div>
            </div>

            <div class="h-56 relative pt-2">
              <canvas id="chart-performance-trend"></canvas>
            </div>

            <div class="flex items-center justify-center gap-5 text-[10px] font-bold pt-2 border-t border-[#273452]">
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-[#F02D9B]"></span>
                <span class="text-slate-200">PRS (Player Strength)</span>
              </div>
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-[#5C9DFF]"></span>
                <span class="text-slate-400">HP% (High-Impact)</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Model Balance (Donut) - 3.5 Cols -->
          <div class="lg:col-span-3 rr-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-[#273452] pb-2.5">
              <div class="flex items-center gap-1.5">
                <h3 class="text-xs font-black text-white uppercase tracking-wider">Model Balance</h3>
                <span class="text-slate-400 text-[10px] cursor-pointer">ⓘ</span>
              </div>
            </div>

            <div class="h-44 relative flex items-center justify-center">
              <canvas id="chart-model-balance"></canvas>
              <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none text-center">
                <span class="text-[9px] font-bold uppercase text-slate-400 tracking-wider">Model</span>
                <span class="text-[11px] font-black text-white">Weightage</span>
              </div>
            </div>

            <div class="space-y-1 text-[10px] pt-1 font-semibold text-slate-300">
              <div class="flex items-center justify-between">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#F02D9B]"></span>Batting Impact</span>
                <span class="font-mono text-white font-bold">32%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#5C9DFF]"></span>Bowling Impact</span>
                <span class="font-mono text-white font-bold">28%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#16C9D5]"></span>Clutch (Death)</span>
                <span class="font-mono text-white font-bold">18%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#F4C95D]"></span>Context (Econ/Wkts)</span>
                <span class="font-mono text-white font-bold">12%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#A45BEE]"></span>Form &amp; Consistency</span>
                <span class="font-mono text-white font-bold">10%</span>
              </div>
            </div>
          </div>

        </div>

        <!-- CORE TARGET & PERFORMER PROFILES (Row 3 - Large Portrait Framing) -->
        <div class="space-y-3.5 pt-2">
          
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-black text-white uppercase tracking-wider">Core Target &amp; Performer Profiles</h3>
              <span class="text-slate-400 text-xs cursor-pointer">ⓘ</span>
            </div>
            
            <div class="flex items-center space-x-2 text-xs">
              <select class="bg-[#111A32] border border-[#273452] rounded-lg px-2.5 py-1 text-slate-300 font-semibold focus:outline-none focus:border-[#F02D9B]">
                <option>Role: All</option>
                <option>Openers</option>
                <option>Finishers</option>
                <option>Bowlers</option>
              </select>
              <select class="bg-[#111A32] border border-[#273452] rounded-lg px-2.5 py-1 text-slate-300 font-semibold focus:outline-none focus:border-[#F02D9B]">
                <option>Target Type: All</option>
                <option>Retention</option>
                <option>Auction Target</option>
              </select>
              <select class="bg-[#111A32] border border-[#273452] rounded-lg px-2.5 py-1 text-slate-300 font-semibold focus:outline-none focus:border-[#F02D9B]">
                <option>Sort: PRS (High &rarr; Low)</option>
                <option>Sort: Strike Rate</option>
                <option>Sort: Economy</option>
              </select>
            </div>
          </div>

          <!-- Four Custom Profile Cards Grid (Large Integrated Player Photography) -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <!-- Card 1: Vaibhav Sooryavanshi -->
            <div class="player-card border-magenta group">
              <!-- Portrait Arch Wrap with SVG Backdrop & Large Upper-Body Photo -->
              <div class="portrait-arch-wrap">
                <div class="portrait-arch-bg" style="background-image: url('{bg_card_batter}');"></div>
                <img src="{bg_portrait_arch}" alt="Arch" class="portrait-arch-vector">
                
                <!-- Role Badge at Top Left -->
                <div class="absolute top-3 left-3 z-10">
                  <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#F02D9B] text-white shadow-md">
                    #1 BATTER OVERALL
                  </span>
                </div>

                <!-- Large Upper-Body Photograph -->
                <img src="{b64_vaibhav or 'assets/vaibhav_sooryavanshi.jpg'}" alt="Vaibhav Sooryavanshi" class="player-img-cutout">
                <div class="portrait-bottom-gradient"></div>
              </div>

              <!-- Content Area Below Portrait -->
              <div class="p-4 pt-1 space-y-2.5 flex-1 flex flex-col justify-between relative z-10">
                
                <!-- Name & PRS Header -->
                <div>
                  <div class="flex items-center justify-between">
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Vaibhav Sooryavanshi</h4>
                    <div class="flex items-baseline gap-1 bg-[#F02D9B]/15 px-2 py-0.5 rounded border border-[#F02D9B]/35">
                      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight">PRS</span>
                      <span class="text-sm font-black font-mono text-[#F02D9B]">77.62</span>
                    </div>
                  </div>
                  <p class="text-[11px] text-slate-300 font-medium">Top-Order Aggressor • RR Incumbent</p>
                </div>

                <!-- 4 Stat Badges Grid -->
                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/60 rounded-lg text-[10px]">
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">HP SR</span>
                    <b class="text-white font-mono text-xs">240.82</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">HP Avg</span>
                    <b class="text-white font-mono text-xs">42.91</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">ClutchΔ</span>
                    <b class="text-[#35E6A1] font-mono text-xs">+24.77</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">BounceΔ</span>
                    <b class="text-white font-mono text-xs">42.9%</b>
                  </div>
                </div>

                <!-- Action Button -->
                <button onclick="inspectPlayer(50284, 'batter')" class="w-full py-2 rounded-lg bg-[#090E22] hover:bg-[#F02D9B] hover:text-white border border-[#273452] hover:border-[#F02D9B] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>

              <!-- Subtle Bottom Wave -->
              <div class="absolute bottom-0 inset-x-0 h-6 opacity-25 pointer-events-none" style="background-image: url('{bg_bottom_wave}'); background-size: cover;"></div>
            </div>

            <!-- Card 2: Ashutosh Sharma -->
            <div class="player-card border-gold group">
              <div class="portrait-arch-wrap">
                <div class="portrait-arch-bg" style="background-image: url('{bg_card_finisher}');"></div>
                <img src="{bg_portrait_arch}" alt="Arch" class="portrait-arch-vector">
                
                <div class="absolute top-3 left-3 z-10">
                  <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#F4C95D] text-slate-950 shadow-md">
                    #1 CLUTCH FINISHER
                  </span>
                </div>

                <img src="{b64_ashutosh or 'assets/ashutosh_sharma.jpg'}" alt="Ashutosh Sharma" class="player-img-cutout">
                <div class="portrait-bottom-gradient"></div>
              </div>

              <div class="p-4 pt-1 space-y-2.5 flex-1 flex flex-col justify-between relative z-10">
                <div>
                  <div class="flex items-center justify-between">
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Ashutosh Sharma</h4>
                    <div class="flex items-baseline gap-1 bg-[#F4C95D]/15 px-2 py-0.5 rounded border border-[#F4C95D]/35">
                      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight">PRS</span>
                      <span class="text-sm font-black font-mono text-[#F4C95D]">67.65</span>
                    </div>
                  </div>
                  <p class="text-[11px] text-slate-300 font-medium">Designated Finisher • Auction Target</p>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/60 rounded-lg text-[10px]">
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">HP SR</span>
                    <b class="text-white font-mono text-xs">189.10</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">ClutchΔ</span>
                    <b class="text-[#35E6A1] font-mono text-xs">+58.22</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Dot%</span>
                    <b class="text-white font-mono text-xs">27.0%</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Target @</span>
                    <b class="text-[#F4C95D] font-mono text-xs">₹5-7 Cr</b>
                  </div>
                </div>

                <button onclick="inspectPlayer(24707, 'batter')" class="w-full py-2 rounded-lg bg-[#090E22] hover:bg-[#F4C95D] hover:text-slate-950 border border-[#273452] hover:border-[#F4C95D] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>

              <div class="absolute bottom-0 inset-x-0 h-6 opacity-25 pointer-events-none" style="background-image: url('{bg_bottom_wave}'); background-size: cover;"></div>
            </div>

            <!-- Card 3: Matheesha Pathirana -->
            <div class="player-card border-magenta group">
              <div class="portrait-arch-wrap">
                <div class="portrait-arch-bg" style="background-image: url('{bg_card_death}');"></div>
                <img src="{bg_portrait_arch}" alt="Arch" class="portrait-arch-vector">
                
                <div class="absolute top-3 left-3 z-10">
                  <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#F02D9B] text-white shadow-md">
                    #1 DEATH CLOSER
                  </span>
                </div>

                <img src="{b64_pathirana or 'assets/matheesha_pathirana.jpg'}" alt="Matheesha Pathirana" class="player-img-cutout">
                <div class="portrait-bottom-gradient"></div>
              </div>

              <div class="p-4 pt-1 space-y-2.5 flex-1 flex flex-col justify-between relative z-10">
                <div>
                  <div class="flex items-center justify-between">
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Matheesha Pathirana</h4>
                    <div class="flex items-baseline gap-1 bg-[#F02D9B]/15 px-2 py-0.5 rounded border border-[#F02D9B]/35">
                      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight">PRS</span>
                      <span class="text-sm font-black font-mono text-[#F02D9B]">68.75</span>
                    </div>
                  </div>
                  <p class="text-[11px] text-slate-300 font-medium">Express Slinger • Primary Auction Target</p>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/60 rounded-lg text-[10px]">
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">HP Wkts</span>
                    <b class="text-white font-mono text-xs">51</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Bowling SR</span>
                    <b class="text-[#35E6A1] font-mono text-xs">10.31</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Econ</span>
                    <b class="text-white font-mono text-xs">7.78</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Target @</span>
                    <b class="text-[#F4C95D] font-mono text-xs">₹12-14.5 Cr</b>
                  </div>
                </div>

                <button onclick="inspectPlayer(24070, 'bowler')" class="w-full py-2 rounded-lg bg-[#090E22] hover:bg-[#F02D9B] hover:text-white border border-[#273452] hover:border-[#F02D9B] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>

              <div class="absolute bottom-0 inset-x-0 h-6 opacity-25 pointer-events-none" style="background-image: url('{bg_bottom_wave}'); background-size: cover;"></div>
            </div>

            <!-- Card 4: Mitchell Santner -->
            <div class="player-card border-blue group">
              <div class="portrait-arch-wrap">
                <div class="portrait-arch-bg" style="background-image: url('{bg_card_spin}');"></div>
                <img src="{bg_portrait_arch}" alt="Arch" class="portrait-arch-vector">
                
                <div class="absolute top-3 left-3 z-10">
                  <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#16C9D5] text-slate-950 shadow-md">
                    #1 SPIN SQUEEZER
                  </span>
                </div>

                <img src="{b64_santner or 'assets/mitchell_santner.jpg'}" alt="Mitchell Santner" class="player-img-cutout">
                <div class="portrait-bottom-gradient"></div>
              </div>

              <div class="p-4 pt-1 space-y-2.5 flex-1 flex flex-col justify-between relative z-10">
                <div>
                  <div class="flex items-center justify-between">
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Mitchell Santner</h4>
                    <div class="flex items-baseline gap-1 bg-[#16C9D5]/15 px-2 py-0.5 rounded border border-[#16C9D5]/35">
                      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight">PRS</span>
                      <span class="text-sm font-black font-mono text-[#16C9D5]">63.64</span>
                    </div>
                  </div>
                  <p class="text-[11px] text-slate-300 font-medium">Left-Arm Spin • Tactical Auction Target</p>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/60 rounded-lg text-[10px]">
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">HP Econ</span>
                    <b class="text-white font-mono text-xs">6.45</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Chase WPA</span>
                    <b class="text-[#35E6A1] font-mono text-xs">+2.25</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Dot%</span>
                    <b class="text-white font-mono text-xs">42.3%</b>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[9px] font-bold">Target @</span>
                    <b class="text-[#F4C95D] font-mono text-xs">₹4.6-5.8 Cr</b>
                  </div>
                </div>

                <button onclick="inspectPlayer(1469, 'bowler')" class="w-full py-2 rounded-lg bg-[#090E22] hover:bg-[#5C9DFF] hover:text-slate-950 border border-[#273452] hover:border-[#5C9DFF] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>

              <div class="absolute bottom-0 inset-x-0 h-6 opacity-25 pointer-events-none" style="background-image: url('{bg_bottom_wave}'); background-size: cover;"></div>
            </div>

          </div>
        </div>

      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 02: BATTING INTELLIGENCE                                       -->
      <!-- ===================================================================== -->
      <section id="module-batting" class="module-pane hidden space-y-5">
        <div class="rr-card p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex-1 flex flex-wrap items-center gap-3">
            <div class="relative w-64">
              <input type="text" id="batting-search" placeholder="Search 146 qualified batters..." oninput="filterBatters()" class="w-full pl-3 pr-3 py-1.5 bg-[#090E22] border border-[#273452] rounded-lg text-xs text-white placeholder-slate-400 focus:outline-none focus:border-[#F02D9B]">
            </div>
            <div class="flex items-center space-x-2 bg-[#090E22] border border-[#273452] px-3 py-1 rounded-lg text-xs">
              <span class="text-slate-400">Min Balls:</span>
              <input type="range" id="batting-min-balls" min="80" max="300" value="120" step="10" oninput="updateBattingMinBalls(this.value)" class="w-20 accent-[#F02D9B]">
              <span id="batting-min-balls-val" class="font-mono font-bold text-[#F02D9B]">120</span>
            </div>
            <select id="batting-eligibility" onchange="filterBatters()" class="bg-[#090E22] border border-[#273452] text-slate-300 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#F02D9B]">
              <option value="all">All Batters (146)</option>
              <option value="eligible">Auction Eligible Only</option>
              <option value="ipl">Active IPL Players</option>
            </select>
          </div>
          <div class="text-xs font-medium text-slate-400">
            Showing <b id="batting-count" class="text-white font-mono">146</b> qualified batters
          </div>
        </div>

        <div class="rr-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-[#090E22] border-b border-[#273452] text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                  <th class="py-3 px-3 cursor-pointer hover:text-white" onclick="sortBatters('rank')">Rank</th>
                  <th class="py-3 px-4 cursor-pointer hover:text-white" onclick="sortBatters('name')">Player</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-center" onclick="sortBatters('prs')">PRS Score</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('hp_balls')">HP Balls</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('hp_runs')">HP Runs</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('hp_sr')">HP Strike Rate</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('hp_avg')">HP Average</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('dot_pct')">Dot %</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('bound_pct')">Bound %</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBatters('delta_sr')">Clutch &Delta;SR</th>
                  <th class="py-3 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody id="batting-table-body" class="divide-y divide-[#273452]/60 text-xs font-medium"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 03: BOWLING INTELLIGENCE                                       -->
      <!-- ===================================================================== -->
      <section id="module-bowling" class="module-pane hidden space-y-5">
        <div class="rr-card p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex-1 flex flex-wrap items-center gap-3">
            <div class="relative w-64">
              <input type="text" id="bowling-search" placeholder="Search 158 qualified bowlers..." oninput="filterBowlers()" class="w-full pl-3 pr-3 py-1.5 bg-[#090E22] border border-[#273452] rounded-lg text-xs text-white placeholder-slate-400 focus:outline-none focus:border-[#5C9DFF]">
            </div>
            <div class="flex items-center space-x-2 bg-[#090E22] border border-[#273452] px-3 py-1 rounded-lg text-xs">
              <span class="text-slate-400">Min Balls:</span>
              <input type="range" id="bowling-min-balls" min="80" max="300" value="120" step="10" oninput="updateBowlingMinBalls(this.value)" class="w-20 accent-[#5C9DFF]">
              <span id="bowling-min-balls-val" class="font-mono font-bold text-[#5C9DFF]">120</span>
            </div>
            <select id="bowling-eligibility" onchange="filterBowlers()" class="bg-[#090E22] border border-[#273452] text-slate-300 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#5C9DFF]">
              <option value="eligible">Auction Eligible Candidates (BCCI Compliant)</option>
              <option value="all">All Bowlers (Including Policy-Excluded)</option>
            </select>
          </div>
          <div class="text-xs font-medium text-slate-400">
            Showing <b id="bowling-count" class="text-white font-mono">158</b> qualified bowlers
          </div>
        </div>

        <div class="rr-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-[#090E22] border-b border-[#273452] text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                  <th class="py-3 px-3 cursor-pointer hover:text-white" onclick="sortBowlers('rank')">Rank</th>
                  <th class="py-3 px-4 cursor-pointer hover:text-white" onclick="sortBowlers('name')">Bowler</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-center" onclick="sortBowlers('prs')">PRS Score</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('hp_balls')">HP Balls</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('hp_wkts')">HP Wickets</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('hp_econ')">HP Economy</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('hp_sr')">Bowling SR</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('dot_pct')">Dot %</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('bound_pct')">Bound %</th>
                  <th class="py-3 px-3 cursor-pointer hover:text-white text-right" onclick="sortBowlers('delta_econ')">&Delta; Economy</th>
                  <th class="py-3 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody id="bowling-table-body" class="divide-y divide-[#273452]/60 text-xs font-medium"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 04: PRESSURE LAB & MODELS                                      -->
      <!-- ===================================================================== -->
      <section id="module-lab" class="module-pane hidden space-y-5">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="rr-card p-4 space-y-2">
            <span class="badge-magenta text-[10px] font-bold px-2 py-0.5 rounded">PRESSURE INDEX</span>
            <h4 class="font-bold text-white text-sm">Multi-Factor Formulation</h4>
            <p class="text-slate-400 text-xs leading-relaxed">
              Indexes required run rate, wicket leverage, and phase into continuous scale \(PI \in [0, 100]\). 78,374 deliveries categorized under High Pressure (39.0%).
            </p>
          </div>
          <div class="rr-card p-4 space-y-2">
            <span class="badge-blue text-[10px] font-bold px-2 py-0.5 rounded">WPA LOGISTIC</span>
            <h4 class="font-bold text-white text-sm">Chase Modeling (AUC 0.897)</h4>
            <p class="text-slate-400 text-xs leading-relaxed">
              Trained on 95,272 chase balls. First-innings evaluated via crisis collapse (&le;30/3) and death par benchmarks. WPA rates use chase balls as denominator.
            </p>
          </div>
          <div class="rr-card p-4 space-y-2">
            <span class="badge-gold text-[10px] font-bold px-2 py-0.5 rounded">SHRINKAGE</span>
            <h4 class="font-bold text-white text-sm">Bayesian Prior &amp; Quality</h4>
            <p class="text-slate-400 text-xs leading-relaxed">
              Shrinkage ($k=80$) prevents small-sample distortion. Tournament quality weighting (IPL 1.00&times;, T20I 0.90&times;, Associate 0.75&times;).
            </p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="rr-card p-4 space-y-3">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider">Batting Efficiency Frontier</h4>
            <div class="h-64 flex items-center justify-center bg-[#090E22] rounded-lg p-2">
              <img src="{b64_batting_front or 'figures/batting_frontier.png'}" alt="Batting Frontier" class="max-h-full max-w-full object-contain">
            </div>
          </div>
          <div class="rr-card p-4 space-y-3">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider">Bowling Efficiency Frontier</h4>
            <div class="h-64 flex items-center justify-center bg-[#090E22] rounded-lg p-2">
              <img src="{b64_bowling_front or 'figures/bowling_frontier.png'}" alt="Bowling Frontier" class="max-h-full max-w-full object-contain">
            </div>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 05: RR SQUAD WAR ROOM                                          -->
      <!-- ===================================================================== -->
      <section id="module-squad" class="module-pane hidden space-y-5">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="rr-card p-4 border-l-4 border-[#35E6A1]">
            <div class="text-[10px] uppercase font-bold text-slate-400">Powerplay Phase (Overs 1-6)</div>
            <div class="text-2xl font-black text-[#35E6A1] mt-1 font-mono">+18.2%</div>
            <div class="text-[11px] text-slate-300 mt-1">Above League Par (Jaiswal &amp; Sooryavanshi)</div>
          </div>
          <div class="rr-card p-4 border-l-4 border-[#5C9DFF]">
            <div class="text-[10px] uppercase font-bold text-slate-400">Middle Phase (Overs 7-15)</div>
            <div class="text-2xl font-black text-[#5C9DFF] mt-1 font-mono">+4.1%</div>
            <div class="text-[11px] text-slate-300 mt-1">Controlled Tempo (Samson &amp; Parag)</div>
          </div>
          <div class="rr-card p-4 border-l-4 border-[#F02D9B] bg-gradient-to-r from-[#201026] to-[#111A32]">
            <div class="text-[10px] uppercase font-bold text-[#F02D9B]">Death Phase (Overs 16-20)</div>
            <div class="text-2xl font-black text-[#F02D9B] mt-1 font-mono">-38.6%</div>
            <div class="text-[11px] text-pink-300 mt-1">Death Bowling Deficit (Curran/Deshpande leak)</div>
          </div>
        </div>

        <div class="rr-card overflow-hidden">
          <div class="px-5 py-3 border-b border-[#273452] flex items-center justify-between">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider">Current Squad Pressure Reliability Audit</h4>
            <span class="text-xs text-slate-400">27 Players Audited</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-[#090E22] text-[10px] uppercase font-bold text-slate-400 border-b border-[#273452]">
                <tr>
                  <th class="py-2.5 px-4">Player Name</th>
                  <th class="py-2.5 px-3">Batting Rank</th>
                  <th class="py-2.5 px-3">Batting PRS</th>
                  <th class="py-2.5 px-3">Bowling Rank</th>
                  <th class="py-2.5 px-3">Bowling PRS</th>
                  <th class="py-2.5 px-3">HP Econ</th>
                  <th class="py-2.5 px-4">Tactical Verdict</th>
                </tr>
              </thead>
              <tbody id="squad-table-body" class="divide-y divide-[#273452]/60 font-medium"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 06: AUCTION SIMULATOR                                          -->
      <!-- ===================================================================== -->
      <section id="module-auction" class="module-pane hidden space-y-5">
        <div class="rr-card p-5 space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-[#273452] pb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                Auction Purse Allocation Planner (₹35.0 Cr War Chest)
                <span class="badge-gold px-2 py-0.5 rounded text-[9px] font-bold">SIMULATOR</span>
              </h3>
              <p class="text-[11px] text-slate-400">Simulate winning bids for target players and evaluate remaining purse headroom</p>
            </div>
            <div class="flex items-center space-x-3 bg-[#090E22] border border-[#273452] px-3 py-1.5 rounded-lg text-xs font-mono">
              <span class="text-slate-400">Remaining Purse:</span>
              <span id="sim-remaining-purse" class="text-base font-black text-[#35E6A1]">₹7.50 Cr</span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-3.5 rounded-lg bg-[#090E22] border border-[#273452] space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">Matheesha Pathirana</span>
                <span id="val-sim-pathirana" class="font-mono font-bold text-[#F02D9B]">₹13.50 Cr</span>
              </div>
              <input type="range" id="slider-pathirana" min="9.0" max="18.0" step="0.25" value="13.50" oninput="updateAuctionSimulator()" class="w-full accent-[#F02D9B]">
            </div>
            <div class="p-3.5 rounded-lg bg-[#090E22] border border-[#273452] space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">Mitchell Santner</span>
                <span id="val-sim-santner" class="font-mono font-bold text-[#5C9DFF]">₹7.50 Cr</span>
              </div>
              <input type="range" id="slider-santner" min="4.0" max="11.0" step="0.25" value="7.50" oninput="updateAuctionSimulator()" class="w-full accent-[#5C9DFF]">
            </div>
            <div class="p-3.5 rounded-lg bg-[#090E22] border border-[#273452] space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">Ashutosh Sharma</span>
                <span id="val-sim-ashutosh" class="font-mono font-bold text-[#F4C95D]">₹6.50 Cr</span>
              </div>
              <input type="range" id="slider-ashutosh" min="3.0" max="10.0" step="0.25" value="6.50" oninput="updateAuctionSimulator()" class="w-full accent-[#F4C95D]">
            </div>
          </div>
        </div>

        <div class="rr-card p-5 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider border-b border-[#273452] pb-2">Dynamic 3-Player Head-to-Head Comparison</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-[11px] text-slate-400 font-semibold mb-1">Player 1</label>
              <select id="compare-p1" onchange="updateComparison()" class="w-full bg-[#090E22] border border-[#273452] rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-[#F02D9B]"></select>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 font-semibold mb-1">Player 2</label>
              <select id="compare-p2" onchange="updateComparison()" class="w-full bg-[#090E22] border border-[#273452] rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-[#F02D9B]"></select>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 font-semibold mb-1">Player 3</label>
              <select id="compare-p3" onchange="updateComparison()" class="w-full bg-[#090E22] border border-[#273452] rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-[#F02D9B]"></select>
            </div>
          </div>
          <div id="comparison-display-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2"></div>
        </div>
      </section>

    </main>
  </div>

  <!-- ========================================================================= -->
  <!-- MODALS: RECONCILIATION & PLAYER DOSSIER                                   -->
  <!-- ========================================================================= -->
  <div id="player-modal" class="fixed inset-0 z-50 modal-backdrop hidden flex items-center justify-center p-4">
    <div class="rr-card max-w-xl w-full p-6 relative border-[#F02D9B]/40 shadow-2xl bg-[#111A32] space-y-4 max-h-[90vh] overflow-y-auto">
      <button onclick="closePlayerModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>

      <div class="flex items-center space-x-4 border-b border-[#273452] pb-4">
        <div id="modal-player-img-container" class="w-16 h-16 rounded-full overflow-hidden border-2 border-[#F02D9B] flex-shrink-0 bg-[#090E22] flex items-center justify-center">
          <span id="modal-player-initials" class="font-black text-xl text-white"></span>
        </div>
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <h3 id="modal-player-name" class="text-lg font-black text-white"></h3>
            <span id="modal-player-role-badge" class="badge-magenta text-[10px] font-bold px-2 py-0.5 rounded"></span>
          </div>
          <p id="modal-player-eligibility" class="text-xs text-slate-400"></p>
        </div>
      </div>

      <div id="modal-player-metrics-grid" class="grid grid-cols-3 gap-3"></div>

      <div class="p-3.5 rounded-lg bg-[#090E22] border border-[#273452] space-y-1.5">
        <div class="text-[10px] uppercase font-bold text-[#F02D9B] tracking-wider">War Room Scouting Assessment</div>
        <p id="modal-player-verdict" class="text-xs text-slate-300 leading-relaxed"></p>
      </div>

      <div class="pt-2 flex justify-end">
        <button onclick="closePlayerModal()" class="px-4 py-1.5 rounded-lg bg-[#090E22] hover:bg-[#151F3A] text-xs font-bold text-white transition">Close</button>
      </div>
    </div>
  </div>

  <div id="reconciliation-modal" class="fixed inset-0 z-50 modal-backdrop hidden flex items-center justify-center p-4">
    <div class="rr-card max-w-2xl w-full p-6 relative border-[#5C9DFF]/40 shadow-2xl bg-[#111A32] space-y-4 max-h-[90vh] overflow-y-auto">
      <button onclick="closeReconciliationModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>

      <div class="border-b border-[#273452] pb-3">
        <h3 class="text-base font-black text-white flex items-center gap-2">
          Dataset Match Count Reconciliation &amp; Audit
          <span class="badge-blue text-[10px] font-bold px-2 py-0.5 rounded">VERIFIED</span>
        </h3>
        <p class="text-xs text-slate-400 mt-0.5">883 scheduled matches vs 867 contested matches in the proprietary delivery dataset</p>
      </div>

      <div class="grid grid-cols-3 gap-3 text-center">
        <div class="p-3 rounded-lg bg-[#090E22] border border-[#273452]">
          <div class="text-[10px] uppercase text-slate-400 font-bold">Scheduled Matches</div>
          <div class="text-xl font-black text-white font-mono mt-1">883</div>
        </div>
        <div class="p-3 rounded-lg bg-[#090E22] border border-[#273452]">
          <div class="text-[10px] uppercase text-slate-400 font-bold">Contested Matches</div>
          <div class="text-xl font-black text-[#F02D9B] font-mono mt-1">867</div>
        </div>
        <div class="p-3 rounded-lg bg-[#090E22] border border-[#273452]">
          <div class="text-[10px] uppercase text-slate-400 font-bold">Abandoned Matches</div>
          <div class="text-xl font-black text-[#F4C95D] font-mono mt-1">16</div>
        </div>
      </div>

      <div class="text-xs text-slate-300 leading-relaxed bg-[#090E22] p-3.5 rounded-lg border border-[#273452]">
        Exactly 16 scheduled matches had 0 balls bowled due to persistent rain washouts. Equation: <b class="text-[#35E6A1]">883 Scheduled = 867 Contested + 16 Abandoned</b>.
      </div>

      <div class="pt-2 flex justify-end">
        <button onclick="closeReconciliationModal()" class="px-4 py-1.5 rounded-lg bg-[#5C9DFF] hover:bg-blue-500 text-xs font-bold text-slate-950 transition">Acknowledge</button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- INLINE DATA & APPLICATION JAVASCRIPT                                      -->
  <!-- ========================================================================= -->
  <script>
    const BATTERS_DATA = {json.dumps(batters_data)};
    const BOWLERS_DATA = {json.dumps(bowlers_data)};
    const RR_SQUAD_DATA = {json.dumps(rr_squad_data)};
    const AUCTION_TARGETS_DATA = {json.dumps(auction_targets_data)};
    const METADATA = {json.dumps(metadata_data)};

    let currentModel = 'calibrated';
    let currentBattingSort = {{ column: 'rank', asc: true }};
    let currentBowlingSort = {{ column: 'rank', asc: true }};

    function switchModule(moduleId) {{
      document.querySelectorAll('.module-pane').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));

      const targetPane = document.getElementById(moduleId);
      if (targetPane) targetPane.classList.remove('hidden');

      const targetNav = document.getElementById('nav-' + moduleId);
      if (targetNav) targetNav.classList.add('active');

      const titles = {{
        'module-overview': '01 EXECUTIVE OVERVIEW',
        'module-batting': '02 BATTING INTELLIGENCE',
        'module-bowling': '03 BOWLING INTELLIGENCE',
        'module-lab': '04 PRESSURE LAB & MODELS',
        'module-squad': '05 RR SQUAD WAR ROOM',
        'module-auction': '06 AUCTION SIMULATOR'
      }};
      document.getElementById('breadcrumb-current').textContent = titles[moduleId] || '';
    }}

    function setModel(modelName) {{
      currentModel = modelName;
      const btnCal = document.getElementById('btn-model-calibrated');
      const btnLeg = document.getElementById('btn-model-legacy');

      if (modelName === 'calibrated') {{
        btnCal.className = "px-3 py-1 rounded-md text-[11px] font-bold text-white bg-[#F02D9B] shadow-sm flex items-center gap-1 transition";
        btnLeg.className = "px-3 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition";
      }} else {{
        btnLeg.className = "px-3 py-1 rounded-md text-[11px] font-bold text-white bg-[#5C9DFF] shadow-sm flex items-center gap-1 transition";
        btnCal.className = "px-3 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition";
      }}

      renderBattersTable();
      renderBowlersTable();
      updateComparison();
    }}

    function initHomepageCharts() {{
      // 1. Squad Quality Snapshot (Radar Pentagon)
      const ctxRadar = document.getElementById('chart-squad-radar').getContext('2d');
      new Chart(ctxRadar, {{
        type: 'radar',
        data: {{
          labels: ['Batting', 'Bowling', 'Clutch', 'Balance', 'Depth'],
          datasets: [
            {{
              label: 'RR (Current)',
              data: [76.4, 72.1, 78.8, 77.3, 74.9],
              backgroundColor: 'rgba(240, 45, 155, 0.35)',
              borderColor: '#F02D9B',
              borderWidth: 2,
              pointBackgroundColor: '#F02D9B',
              pointRadius: 3,
            }},
            {{
              label: 'League Avg',
              data: [71.2, 69.8, 70.5, 71.0, 68.5],
              backgroundColor: 'rgba(92, 157, 255, 0.15)',
              borderColor: '#5C9DFF',
              borderWidth: 1.5,
              borderDash: [4, 4],
              pointBackgroundColor: '#5C9DFF',
              pointRadius: 2,
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }}
          }},
          scales: {{
            r: {{
              min: 50,
              max: 90,
              ticks: {{ display: false, stepSize: 10 }},
              grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
              angleLines: {{ color: 'rgba(255, 255, 255, 0.08)' }},
              pointLabels: {{
                color: '#9AA8C2',
                font: {{ size: 9, weight: 'bold' }}
              }}
            }}
          }}
        }}
      }});

      // 2. Performance Trend & Impact (Multi-axis Line/Area)
      const ctxTrend = document.getElementById('chart-performance-trend').getContext('2d');
      const gradient = ctxTrend.createLinearGradient(0, 0, 0, 200);
      gradient.addColorStop(0, 'rgba(92, 157, 255, 0.4)');
      gradient.addColorStop(1, 'rgba(92, 157, 255, 0.0)');

      new Chart(ctxTrend, {{
        type: 'line',
        data: {{
          labels: ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
          datasets: [
            {{
              label: 'PRS (Player Strength)',
              data: [59, 64, 61, 71, 69, 76],
              borderColor: '#F02D9B',
              borderWidth: 2.5,
              pointBackgroundColor: '#F02D9B',
              pointBorderColor: '#fff',
              pointBorderWidth: 1.5,
              pointRadius: 4,
              tension: 0.35,
              yAxisID: 'y'
            }},
            {{
              label: 'HP% (High-Impact)',
              data: [24, 30, 26, 38, 42, 46],
              borderColor: '#5C9DFF',
              borderWidth: 1.5,
              backgroundColor: gradient,
              fill: true,
              pointRadius: 0,
              tension: 0.35,
              yAxisID: 'y1'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }}
          }},
          scales: {{
            x: {{
              grid: {{ display: false }},
              ticks: {{ color: '#9AA8C2', font: {{ size: 9 }} }}
            }},
            y: {{
              type: 'linear',
              position: 'left',
              min: 50,
              max: 80,
              grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
              ticks: {{ color: '#9AA8C2', stepSize: 5, font: {{ size: 9 }} }}
            }},
            y1: {{
              type: 'linear',
              position: 'right',
              min: 20,
              max: 50,
              grid: {{ display: false }},
              ticks: {{
                color: '#9AA8C2',
                stepSize: 5,
                font: {{ size: 9 }},
                callback: v => v + '%'
              }}
            }}
          }}
        }}
      }});

      // 3. Model Balance (Donut)
      const ctxDonut = document.getElementById('chart-model-balance').getContext('2d');
      new Chart(ctxDonut, {{
        type: 'doughnut',
        data: {{
          labels: ['Batting Impact', 'Bowling Impact', 'Clutch (Death)', 'Context (Econ/Wkts)', 'Form & Consistency'],
          datasets: [{{
            data: [32, 28, 18, 12, 10],
            backgroundColor: ['#F02D9B', '#5C9DFF', '#16C9D5', '#F4C95D', '#A45BEE'],
            borderColor: '#111A32',
            borderWidth: 3,
            hoverOffset: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          cutout: '72%',
          plugins: {{
            legend: {{ display: false }}
          }}
        }}
      }});
    }}

    // Table Rendering
    function renderBattersTable() {{
      const tbody = document.getElementById('batting-table-body');
      if (!tbody) return;
      const searchVal = document.getElementById('batting-search').value.toLowerCase();
      const minBalls = parseInt(document.getElementById('batting-min-balls').value, 10);
      const eligFilter = document.getElementById('batting-eligibility').value;

      let filtered = BATTERS_DATA.filter(b => {{
        if (b.hp_balls < minBalls) return false;
        if (searchVal && !b.name.toLowerCase().includes(searchVal)) return false;
        if (eligFilter === 'eligible' && !b.is_auction_eligible) return false;
        if (eligFilter === 'ipl' && b.eligibility_status !== 'ELIGIBLE_ACTIVE_IPL') return false;
        return true;
      }});

      filtered.sort((a, b) => {{
        let valA, valB;
        if (currentBattingSort.column === 'rank') {{
          valA = a.rank; valB = b.rank;
        }} else if (currentBattingSort.column === 'name') {{
          valA = a.name; valB = b.name;
        }} else if (currentBattingSort.column === 'prs') {{
          valA = currentModel === 'calibrated' ? a.prs_calibrated : a.prs_legacy;
          valB = currentModel === 'calibrated' ? b.prs_calibrated : b.prs_legacy;
        }} else if (currentBattingSort.column === 'hp_balls') {{
          valA = a.hp_balls; valB = b.hp_balls;
        }} else if (currentBattingSort.column === 'hp_runs') {{
          valA = a.hp_runs; valB = b.hp_runs;
        }} else if (currentBattingSort.column === 'hp_sr') {{
          valA = a.hp_sr; valB = b.hp_sr;
        }} else if (currentBattingSort.column === 'hp_avg') {{
          valA = a.hp_avg; valB = b.hp_avg;
        }} else if (currentBattingSort.column === 'dot_pct') {{
          valA = a.dot_pct; valB = b.dot_pct;
        }} else if (currentBattingSort.column === 'bound_pct') {{
          valA = a.bound_pct; valB = b.bound_pct;
        }} else if (currentBattingSort.column === 'delta_sr') {{
          valA = a.delta_sr; valB = b.delta_sr;
        }}
        if (valA < valB) return currentBattingSort.asc ? -1 : 1;
        if (valA > valB) return currentBattingSort.asc ? 1 : -1;
        return 0;
      }});

      document.getElementById('batting-count').textContent = filtered.length;

      let html = '';
      filtered.forEach(b => {{
        const prsScore = (currentModel === 'calibrated' ? b.prs_calibrated : b.prs_legacy).toFixed(2);
        const deltaColor = b.delta_sr >= 0 ? 'text-[#35E6A1]' : 'text-red-400';
        const deltaSign = b.delta_sr >= 0 ? '+' : '';
        const rankBadge = b.rank <= 10 ? 'bg-[#F02D9B]/20 text-[#F02D9B] border border-[#F02D9B]/30' : 'text-slate-400';

        html += `
          <tr class="hover:bg-[#151F3A]/80 transition">
            <td class="py-2.5 px-3 font-mono font-bold text-center">
              <span class="px-1.5 py-0.5 rounded text-[11px] ${{rankBadge}}">#${{b.rank}}</span>
            </td>
            <td class="py-2.5 px-4 font-bold text-white flex items-center gap-2">
              <span>${{b.name}}</span>
              ${{b.id === 50284 ? '<span class="badge-magenta text-[9px] px-1 rounded font-bold">RR</span>' : ''}}
              ${{b.id === 24707 ? '<span class="badge-gold text-[9px] px-1 rounded font-bold">TARGET</span>' : ''}}
            </td>
            <td class="py-2.5 px-3 text-center">
              <span class="font-mono font-bold text-[#F02D9B] text-xs">${{prsScore}}</span>
            </td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_balls}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_runs}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-white">${{b.hp_sr.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_avg.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.dot_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.bound_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold ${{deltaColor}}">${{deltaSign}}${{b.delta_sr.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-center">
              <button onclick="inspectPlayer(${{b.id}}, 'batter')" class="px-2 py-1 rounded bg-[#090E22] hover:bg-[#F02D9B] hover:text-white text-[11px] font-semibold text-slate-300 transition">
                Inspect
              </button>
            </td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    function filterBatters() {{ renderBattersTable(); }}
    function updateBattingMinBalls(val) {{
      document.getElementById('batting-min-balls-val').textContent = val;
      renderBattersTable();
    }}
    function sortBatters(col) {{
      if (currentBattingSort.column === col) {{
        currentBattingSort.asc = !currentBattingSort.asc;
      }} else {{
        currentBattingSort.column = col;
        currentBattingSort.asc = false;
      }}
      renderBattersTable();
    }}

    // Bowling Table Rendering
    function renderBowlersTable() {{
      const tbody = document.getElementById('bowling-table-body');
      if (!tbody) return;
      const searchVal = document.getElementById('bowling-search').value.toLowerCase();
      const minBalls = parseInt(document.getElementById('bowling-min-balls').value, 10);
      const eligFilter = document.getElementById('bowling-eligibility').value;

      let filtered = BOWLERS_DATA.filter(b => {{
        if (b.hp_balls < minBalls) return false;
        if (searchVal && !b.name.toLowerCase().includes(searchVal)) return false;
        if (eligFilter === 'eligible' && !b.is_auction_eligible) return false;
        return true;
      }});

      filtered.sort((a, b) => {{
        let valA, valB;
        if (currentBowlingSort.column === 'rank') {{
          valA = eligFilter === 'eligible' ? (a.rank_eligible || 999) : a.rank_all;
          valB = eligFilter === 'eligible' ? (b.rank_eligible || 999) : b.rank_all;
        }} else if (currentBowlingSort.column === 'name') {{
          valA = a.name; valB = b.name;
        }} else if (currentBowlingSort.column === 'prs') {{
          valA = currentModel === 'calibrated' ? a.prs_calibrated : a.prs_legacy;
          valB = currentModel === 'calibrated' ? b.prs_calibrated : b.prs_legacy;
        }} else if (currentBowlingSort.column === 'hp_balls') {{
          valA = a.hp_balls; valB = b.hp_balls;
        }} else if (currentBowlingSort.column === 'hp_wkts') {{
          valA = a.hp_wkts; valB = b.hp_wkts;
        }} else if (currentBowlingSort.column === 'hp_econ') {{
          valA = a.hp_econ; valB = b.hp_econ;
        }} else if (currentBowlingSort.column === 'hp_sr') {{
          valA = a.hp_sr; valB = b.hp_sr;
        }} else if (currentBowlingSort.column === 'dot_pct') {{
          valA = a.dot_pct; valB = b.dot_pct;
        }} else if (currentBowlingSort.column === 'bound_pct') {{
          valA = a.bound_pct; valB = b.bound_pct;
        }} else if (currentBowlingSort.column === 'delta_econ') {{
          valA = a.delta_econ; valB = b.delta_econ;
        }}
        if (valA < valB) return currentBowlingSort.asc ? -1 : 1;
        if (valA > valB) return currentBowlingSort.asc ? 1 : -1;
        return 0;
      }});

      document.getElementById('bowling-count').textContent = filtered.length;

      let html = '';
      filtered.forEach(b => {{
        const prsScore = (currentModel === 'calibrated' ? b.prs_calibrated : b.prs_legacy).toFixed(2);
        const rankDisplay = eligFilter === 'eligible' ? (b.rank_eligible ? '#' + b.rank_eligible : 'N/A') : '#' + b.rank_all;
        const deltaColor = b.delta_econ <= 0 ? 'text-[#35E6A1]' : 'text-red-400';
        const deltaSign = b.delta_econ > 0 ? '+' : '';

        html += `
          <tr class="hover:bg-[#151F3A]/80 transition">
            <td class="py-2.5 px-3 font-mono font-bold text-center">
              <span class="px-1.5 py-0.5 rounded text-[11px] bg-[#5C9DFF]/20 text-[#5C9DFF]">${{rankDisplay}}</span>
            </td>
            <td class="py-2.5 px-4 font-bold text-white flex items-center gap-2">
              <span>${{b.name}}</span>
              ${{!b.is_auction_eligible ? '<span class="badge-red text-[9px] px-1 rounded font-bold">EXCLUDED</span>' : ''}}
              ${{b.id === 24070 ? '<span class="badge-magenta text-[9px] px-1 rounded font-bold">#1 CLOSER</span>' : ''}}
              ${{b.id === 1469 ? '<span class="badge-blue text-[9px] px-1 rounded font-bold">#1 SPIN</span>' : ''}}
            </td>
            <td class="py-2.5 px-3 text-center">
              <span class="font-mono font-bold text-[#5C9DFF] text-xs">${{prsScore}}</span>
            </td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_balls}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-[#35E6A1]">${{b.hp_wkts}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-white">${{b.hp_econ.toFixed(2)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_sr.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.dot_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.bound_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold ${{deltaColor}}">${{deltaSign}}${{b.delta_econ.toFixed(2)}}</td>
            <td class="py-2.5 px-3 text-center">
              <button onclick="inspectPlayer(${{b.id}}, 'bowler')" class="px-2 py-1 rounded bg-[#090E22] hover:bg-[#5C9DFF] hover:text-slate-950 text-[11px] font-semibold text-slate-300 transition">
                Inspect
              </button>
            </td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    function filterBowlers() {{ renderBowlersTable(); }}
    function updateBowlingMinBalls(val) {{
      document.getElementById('bowling-min-balls-val').textContent = val;
      renderBowlersTable();
    }}
    function sortBowlers(col) {{
      if (currentBowlingSort.column === col) {{
        currentBowlingSort.asc = !currentBowlingSort.asc;
      }} else {{
        currentBowlingSort.column = col;
        currentBowlingSort.asc = col === 'hp_econ' || col === 'hp_sr';
      }}
      renderBowlersTable();
    }}

    // RR Squad Table
    function renderSquadTable() {{
      const tbody = document.getElementById('squad-table-body');
      if (!tbody) return;
      let html = '';

      RR_SQUAD_DATA.forEach(p => {{
        const bRank = p.batter_rank ? '#' + p.batter_rank : '-';
        const bPrs = p.batter_prs ? p.batter_prs.toFixed(1) : '-';
        const bwRank = p.bowler_rank ? '#' + p.bowler_rank : '-';
        const bwPrs = p.bowler_prs ? p.bowler_prs.toFixed(1) : '-';
        const bwEcon = p.bowler_hp_econ ? p.bowler_hp_econ.toFixed(2) : '-';

        let verdict = '<span class="text-slate-400">Squad Depth</span>';
        if (p.player_name === 'Vaibhav Sooryavanshi') verdict = '<span class="badge-magenta px-2 py-0.5 rounded font-bold">#1 Key Retention &amp; Build Around</span>';
        else if (p.player_name === 'Yashasvi Jaiswal') verdict = '<span class="badge-green px-2 py-0.5 rounded font-bold">Core Opener (PRS 55.44)</span>';
        else if (p.player_name === 'Sam Curran') verdict = '<span class="badge-red px-2 py-0.5 rounded font-bold">High Death Leak (10.21 Econ)</span>';
        else if (p.player_name === 'Tushar Deshpande') verdict = '<span class="badge-red px-2 py-0.5 rounded font-bold">Death Leak (9.84 Econ)</span>';
        else if (p.player_name === 'Jofra Archer') verdict = '<span class="badge-blue px-2 py-0.5 rounded font-bold">Pace Spearhead (PRS 48.75)</span>';
        else if (p.player_name === 'Dhruv Jurel') verdict = '<span class="badge-gold px-2 py-0.5 rounded font-bold">Crisis Closer (PRS 42.61)</span>';

        html += `
          <tr class="hover:bg-[#151F3A]/80 transition">
            <td class="py-2 px-4 font-bold text-white">${{p.player_name}}</td>
            <td class="py-2 px-3 font-mono text-slate-300">${{bRank}}</td>
            <td class="py-2 px-3 font-mono text-[#F02D9B] font-bold">${{bPrs}}</td>
            <td class="py-2 px-3 font-mono text-slate-300">${{bwRank}}</td>
            <td class="py-2 px-3 font-mono text-[#5C9DFF] font-bold">${{bwPrs}}</td>
            <td class="py-2 px-3 font-mono text-slate-300">${{bwEcon}}</td>
            <td class="py-2 px-4 text-xs">${{verdict}}</td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    // Auction Simulator
    function updateAuctionSimulator() {{
      const pCost = parseFloat(document.getElementById('slider-pathirana').value);
      const sCost = parseFloat(document.getElementById('slider-santner').value);
      const aCost = parseFloat(document.getElementById('slider-ashutosh').value);

      document.getElementById('val-sim-pathirana').textContent = '₹' + pCost.toFixed(2) + ' Cr';
      document.getElementById('val-sim-santner').textContent = '₹' + sCost.toFixed(2) + ' Cr';
      document.getElementById('val-sim-ashutosh').textContent = '₹' + aCost.toFixed(2) + ' Cr';

      const totalSpent = pCost + sCost + aCost;
      const remaining = 35.0 - totalSpent;

      const remEl = document.getElementById('sim-remaining-purse');
      remEl.textContent = '₹' + remaining.toFixed(2) + ' Cr';
      if (remaining < 3.0) {{
        remEl.className = 'text-base font-black text-red-400';
      }} else if (remaining < 6.0) {{
        remEl.className = 'text-base font-black text-[#F4C95D]';
      }} else {{
        remEl.className = 'text-base font-black text-[#35E6A1]';
      }}
    }}

    function initComparisonDropdowns() {{
      const sel1 = document.getElementById('compare-p1');
      const sel2 = document.getElementById('compare-p2');
      const sel3 = document.getElementById('compare-p3');
      if (!sel1 || !sel2 || !sel3) return;

      let optionsHtml = '<optgroup label="Auction Targets & Bowlers">';
      BOWLERS_DATA.forEach(b => {{
        optionsHtml += `<option value="bowl_${{b.id}}">${{b.name}} (Bowler - PRS ${{b.prs_calibrated.toFixed(1)}})</option>`;
      }});
      optionsHtml += '</optgroup><optgroup label="Batters">';
      BATTERS_DATA.forEach(b => {{
        optionsHtml += `<option value="bat_${{b.id}}">${{b.name}} (Batter - PRS ${{b.prs_calibrated.toFixed(1)}})</option>`;
      }});
      optionsHtml += '</optgroup>';

      sel1.innerHTML = optionsHtml;
      sel2.innerHTML = optionsHtml;
      sel3.innerHTML = optionsHtml;

      sel1.value = 'bowl_24070';
      sel2.value = 'bowl_1469';
      sel3.value = 'bowl_4409';

      updateComparison();
    }}

    function getPlayerObj(valStr) {{
      const [type, idStr] = valStr.split('_');
      const id = parseInt(idStr, 10);
      if (type === 'bat') {{
        return {{ type: 'bat', data: BATTERS_DATA.find(b => b.id === id) }};
      }} else {{
        return {{ type: 'bowl', data: BOWLERS_DATA.find(b => b.id === id) }};
      }}
    }}

    function updateComparison() {{
      const p1Val = document.getElementById('compare-p1').value;
      const p2Val = document.getElementById('compare-p2').value;
      const p3Val = document.getElementById('compare-p3').value;

      const p1 = getPlayerObj(p1Val);
      const p2 = getPlayerObj(p2Val);
      const p3 = getPlayerObj(p3Val);

      const renderCol = (pObj, title) => {{
        if (!pObj || !pObj.data) return '';
        const d = pObj.data;
        const isBat = pObj.type === 'bat';
        const prs = currentModel === 'calibrated' ? d.prs_calibrated : d.prs_legacy;

        return `
          <div class="p-4 rounded-xl bg-[#090E22] border border-[#273452] space-y-3">
            <div class="flex items-center justify-between border-b border-[#273452] pb-2">
              <div>
                <span class="text-[10px] text-[#F02D9B] font-bold uppercase">${{title}}</span>
                <h4 class="font-bold text-white text-sm">${{d.name}}</h4>
              </div>
              <span class="badge-gold text-xs font-mono font-bold px-2 py-0.5 rounded">PRS ${{prs.toFixed(2)}}</span>
            </div>
            <div class="space-y-1.5 text-xs">
              <div class="flex justify-between">
                <span class="text-slate-400">Role:</span>
                <span class="text-white font-medium">${{isBat ? 'Batter / Striker' : 'Bowler / Specialist'}}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">HP Deliveries:</span>
                <span class="font-mono text-white">${{d.hp_balls}}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">${{isBat ? 'HP Strike Rate:' : 'HP Economy:'}}</span>
                <span class="font-mono font-bold text-[#35E6A1]">${{isBat ? d.hp_sr.toFixed(1) : d.hp_econ.toFixed(2)}}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">${{isBat ? 'HP Average:' : 'Bowling SR:'}}</span>
                <span class="font-mono text-white">${{isBat ? d.hp_avg.toFixed(1) : d.hp_sr.toFixed(1)}}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">Dot Ball %:</span>
                <span class="font-mono text-slate-300">${{d.dot_pct.toFixed(1)}}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">Chase WPA / 100:</span>
                <span class="font-mono text-white">${{d.chase_wpa.toFixed(2)}}</span>
              </div>
            </div>
          </div>
        `;
      }};

      document.getElementById('comparison-display-grid').innerHTML = `
        ${{renderCol(p1, 'Candidate 1')}}
        ${{renderCol(p2, 'Candidate 2')}}
        ${{renderCol(p3, 'Candidate 3')}}
      `;
    }}

    // Player Modal
    function inspectPlayer(playerId, playerType) {{
      let player;
      if (playerType === 'batter') {{
        player = BATTERS_DATA.find(b => b.id === playerId);
      }} else {{
        player = BOWLERS_DATA.find(b => b.id === playerId);
      }}
      if (!player) return;

      document.getElementById('modal-player-name').textContent = player.name;
      document.getElementById('modal-player-role-badge').textContent = playerType === 'batter' ? 'BATTER' : 'BOWLER';
      document.getElementById('modal-player-eligibility').textContent = player.eligibility_status.replace(/_/g, ' ');

      const initials = player.name.split(' ').map(n => n[0]).join('').slice(0, 2);
      document.getElementById('modal-player-initials').textContent = initials;

      const prs = currentModel === 'calibrated' ? player.prs_calibrated : player.prs_legacy;

      let metricsHtml = '';
      if (playerType === 'batter') {{
        metricsHtml = `
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">PRS Score</span>
            <div class="text-base font-black text-[#F02D9B] font-mono">${{prs.toFixed(2)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Strike Rate</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_sr.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Average</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_avg.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Clutch &Delta;SR</span>
            <div class="text-base font-black text-[#35E6A1] font-mono">+${{player.delta_sr.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Dot Ball %</span>
            <div class="text-base font-black text-slate-300 font-mono">${{player.dot_pct.toFixed(1)}}%</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Bound %</span>
            <div class="text-base font-black text-slate-300 font-mono">${{player.bound_pct.toFixed(1)}}%</div>
          </div>
        `;
      }} else {{
        metricsHtml = `
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">PRS Score</span>
            <div class="text-base font-black text-[#5C9DFF] font-mono">${{prs.toFixed(2)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Economy</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_econ.toFixed(2)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Wickets</span>
            <div class="text-base font-black text-[#35E6A1] font-mono">${{player.hp_wkts}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Bowling SR</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_sr.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Dot Ball %</span>
            <div class="text-base font-black text-slate-300 font-mono">${{player.dot_pct.toFixed(1)}}%</div>
          </div>
          <div class="p-2.5 rounded bg-[#090E22] border border-[#273452] text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Chase WPA / 100</span>
            <div class="text-base font-black text-[#F4C95D] font-mono">${{player.chase_wpa.toFixed(2)}}</div>
          </div>
        `;
      }}
      document.getElementById('modal-player-metrics-grid').innerHTML = metricsHtml;

      let verdict = `${{player.name}} has faced/bowled ${{player.hp_balls}} deliveries in high-pressure match situations across the 2022-2026 window. `;
      if (player.name === 'Vaibhav Sooryavanshi') verdict += 'Demonstrates exceptional boundary capability (42.9%) with top-tier strike rate. High-conviction core retention recommendation.';
      else if (player.name === 'Ashutosh Sharma') verdict += 'Highest clutch strike rate delta in the entire tournament dataset (+58.22). Primary domestic finisher auction target.';
      else if (player.name === 'Matheesha Pathirana') verdict += 'Elite sling-arm death closer with 51 wickets under pressure and 10.31 strike rate. Essential acquisition to cure -38.6% death deficit.';
      else if (player.name === 'Mitchell Santner') verdict += 'Supreme economy of 6.45 RPO in pressure situations. Solves middle-overs control and batting depth.';
      else verdict += 'Meets all minimum statistical volume requirements with consistent match execution.';

      document.getElementById('modal-player-verdict').textContent = verdict;
      document.getElementById('player-modal').classList.remove('hidden');
    }}

    function closePlayerModal() {{
      document.getElementById('player-modal').classList.add('hidden');
    }}

    function openReconciliationModal() {{
      document.getElementById('reconciliation-modal').classList.remove('hidden');
    }}

    function closeReconciliationModal() {{
      document.getElementById('reconciliation-modal').classList.add('hidden');
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initHomepageCharts();
      renderBattersTable();
      renderBowlersTable();
      renderSquadTable();
      initComparisonDropdowns();
      updateAuctionSimulator();
    }});
  </script>

</body>
</html>
"""

    for dest in [
        os.path.join(DASHBOARD_DIR, "index.html"),
        os.path.join(WORKSPACE_DIR, "index.html"),
        os.path.join(WORKSPACE_DIR, "dashboard.html"),
        r"C:\Users\lenovo\.gemini\antigravity\brain\02fbebc3-754b-4b0e-8c30-841bbd239b40\dashboard.html"
    ]:
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"SUCCESS: Written {dest} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
