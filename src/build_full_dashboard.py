import os
import json
import base64

WORKSPACE_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")
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

def main():
    print("Building Rajasthan Royals War Room 6-Module Interactive Dashboard...")

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

    # Encode images to base64 for standalone portability
    b64_crest = load_base64(os.path.join(ASSETS_DIR, "rr_crest.jpg"))
    b64_vaibhav = load_base64(os.path.join(ASSETS_DIR, "vaibhav_sooryavanshi.jpg"))
    b64_ashutosh = load_base64(os.path.join(ASSETS_DIR, "ashutosh_sharma.jpg"))
    b64_pathirana = load_base64(os.path.join(ASSETS_DIR, "matheesha_pathirana.jpg"))
    b64_santner = load_base64(os.path.join(ASSETS_DIR, "mitchell_santner.jpg"))
    b64_banner = load_base64(os.path.join(ASSETS_DIR, "rr_banner.jpg"))
    b64_stadium = load_base64(os.path.join(ASSETS_DIR, "sawai_mansingh_stadium.jpg"))

    # Figures
    b64_donut = load_base64(os.path.join(FIGURES_DIR, "pressure_donut.png"))
    b64_batting_front = load_base64(os.path.join(FIGURES_DIR, "batting_frontier.png"))
    b64_bowling_front = load_base64(os.path.join(FIGURES_DIR, "bowling_frontier.png"))
    b64_clutch_delta = load_base64(os.path.join(FIGURES_DIR, "batting_clutch_delta.png"))
    b64_role_map = load_base64(os.path.join(FIGURES_DIR, "rr_squad_role_map.png"))
    b64_radar = load_base64(os.path.join(FIGURES_DIR, "auction_radar_comparison.png"))
    b64_bowling_diag = load_base64(os.path.join(FIGURES_DIR, "rr_bowling_diagnosis.png"))

    # Render HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajasthan Royals War Room • SupeRR Selector S2</title>
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
              navy: '#080F22',
              surface: '#111C35',
              surfaceElevated: '#162444',
              border: 'rgba(255, 255, 255, 0.08)',
              borderLight: 'rgba(255, 255, 255, 0.15)',
              pink: '#EA1B86',
              pinkHover: '#d01275',
              pinkGlow: 'rgba(234, 27, 134, 0.35)',
              blue: '#3156A5',
              gold: '#D4AF37',
              goldHover: '#c19b26',
              accentGreen: '#10B981',
              accentRed: '#EF4444'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background-color: #080F22;
      color: #F8FAFC;
      font-family: 'Plus Jakarta Sans', sans-serif;
      overflow-x: hidden;
    }}
    /* Custom Scrollbars */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #080F22;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1E2D5A;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #EA1B86;
    }}
    /* Nav Tab Active */
    .nav-link.active {{
      background: linear-gradient(90deg, rgba(234, 27, 134, 0.15) 0%, rgba(49, 86, 165, 0.08) 100%);
      border-left: 3px solid #EA1B86;
      color: #FFFFFF;
      font-weight: 700;
    }}
    .nav-link.active svg {{
      color: #EA1B86;
    }}
    /* Score Meter Bar */
    .meter-bar {{
      height: 6px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.1);
      overflow: hidden;
    }}
    .meter-fill {{
      height: 100%;
      border-radius: 9999px;
      transition: width 0.4s ease;
    }}
    /* Glass card */
    .glass-card {{
      background-color: #111C35;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 0.75rem;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .glass-card:hover {{
      border-color: rgba(234, 27, 134, 0.25);
    }}
    /* Badge styling */
    .badge-pink {{
      background: rgba(234, 27, 134, 0.15);
      color: #FF5EA7;
      border: 1px solid rgba(234, 27, 134, 0.3);
    }}
    .badge-blue {{
      background: rgba(49, 86, 165, 0.2);
      color: #93C5FD;
      border: 1px solid rgba(49, 86, 165, 0.4);
    }}
    .badge-gold {{
      background: rgba(212, 175, 55, 0.15);
      color: #FDE047;
      border: 1px solid rgba(212, 175, 55, 0.35);
    }}
    .badge-green {{
      background: rgba(16, 185, 129, 0.15);
      color: #6EE7B7;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-red {{
      background: rgba(239, 68, 68, 0.15);
      color: #FCA5A5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    /* Animated Pulse Glow */
    @keyframes pulseGlow {{
      0%, 100% {{ box-shadow: 0 0 15px rgba(234, 27, 134, 0.2); }}
      50% {{ box-shadow: 0 0 25px rgba(234, 27, 134, 0.4); }}
    }}
    .glow-pulse {{
      animation: pulseGlow 3s infinite;
    }}
    /* Modal transitions */
    .modal-backdrop {{
      background: rgba(8, 15, 34, 0.85);
      backdrop-filter: blur(8px);
    }}
    /* Tactical Ground Pitch Styling */
    .ground-oval {{
      background: radial-gradient(ellipse at center, #1b3d2f 0%, #102920 60%, #0d1e17 100%);
      border: 2px dashed rgba(255, 255, 255, 0.2);
      box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.6);
    }}
    .ground-pitch {{
      background: #73634e;
      border: 1px solid #998369;
    }}
  </style>
</head>

<body class="flex h-screen w-screen overflow-hidden text-slate-100 antialiased selection:bg-pink-500 selection:text-white">

  <!-- ========================================================================= -->
  <!-- PERSISTENT LEFT SIDEBAR                                                   -->
  <!-- ========================================================================= -->
  <aside class="w-64 flex-shrink-0 bg-[#0A1227] border-r border-slate-800/80 flex flex-col justify-between z-30 select-none">
    
    <!-- Top Franchise Brand Section -->
    <div>
      <div class="px-5 py-4 border-b border-slate-800/80 flex items-center space-x-3.5">
        <div class="relative w-11 h-11 flex-shrink-0 rounded-full p-0.5 bg-gradient-to-tr from-[#D4AF37] to-[#EA1B86] shadow-lg shadow-pink-600/20">
          <img src="{b64_crest or 'assets/rr_crest.jpg'}" alt="Rajasthan Royals Crest" class="w-full h-full object-cover rounded-full bg-[#001F5B]">
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <span class="font-extrabold tracking-wider text-sm text-white">RR WAR ROOM</span>
            <span class="text-[9px] font-black uppercase px-1.5 py-0.5 rounded bg-pink-500/20 text-pink-400 border border-pink-500/30">S2</span>
          </div>
          <p class="text-[11px] text-slate-400 font-medium">IPL 2027 Analytics Engine</p>
        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="p-3 space-y-1 text-xs font-semibold">
        <div class="px-3 pt-2 pb-1 text-[10px] uppercase font-bold tracking-widest text-slate-500">Modules</div>

        <!-- 01 Executive Overview -->
        <button onclick="switchModule('module-overview')" id="nav-module-overview" class="nav-link active w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 transition">
          <div class="flex items-center space-x-2.5">
            <svg class="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
            <span>01 Executive Overview</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-pink-500"></span>
        </button>

        <!-- 02 Batting Intelligence -->
        <button onclick="switchModule('module-batting')" id="nav-module-batting" class="nav-link w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition">
          <div class="flex items-center space-x-2.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            <span>02 Batting Intelligence</span>
          </div>
          <span class="text-[10px] font-mono text-slate-500">146</span>
        </button>

        <!-- 03 Bowling Intelligence -->
        <button onclick="switchModule('module-bowling')" id="nav-module-bowling" class="nav-link w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition">
          <div class="flex items-center space-x-2.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>03 Bowling Intelligence</span>
          </div>
          <span class="text-[10px] font-mono text-slate-500">158</span>
        </button>

        <!-- 04 Pressure Analytics Lab -->
        <button onclick="switchModule('module-lab')" id="nav-module-lab" class="nav-link w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition">
          <div class="flex items-center space-x-2.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <span>04 Pressure Lab &amp; Models</span>
          </div>
          <span class="text-[10px] font-mono px-1 rounded bg-blue-500/20 text-blue-300">WPA</span>
        </button>

        <!-- 05 RR Squad War Room -->
        <button onclick="switchModule('module-squad')" id="nav-module-squad" class="nav-link w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition">
          <div class="flex items-center space-x-2.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
            <span>05 RR Squad War Room</span>
          </div>
          <span class="text-[9px] font-bold px-1.5 py-0.5 rounded bg-pink-500/20 text-pink-400">-38.6%</span>
        </button>

        <!-- 06 Auction Intelligence Simulator -->
        <button onclick="switchModule('module-auction')" id="nav-module-auction" class="nav-link w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition">
          <div class="flex items-center space-x-2.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>06 Auction Simulator</span>
          </div>
          <span class="text-[10px] font-bold text-amber-400 font-mono">â‚¹35 Cr</span>
        </button>
      </nav>

      <!-- Quick Action Utilities -->
      <div class="p-3 pt-4 border-t border-slate-800/80 space-y-2">
        <button onclick="openReconciliationModal()" class="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 hover:text-white transition">
          <span class="flex items-center gap-2">
            <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            Match Reconciliation
          </span>
          <span class="text-[10px] font-mono text-slate-400">883 / 867</span>
        </button>

        <a href="SupeRR_Selector_Season2_RR_WarRoom_Report.pdf" target="_blank" class="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-500 hover:to-pink-600 text-xs font-bold text-white shadow-md shadow-pink-600/30 transition">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          Download PDF Report (9p)
        </a>
      </div>
    </div>

    <!-- Bottom Disclaimer Section -->
    <div class="p-4 border-t border-slate-800/80 bg-[#070D1D]">
      <div class="text-[10px] text-slate-400 leading-snug">
        <span class="font-bold text-slate-300">Independent Research Dossier</span><br>
        SupeRR Selector Season 2<br>
        <span class="text-slate-500">Not an official RR publication</span>
      </div>
    </div>
  </aside>

  <!-- ========================================================================= -->
  <!-- MAIN CONTENT AREA                                                         -->
  <!-- ========================================================================= -->
  <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
    
    <!-- Top Global App Bar -->
    <header class="h-16 flex-shrink-0 bg-[#0A1227]/90 backdrop-blur border-b border-slate-800/80 px-6 flex items-center justify-between z-20">
      
      <!-- Left: Breadcrumb & Model Indicator -->
      <div class="flex items-center space-x-4">
        <div>
          <div class="text-[10px] uppercase font-bold tracking-wider text-slate-500 flex items-center gap-1.5">
            <span>Rajasthan Royals</span>
            <span>&rsaquo;</span>
            <span class="text-pink-400">War Room Dossier</span>
            <span>&rsaquo;</span>
            <span id="breadcrumb-current" class="text-slate-300">01 Executive Overview</span>
          </div>
          <h2 id="header-title" class="text-base font-extrabold text-white tracking-tight">Executive Scouting &amp; Reliability Framework</h2>
        </div>
      </div>

      <!-- Right: Model Switcher & Dataset Badges -->
      <div class="flex items-center space-x-3 text-xs">
        
        <!-- PRS Model Selector Toggle -->
        <div class="flex items-center bg-slate-900 border border-slate-700/80 rounded-lg p-0.5 shadow-inner">
          <button onclick="setModel('calibrated')" id="btn-model-calibrated" class="px-2.5 py-1 rounded-md text-[11px] font-bold transition bg-gradient-to-r from-pink-600 to-pink-700 text-white shadow">
            Model B: Calibrated PRS
          </button>
          <button onclick="setModel('legacy')" id="btn-model-legacy" class="px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition">
            Model A: Legacy PRS
          </button>
        </div>

        <!-- Global Metrics Badges -->
        <div class="hidden lg:flex items-center space-x-1.5 font-mono text-[11px]">
          <span class="px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-800 text-slate-300">
            <b class="text-pink-400 font-sans">200,999</b> Balls
          </span>
          <button onclick="openReconciliationModal()" class="px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white transition flex items-center gap-1">
            <b class="text-blue-400 font-sans">867</b> Contested <span class="text-[9px] text-slate-400">(883 Sched)</span>
          </button>
          <span class="px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-800 text-slate-300">
            <b class="text-amber-400 font-sans">78,374</b> HP (39.0%)
          </span>
        </div>

      </div>
    </header>

    <!-- Scrollable Workspace Body -->
    <main class="flex-1 overflow-y-auto px-6 py-6 space-y-6">

      <!-- ===================================================================== -->
      <!-- MODULE 01: EXECUTIVE OVERVIEW                                         -->
      <!-- ===================================================================== -->
      <section id="module-overview" class="module-pane space-y-6">
        
        <!-- Hero Banner with Franchise Watermark -->
        <div class="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-r from-[#0F1E40] via-[#0E1B38] to-[#1E0F2B] p-6 shadow-xl">
          <div class="absolute -right-8 -bottom-10 w-72 h-72 opacity-15 pointer-events-none">
            <img src="{b64_crest or 'assets/rr_crest.jpg'}" alt="Watermark" class="w-full h-full object-contain filter grayscale invert">
          </div>
          <div class="relative z-10 max-w-3xl space-y-2">
            <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full badge-pink text-[11px] font-bold">
              <span class="w-1.5 h-1.5 rounded-full bg-pink-400 animate-ping"></span>
              IPL 2027 WAR ROOM SCOUTING AUDIT
            </div>
            <h1 class="text-2xl font-black text-white tracking-tight sm:text-3xl">
              Pressure Reliability Scoring &amp; Franchise War Room Dossier
            </h1>
            <p class="text-slate-300 text-xs sm:text-sm leading-relaxed">
              Evaluating <span class="text-pink-400 font-bold">200,999 deliveries</span> across 867 contested matches (2022–2026) to quantify clutch performance under crisis, death, and tight chases. Calibrated with Bayesian shrinkage and tournament quality factors to engineer Rajasthan Royals' championship squad for IPL 2027.
            </p>
          </div>
        </div>

        <!-- 5 Top KPI Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
          
          <div class="glass-card p-4">
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400">Total Deliveries</span>
            <div class="text-2xl font-black text-white mt-1 font-mono">200,999</div>
            <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
              <span class="text-pink-400 font-bold">867</span> Contested Matches
            </div>
          </div>

          <div class="glass-card p-4">
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400">High-Pressure Balls</span>
            <div class="text-2xl font-black text-pink-400 mt-1 font-mono">78,374</div>
            <div class="text-[11px] text-slate-400 mt-1">
              <b class="text-white">39.0%</b> of all deliveries
            </div>
          </div>

          <div class="glass-card p-4">
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400">Primary Ranking Model</span>
            <div class="text-base font-black text-blue-300 mt-2">Model B (Calibrated)</div>
            <div class="text-[11px] text-slate-400 mt-1">
              Bayesian Shrinkage + Quality
            </div>
          </div>

          <div class="glass-card p-4">
            <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400">Target Auction Purse</span>
            <div class="text-2xl font-black text-amber-400 mt-1 font-mono">â‚¹35.0 Cr</div>
            <div class="text-[11px] text-slate-400 mt-1">
              For 3 Essential Signings
            </div>
          </div>

          <div class="glass-card p-4 col-span-2 lg:col-span-1 border-pink-500/30 bg-gradient-to-br from-[#111C35] to-[#250F24]">
            <span class="text-[10px] uppercase font-bold tracking-wider text-pink-400">Critical RR Gap</span>
            <div class="text-2xl font-black text-red-400 mt-1 font-mono">-38.6%</div>
            <div class="text-[11px] text-slate-300 mt-1">
              Death Bowling Par Deficit
            </div>
          </div>

        </div>

        <!-- Two Column Deep Dive: Pressure Distribution & Executive Mandates -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          <!-- Left: Pressure Distribution & Methodology Trigger (5 Cols) -->
          <div class="lg:col-span-5 glass-card p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 class="text-sm font-bold text-white">Pressure Index Distribution</h3>
                <p class="text-[11px] text-slate-400">200,999 Deliveries by Match Leverage</p>
              </div>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded badge-blue">PI &ge; 50</span>
            </div>

            <div class="flex flex-col sm:flex-row items-center gap-4">
              <div class="w-40 h-40 flex-shrink-0 relative">
                <img src="{b64_donut or 'figures/pressure_donut.png'}" alt="Pressure Distribution Donut" class="w-full h-full object-contain rounded-lg">
              </div>
              <div class="space-y-2 text-xs flex-1">
                <div class="p-2 rounded bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span>
                    <span class="font-medium text-slate-200">High Pressure</span>
                  </div>
                  <span class="font-mono font-bold text-pink-400">39.0% (78,374)</span>
                </div>
                <div class="p-2 rounded bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                    <span class="font-medium text-slate-200">Medium Pressure</span>
                  </div>
                  <span class="font-mono font-bold text-blue-400">19.7% (39,673)</span>
                </div>
                <div class="p-2 rounded bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
                    <span class="font-medium text-slate-200">Low Pressure</span>
                  </div>
                  <span class="font-mono font-bold text-slate-400">41.3% (82,952)</span>
                </div>
              </div>
            </div>

            <div class="text-[11px] text-slate-400 bg-slate-900/80 p-3 rounded-lg border border-slate-800/80 leading-relaxed">
              <b class="text-slate-300">Operational Pressure Triggers:</b> Deliveries enter High Pressure when (1) Chase RRR &ge; 9.0, (2) Top-order crisis collapses (&le;30 runs for 3+ wickets), or (3) Death overs (16–20) with win margin within 30 runs.
            </div>
          </div>

          <!-- Right: The 3 Executive Strategic Mandates (7 Cols) -->
          <div class="lg:col-span-7 glass-card p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 class="text-sm font-bold text-white">War Room Strategic Directives (IPL 2027)</h3>
                <p class="text-[11px] text-slate-400">Evidence-Based Franchise Execution Plan</p>
              </div>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded badge-pink">PRIORITY 1-2-3</span>
            </div>

            <div class="grid grid-cols-1 gap-3 text-xs">
              
              <!-- Directive 1 -->
              <div class="p-3 rounded-lg bg-slate-900/70 border border-slate-800 hover:border-pink-500/40 transition flex gap-3">
                <div class="w-7 h-7 rounded-md bg-pink-500/20 text-pink-400 font-black flex items-center justify-center flex-shrink-0 text-sm">
                  1
                </div>
                <div class="space-y-1">
                  <div class="font-bold text-white flex items-center gap-2">
                    Retain &amp; Back Vaibhav Sooryavanshi (#1 Overall Batter)
                    <span class="badge-green px-1.5 py-0.5 rounded text-[9px] font-bold">RR SQUAD</span>
                  </div>
                  <p class="text-slate-300 text-[11px] leading-relaxed">
                    At Calibrated PRS <b class="text-pink-400">77.62</b> and an extraordinary HP Strike Rate of <b class="text-white">240.82</b>, Sooryavanshi provides rare pressure strike capability. Pair him with Yashasvi Jaiswal for the tournament's most lethal left-hand opening combination.
                  </p>
                </div>
              </div>

              <!-- Directive 2 -->
              <div class="p-3 rounded-lg bg-slate-900/70 border border-slate-800 hover:border-pink-500/40 transition flex gap-3">
                <div class="w-7 h-7 rounded-md bg-pink-500/20 text-pink-400 font-black flex items-center justify-center flex-shrink-0 text-sm">
                  2
                </div>
                <div class="space-y-1">
                  <div class="font-bold text-white flex items-center gap-2">
                    Acquire Matheesha Pathirana as Primary Death Specialist
                    <span class="badge-gold px-1.5 py-0.5 rounded text-[9px] font-bold">TARGET: â‚¹12.0 - 14.5 Cr</span>
                  </div>
                  <p class="text-slate-300 text-[11px] leading-relaxed">
                    Directly addresses Rajasthan Royals' catastrophic <b class="text-red-400">-38.6% death bowling leak</b> (where Curran and Deshpande conceded &gt;9.8 RPO). Pathirana's 10.31 bowling strike rate and 40.3% dot-ball rate will lock down overs 18 &amp; 20.
                  </p>
                </div>
              </div>

              <!-- Directive 3 -->
              <div class="p-3 rounded-lg bg-slate-900/70 border border-slate-800 hover:border-pink-500/40 transition flex gap-3">
                <div class="w-7 h-7 rounded-md bg-pink-500/20 text-pink-400 font-black flex items-center justify-center flex-shrink-0 text-sm">
                  3
                </div>
                <div class="space-y-1">
                  <div class="font-bold text-white flex items-center gap-2">
                    Secure Mitchell Santner &amp; Ashutosh Sharma for Tactical Balance
                    <span class="badge-blue px-1.5 py-0.5 rounded text-[9px] font-bold">TARGET: â‚¹11.5 - 15.0 Cr</span>
                  </div>
                  <p class="text-slate-300 text-[11px] leading-relaxed">
                    Santner (PRS 63.64, 6.45 Econ) provides middle-overs spin choke and batting at No. 8. Ashutosh Sharma (PRS 67.65, +58.22 Clutch Delta) provides elite boundary acceleration at No. 6/7 alongside Dhruv Jurel.
                  </p>
                </div>
              </div>

            </div>
          </div>

        </div>

        <!-- Featured Player Showcase Grid (Photos & Badges) -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white tracking-wide uppercase">Core Target &amp; Performer Profiles</h3>
            <span class="text-xs text-slate-400">Photographs from official franchise player databases</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <!-- Vaibhav Sooryavanshi -->
            <div class="glass-card overflow-hidden group hover:border-pink-500/50 transition">
              <div class="h-44 bg-slate-900 relative overflow-hidden">
                <img src="{b64_vaibhav or 'assets/vaibhav_sooryavanshi.jpg'}" alt="Vaibhav Sooryavanshi" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-300">
                <div class="absolute inset-0 bg-gradient-to-t from-[#111C35] via-transparent to-transparent"></div>
                <span class="absolute top-2.5 left-2.5 badge-pink text-[10px] font-black px-2 py-0.5 rounded">#1 BATTER OVERALL</span>
                <span class="absolute bottom-2 right-2.5 text-xs font-mono font-bold text-pink-400">PRS 77.62</span>
              </div>
              <div class="p-3.5 space-y-2">
                <div>
                  <h4 class="font-bold text-white text-sm">Vaibhav Sooryavanshi</h4>
                  <p class="text-[11px] text-slate-400">Top-Order Aggressor • RR Incumbent</p>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] pt-1 border-t border-slate-800">
                  <div>
                    <span class="text-slate-400">HP SR:</span> <b class="text-white font-mono">240.82</b>
                  </div>
                  <div>
                    <span class="text-slate-400">HP Avg:</span> <b class="text-white font-mono">42.91</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Clutch &Delta;:</span> <b class="text-emerald-400 font-mono">+24.77</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Bounds:</span> <b class="text-white font-mono">42.9%</b>
                  </div>
                </div>
                <button onclick="inspectPlayer(50284, 'batter')" class="w-full py-1.5 mt-1 rounded bg-slate-900 border border-slate-800 hover:border-pink-500 text-xs font-semibold text-slate-200 hover:text-white transition">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

            <!-- Ashutosh Sharma -->
            <div class="glass-card overflow-hidden group hover:border-pink-500/50 transition">
              <div class="h-44 bg-slate-900 relative overflow-hidden">
                <img src="{b64_ashutosh or 'assets/ashutosh_sharma.jpg'}" alt="Ashutosh Sharma" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-300">
                <div class="absolute inset-0 bg-gradient-to-t from-[#111C35] via-transparent to-transparent"></div>
                <span class="absolute top-2.5 left-2.5 badge-gold text-[10px] font-black px-2 py-0.5 rounded">#1 CLUTCH FINISHER</span>
                <span class="absolute bottom-2 right-2.5 text-xs font-mono font-bold text-amber-400">PRS 67.65</span>
              </div>
              <div class="p-3.5 space-y-2">
                <div>
                  <h4 class="font-bold text-white text-sm">Ashutosh Sharma</h4>
                  <p class="text-[11px] text-slate-400">Designated Finisher • Auction Target</p>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] pt-1 border-t border-slate-800">
                  <div>
                    <span class="text-slate-400">HP SR:</span> <b class="text-white font-mono">189.10</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Clutch &Delta;:</span> <b class="text-emerald-400 font-mono">+58.22</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Dot %:</span> <b class="text-white font-mono">27.0%</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Target:</span> <b class="text-amber-400 font-mono">â‚¹5 - 7 Cr</b>
                  </div>
                </div>
                <button onclick="inspectPlayer(24707, 'batter')" class="w-full py-1.5 mt-1 rounded bg-slate-900 border border-slate-800 hover:border-pink-500 text-xs font-semibold text-slate-200 hover:text-white transition">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

            <!-- Matheesha Pathirana -->
            <div class="glass-card overflow-hidden group hover:border-pink-500/50 transition">
              <div class="h-44 bg-slate-900 relative overflow-hidden">
                <img src="{b64_pathirana or 'assets/matheesha_pathirana.jpg'}" alt="Matheesha Pathirana" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-300">
                <div class="absolute inset-0 bg-gradient-to-t from-[#111C35] via-transparent to-transparent"></div>
                <span class="absolute top-2.5 left-2.5 badge-pink text-[10px] font-black px-2 py-0.5 rounded">#1 DEATH CLOSER</span>
                <span class="absolute bottom-2 right-2.5 text-xs font-mono font-bold text-pink-400">PRS 60.75</span>
              </div>
              <div class="p-3.5 space-y-2">
                <div>
                  <h4 class="font-bold text-white text-sm">Matheesha Pathirana</h4>
                  <p class="text-[11px] text-slate-400">Express Slinger • Primary Auction Target</p>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] pt-1 border-t border-slate-800">
                  <div>
                    <span class="text-slate-400">HP Wkts:</span> <b class="text-white font-mono">51</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Bowling SR:</span> <b class="text-emerald-400 font-mono">10.31</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Econ:</span> <b class="text-white font-mono">7.78</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Target:</span> <b class="text-amber-400 font-mono">â‚¹12 - 14.5 Cr</b>
                  </div>
                </div>
                <button onclick="inspectPlayer(24070, 'bowler')" class="w-full py-1.5 mt-1 rounded bg-slate-900 border border-slate-800 hover:border-pink-500 text-xs font-semibold text-slate-200 hover:text-white transition">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

            <!-- Mitchell Santner -->
            <div class="glass-card overflow-hidden group hover:border-pink-500/50 transition">
              <div class="h-44 bg-slate-900 relative overflow-hidden">
                <img src="{b64_santner or 'assets/mitchell_santner.jpg'}" alt="Mitchell Santner" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-300">
                <div class="absolute inset-0 bg-gradient-to-t from-[#111C35] via-transparent to-transparent"></div>
                <span class="absolute top-2.5 left-2.5 badge-blue text-[10px] font-black px-2 py-0.5 rounded">#1 SPIN SQUEEZER</span>
                <span class="absolute bottom-2 right-2.5 text-xs font-mono font-bold text-blue-400">PRS 63.64</span>
              </div>
              <div class="p-3.5 space-y-2">
                <div>
                  <h4 class="font-bold text-white text-sm">Mitchell Santner</h4>
                  <p class="text-[11px] text-slate-400">Left-Arm Spin • Tactical Auction Target</p>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] pt-1 border-t border-slate-800">
                  <div>
                    <span class="text-slate-400">HP Econ:</span> <b class="text-emerald-400 font-mono">6.45</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Chase WPA:</span> <b class="text-white font-mono">+2.25</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Dot %:</span> <b class="text-white font-mono">42.3%</b>
                  </div>
                  <div>
                    <span class="text-slate-400">Target:</span> <b class="text-amber-400 font-mono">â‚¹6.5 - 8 Cr</b>
                  </div>
                </div>
                <button onclick="inspectPlayer(1469, 'bowler')" class="w-full py-1.5 mt-1 rounded bg-slate-900 border border-slate-800 hover:border-pink-500 text-xs font-semibold text-slate-200 hover:text-white transition">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

          </div>
        </div>

      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 02: BATTING INTELLIGENCE                                       -->
      <!-- ===================================================================== -->
      <section id="module-batting" class="module-pane hidden space-y-6">
        
        <!-- Filter and Search Header -->
        <div class="glass-card p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex-1 flex flex-wrap items-center gap-3">
            
            <!-- Search input -->
            <div class="relative w-64">
              <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <input type="text" id="batting-search" placeholder="Search 146 qualified batters..." oninput="filterBatters()" class="w-full pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-pink-500">
            </div>

            <!-- Sample Size Slider -->
            <div class="flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1 rounded-lg text-xs">
              <span class="text-slate-400">Min Balls:</span>
              <input type="range" id="batting-min-balls" min="80" max="300" value="120" step="10" oninput="updateBattingMinBalls(this.value)" class="w-20 accent-pink-500">
              <span id="batting-min-balls-val" class="font-mono font-bold text-pink-400">120</span>
            </div>

            <!-- Auction Eligibility Filter -->
            <select id="batting-eligibility" onchange="filterBatters()" class="bg-slate-900 border border-slate-800 text-slate-300 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-pink-500">
              <option value="all">All Batters (146)</option>
              <option value="eligible">Auction Eligible Only</option>
              <option value="ipl">Active IPL Players</option>
            </select>

          </div>

          <div class="flex items-center space-x-2 text-xs font-medium text-slate-400">
            <span>Showing <b id="batting-count" class="text-white font-mono">146</b> qualified batters</span>
          </div>
        </div>

        <!-- Interactive Batting Table -->
        <div class="glass-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-900/90 border-b border-slate-800 text-[10px] uppercase font-bold text-slate-400 tracking-wider">
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
              <tbody id="batting-table-body" class="divide-y divide-slate-800/60 text-xs font-medium">
                <!-- Injected via JavaScript -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Frontier Scatter Chart Graphic & Analysis -->
        <div class="glass-card p-5 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-sm font-bold text-white">Batting Efficiency Frontier: Strike Rate vs Average</h3>
              <p class="text-[11px] text-slate-400">Bubble size scaled to High-Pressure deliveries faced</p>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded badge-pink">EVALUATION FRONTIER</span>
          </div>
          <div class="h-80 w-full flex items-center justify-center bg-slate-900/50 rounded-lg p-2">
            <img src="{b64_batting_front or 'figures/batting_frontier.png'}" alt="Batting Frontier" class="max-h-full max-w-full object-contain rounded">
          </div>
        </div>

      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 03: BOWLING INTELLIGENCE                                       -->
      <!-- ===================================================================== -->
      <section id="module-bowling" class="module-pane hidden space-y-6">
        
        <!-- Filter Bar -->
        <div class="glass-card p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex-1 flex flex-wrap items-center gap-3">
            
            <!-- Search -->
            <div class="relative w-64">
              <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <input type="text" id="bowling-search" placeholder="Search 158 qualified bowlers..." oninput="filterBowlers()" class="w-full pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-pink-500">
            </div>

            <!-- Min Balls -->
            <div class="flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1 rounded-lg text-xs">
              <span class="text-slate-400">Min Balls:</span>
              <input type="range" id="bowling-min-balls" min="80" max="300" value="120" step="10" oninput="updateBowlingMinBalls(this.value)" class="w-20 accent-pink-500">
              <span id="bowling-min-balls-val" class="font-mono font-bold text-pink-400">120</span>
            </div>

            <!-- Auction Eligibility Filter -->
            <select id="bowling-eligibility" onchange="filterBowlers()" class="bg-slate-900 border border-slate-800 text-slate-300 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-pink-500">
              <option value="eligible">Auction Eligible Candidates (BCCI Compliant)</option>
              <option value="all">All Bowlers (Including PSL/Policy-Excluded)</option>
            </select>

          </div>

          <div class="flex items-center space-x-2 text-xs font-medium text-slate-400">
            <span>Showing <b id="bowling-count" class="text-white font-mono">158</b> qualified bowlers</span>
          </div>
        </div>

        <!-- Policy Note Callout -->
        <div class="p-3.5 rounded-lg bg-blue-950/40 border border-blue-800/60 text-xs flex items-start gap-3">
          <svg class="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <div class="text-slate-300 text-[11px] leading-relaxed">
            <span class="font-bold text-blue-300">IPL Auction Eligibility Disclosure:</span> Bowlers like Sufiyan Muqeem (PRS 85.15) and Shaheen Shah Afridi (PRS 61.72) are marked as <span class="badge-red px-1 rounded font-mono">INELIGIBLE_POLICY_EXCLUDED</span> per BCCI IPL regulations. In the official auction draft rankings, <b class="text-white">Sunil Narine (PRS 64.41)</b> is Rank #1 and <b class="text-white">Mitchell Santner (PRS 63.83)</b> is Rank #2.
          </div>
        </div>

        <!-- Interactive Bowling Table -->
        <div class="glass-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-900/90 border-b border-slate-800 text-[10px] uppercase font-bold text-slate-400 tracking-wider">
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
              <tbody id="bowling-table-body" class="divide-y divide-slate-800/60 text-xs font-medium">
                <!-- Injected via JavaScript -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Bowling Frontier Visualization -->
        <div class="glass-card p-5 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-sm font-bold text-white">Bowling Efficiency Frontier: Economy vs Strike Rate</h3>
              <p class="text-[11px] text-slate-400">Bottom-left quadrant denotes elite pressure wicket-takers and run suppressors</p>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded badge-blue">BOWLING FRONTIER</span>
          </div>
          <div class="h-80 w-full flex items-center justify-center bg-slate-900/50 rounded-lg p-2">
            <img src="{b64_bowling_front or 'figures/bowling_frontier.png'}" alt="Bowling Frontier" class="max-h-full max-w-full object-contain rounded">
          </div>
        </div>

      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 04: PRESSURE ANALYTICS LAB                                     -->
      <!-- ===================================================================== -->
      <section id="module-lab" class="module-pane hidden space-y-6">
        
        <!-- Methodology Pillars Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <div class="glass-card p-4 space-y-2">
            <div class="flex items-center justify-between">
              <span class="badge-pink text-[10px] font-bold px-2 py-0.5 rounded">PI ENGINE</span>
              <span class="text-[10px] font-mono text-slate-500">Tier 1</span>
            </div>
            <h4 class="font-bold text-white text-sm">Pressure Index (PI) Formulation</h4>
            <p class="text-slate-400 text-xs leading-relaxed">
              Synthesizes match situation across required run rate (RRR), wicket clusters (crisis collapses &le;30/3), and late-innings leverage into a continuous metric \(PI_i \in [0, 100]\). Deliveries with \(PI_i \ge 50\) represent 39.0% of all balls.
            </p>
          </div>

          <div class="glass-card p-4 space-y-2">
            <div class="flex items-center justify-between">
              <span class="badge-blue text-[10px] font-bold px-2 py-0.5 rounded">WPA LOGISTIC</span>
              <span class="text-[10px] font-mono text-slate-500">AUC = 0.8966</span>
            </div>
            <h4 class="font-bold text-white text-sm">Win Probability Added (WPA)</h4>
            <p class="text-slate-400 text-xs leading-relaxed">
              Trained on all 95,272 2nd-innings chasing deliveries to track delta win equity. First innings is evaluated via crisis and death par benchmarks. WPA rates use chase balls as denominator to avoid sample skew.
            </p>
          </div>

          <div class="glass-card p-4 space-y-2">
            <div class="flex items-center justify-between">
              <span class="badge-gold text-[10px] font-bold px-2 py-0.5 rounded">BAYESIAN &amp; QUALITY</span>
              <span class="text-[10px] font-mono text-slate-500">k = 80 Balls</span>
            </div>
            <h4 class="font-bold text-white text-sm">Shrinkage &amp; Competition Scaling</h4>
            <p class="text-slate-400 text-xs leading-relaxed">
              Dampens small sample anomalies toward league prior means, and scales competition quality (IPL 1.00&times;, Tier-1 T20I 0.90&times;, Associate 0.75&times;) to prevent lower-league inflation.
            </p>
          </div>

        </div>

        <!-- Visual Analytics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Clutch Delta Bar Chart -->
          <div class="glass-card p-4 space-y-3">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <h4 class="text-xs font-bold text-white uppercase tracking-wider">Batting Clutch Delta (&Delta;SR)</h4>
              <span class="text-[10px] text-slate-400 font-mono">Pressure SR - Base SR</span>
            </div>
            <div class="h-64 flex items-center justify-center">
              <img src="{b64_clutch_delta or 'figures/batting_clutch_delta.png'}" alt="Clutch Delta" class="max-h-full max-w-full object-contain rounded">
            </div>
            <p class="text-[11px] text-slate-400">
              Ashutosh Sharma (+58.22) and Dinesh Karthik (+49.99) demonstrate extraordinary acceleration under high leverage.
            </p>
          </div>

          <!-- RR Bowling Diagnosis -->
          <div class="glass-card p-4 space-y-3">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <h4 class="text-xs font-bold text-white uppercase tracking-wider">RR Bowling Phase Economy Audit</h4>
              <span class="text-[10px] badge-red px-2 py-0.5 rounded font-mono">Death Deficit</span>
            </div>
            <div class="h-64 flex items-center justify-center">
              <img src="{b64_bowling_diag or 'figures/rr_bowling_diagnosis.png'}" alt="Bowling Diagnosis" class="max-h-full max-w-full object-contain rounded">
            </div>
            <p class="text-[11px] text-slate-400">
              RR's 2026 death overs economy leaked at 10.12 RPO, falling 38.6% below league par.
            </p>
          </div>

        </div>

      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 05: RAJASTHAN ROYALS SQUAD WAR ROOM                            -->
      <!-- ===================================================================== -->
      <section id="module-squad" class="module-pane hidden space-y-6">
        
        <!-- Phase Efficiency Diagnosis Banner -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="glass-card p-4 border-l-4 border-emerald-500">
            <div class="text-[10px] uppercase font-bold text-slate-400">Powerplay Phase (Overs 1-6)</div>
            <div class="text-2xl font-black text-emerald-400 mt-1 font-mono">+18.2%</div>
            <div class="text-[11px] text-slate-300 mt-1">Above League Par (Jaiswal &amp; Sooryavanshi)</div>
          </div>

          <div class="glass-card p-4 border-l-4 border-blue-500">
            <div class="text-[10px] uppercase font-bold text-slate-400">Middle Phase (Overs 7-15)</div>
            <div class="text-2xl font-black text-blue-400 mt-1 font-mono">+4.1%</div>
            <div class="text-[11px] text-slate-300 mt-1">Controlled Tempo (Samson &amp; Parag)</div>
          </div>

          <div class="glass-card p-4 border-l-4 border-pink-500 bg-pink-950/20">
            <div class="text-[10px] uppercase font-bold text-pink-400">Death Phase (Overs 16-20)</div>
            <div class="text-2xl font-black text-pink-500 mt-1 font-mono">-38.6%</div>
            <div class="text-[11px] text-red-300 mt-1">Catastrophic Bowling Leak (Curran/Deshpande)</div>
          </div>
        </div>

        <!-- Tactical Cricket Ground Pitch Oval & Projected Best XI -->
        <div class="glass-card p-5 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                Projected Best XI: Tactical Field Formation (IPL 2027)
                <span class="badge-gold px-2 py-0.5 rounded text-[9px] font-bold">WAR ROOM SIMULATION</span>
              </h3>
              <p class="text-[11px] text-slate-400">Hypothetical scenario incorporating target auction acquisitions</p>
            </div>
            <span class="text-[10px] font-mono px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400">Sawai Mansingh Stadium Par: 178</span>
          </div>

          <!-- Cricket Oval Visualization -->
          <div class="ground-oval rounded-2xl p-6 relative overflow-hidden flex flex-col items-center justify-center min-h-[380px]">
            
            <!-- Pitch in center -->
            <div class="ground-pitch w-24 h-48 rounded shadow-2xl relative flex flex-col justify-between py-2 items-center">
              <div class="w-16 h-1 bg-white/70"></div>
              <div class="text-[9px] font-mono text-white/60 tracking-widest uppercase">PITCH</div>
              <div class="w-16 h-1 bg-white/70"></div>
            </div>

            <!-- Positioned Players Overlay Grid -->
            <div class="absolute inset-0 p-4 grid grid-cols-3 grid-rows-4 pointer-events-none text-center text-xs">
              
              <!-- Row 1: Deep Boundary & Openers -->
              <div class="flex items-start justify-center">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-pink-500/60 text-white font-bold shadow-lg">
                  1. Y. Jaiswal (LH Opener)
                </span>
              </div>
              <div class="flex items-start justify-center">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-pink-500/60 text-white font-bold shadow-lg">
                  2. V. Sooryavanshi (LH Aggressor • PRS 77.62)
                </span>
              </div>
              <div class="flex items-start justify-center">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-slate-200 font-bold shadow-lg">
                  3. S. Samson (C / WK)
                </span>
              </div>

              <!-- Row 2: Middle Order Anchors -->
              <div class="flex items-center justify-start pl-6">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-slate-200 font-bold shadow-lg">
                  4. R. Parag (RH Anchor)
                </span>
              </div>
              <div></div>
              <div class="flex items-center justify-end pr-6">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-slate-200 font-bold shadow-lg">
                  5. D. Jurel (Crisis Finisher)
                </span>
              </div>

              <!-- Row 3: Clutch Targets & All-Rounders -->
              <div class="flex items-center justify-start pl-6">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-pink-900/90 border border-pink-400 text-pink-200 font-black shadow-lg">
                  6. Ashutosh Sharma (TARGET • Finisher)
                </span>
              </div>
              <div></div>
              <div class="flex items-center justify-end pr-6">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-slate-200 font-bold shadow-lg">
                  7. R. Jadeja (All-Rounder)
                </span>
              </div>

              <!-- Row 4: Bowling Attack & Closers -->
              <div class="flex items-end justify-center">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-blue-900/90 border border-blue-400 text-blue-200 font-black shadow-lg">
                  8. M. Santner (TARGET • Spin)
                </span>
              </div>
              <div class="flex items-end justify-center gap-2">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-slate-200 font-bold shadow-lg">
                  9. J. Archer (Pace)
                </span>
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-pink-900/90 border border-pink-400 text-pink-200 font-black shadow-lg">
                  10. M. Pathirana (TARGET • Closer)
                </span>
              </div>
              <div class="flex items-end justify-center">
                <span class="pointer-events-auto px-2 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-slate-200 font-bold shadow-lg">
                  11. S. Sharma / T. Deshpande
                </span>
              </div>

            </div>
          </div>
        </div>

        <!-- Squad Audit Table -->
        <div class="glass-card overflow-hidden">
          <div class="px-5 py-3 border-b border-slate-800 flex items-center justify-between">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider">Current Squad Pressure Reliability Audit</h4>
            <span class="text-xs text-slate-400">27 Players Audited</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-900/80 text-[10px] uppercase font-bold text-slate-400 border-b border-slate-800">
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
              <tbody id="squad-table-body" class="divide-y divide-slate-800/60 font-medium">
                <!-- Injected via JavaScript -->
              </tbody>
            </table>
          </div>
        </div>

      </section>

      <!-- ===================================================================== -->
      <!-- MODULE 06: AUCTION INTELLIGENCE SIMULATOR                             -->
      <!-- ===================================================================== -->
      <section id="module-auction" class="module-pane hidden space-y-6">
        
        <!-- Budget Planner & Allocation Simulator -->
        <div class="glass-card p-5 space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                Auction Purse Allocation Planner (â‚¹35.0 Cr War Chest)
                <span class="badge-gold px-2 py-0.5 rounded text-[9px] font-bold">INTERACTIVE SIMULATOR</span>
              </h3>
              <p class="text-[11px] text-slate-400">Simulate winning bids for target players and evaluate remaining purse headroom</p>
            </div>
            
            <div class="flex items-center space-x-3 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-lg text-xs font-mono">
              <span class="text-slate-400">Remaining Purse:</span>
              <span id="sim-remaining-purse" class="text-base font-black text-emerald-400">â‚¹7.50 Cr</span>
            </div>
          </div>

          <!-- Interactive Bidding Sliders -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- Pathirana -->
            <div class="p-3.5 rounded-lg bg-slate-900/70 border border-slate-800 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">Matheesha Pathirana</span>
                <span id="val-sim-pathirana" class="font-mono font-bold text-pink-400">â‚¹13.50 Cr</span>
              </div>
              <input type="range" id="slider-pathirana" min="9.0" max="18.0" step="0.25" value="13.50" oninput="updateAuctionSimulator()" class="w-full accent-pink-500">
              <div class="text-[10px] text-slate-400 flex justify-between">
                <span>Min: â‚¹9 Cr</span>
                <span>Base Target: â‚¹12 - 14.5 Cr</span>
                <span>Max: â‚¹18 Cr</span>
              </div>
            </div>

            <!-- Santner -->
            <div class="p-3.5 rounded-lg bg-slate-900/70 border border-slate-800 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">Mitchell Santner</span>
                <span id="val-sim-santner" class="font-mono font-bold text-blue-400">â‚¹7.50 Cr</span>
              </div>
              <input type="range" id="slider-santner" min="4.0" max="11.0" step="0.25" value="7.50" oninput="updateAuctionSimulator()" class="w-full accent-blue-500">
              <div class="text-[10px] text-slate-400 flex justify-between">
                <span>Min: â‚¹4 Cr</span>
                <span>Base Target: â‚¹6.5 - 8 Cr</span>
                <span>Max: â‚¹11 Cr</span>
              </div>
            </div>

            <!-- Ashutosh -->
            <div class="p-3.5 rounded-lg bg-slate-900/70 border border-slate-800 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">Ashutosh Sharma</span>
                <span id="val-sim-ashutosh" class="font-mono font-bold text-amber-400">â‚¹6.50 Cr</span>
              </div>
              <input type="range" id="slider-ashutosh" min="3.0" max="10.0" step="0.25" value="6.50" oninput="updateAuctionSimulator()" class="w-full accent-amber-500">
              <div class="text-[10px] text-slate-400 flex justify-between">
                <span>Min: â‚¹3 Cr</span>
                <span>Base Target: â‚¹5 - 7 Cr</span>
                <span>Max: â‚¹10 Cr</span>
              </div>
            </div>

          </div>

          <!-- Strategic Presets -->
          <div class="flex flex-wrap items-center gap-2 pt-2">
            <span class="text-[11px] text-slate-400 font-medium">Strategy Presets:</span>
            <button onclick="setSimPreset(14.0, 7.5, 6.0)" class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 hover:border-pink-500 text-xs text-slate-300 hover:text-white transition">
              Scenario A: Pathirana Aggressive
            </button>
            <button onclick="setSimPreset(12.0, 8.5, 7.0)" class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 hover:border-blue-500 text-xs text-slate-300 hover:text-white transition">
              Scenario B: Balanced Core Spread
            </button>
            <button onclick="setSimPreset(10.0, 9.0, 8.0)" class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 hover:border-amber-500 text-xs text-slate-300 hover:text-white transition">
              Scenario C: Indian Finisher Priority
            </button>
          </div>
        </div>

        <!-- 3-Player Dynamic Comparison Tool -->
        <div class="glass-card p-5 space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                Dynamic 3-Player Side-by-Side Comparison
                <span class="badge-pink px-2 py-0.5 rounded text-[9px] font-bold">WAR ROOM COMPARATOR</span>
              </h3>
              <p class="text-[11px] text-slate-400">Select any 3 players to evaluate pressure radar metrics head-to-head</p>
            </div>
          </div>

          <!-- Selectors Row -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-[11px] text-slate-400 font-semibold mb-1">Player 1 (Target Closer)</label>
              <select id="compare-p1" onchange="updateComparison()" class="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-pink-500">
                <!-- Injected via JS -->
              </select>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 font-semibold mb-1">Player 2 (Alternative / Competitor)</label>
              <select id="compare-p2" onchange="updateComparison()" class="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-pink-500">
                <!-- Injected via JS -->
              </select>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 font-semibold mb-1">Player 3 (RR Incumbent)</label>
              <select id="compare-p3" onchange="updateComparison()" class="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-pink-500">
                <!-- Injected via JS -->
              </select>
            </div>
          </div>

          <!-- Comparison Display Grid -->
          <div id="comparison-display-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <!-- Injected via JS -->
          </div>

          <!-- Embedded Static Radar Figure as Reference -->
          <div class="pt-4 border-t border-slate-800 flex flex-col items-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold tracking-wider mb-2">Multivariate Target Comparison Radar (Pathirana vs Santner vs Incumbents)</span>
            <div class="h-64 w-full flex items-center justify-center bg-slate-900/40 rounded-lg p-2">
              <img src="{b64_radar or 'figures/auction_radar_comparison.png'}" alt="Auction Radar Comparison" class="max-h-full max-w-full object-contain rounded">
            </div>
          </div>

        </div>

      </section>

    </main>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: PLAYER DETAIL INSPECTION (JOS BUTTLER STYLE)                      -->
  <!-- ========================================================================= -->
  <div id="player-modal" class="fixed inset-0 z-50 modal-backdrop hidden flex items-center justify-center p-4">
    <div class="glass-card max-w-xl w-full p-6 relative border-pink-500/40 shadow-2xl bg-[#0D1836] space-y-4 max-h-[90vh] overflow-y-auto">
      
      <!-- Close button -->
      <button onclick="closePlayerModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>

      <!-- Player Header with Photo / Monogram -->
      <div class="flex items-center space-x-4 border-b border-slate-800 pb-4">
        <div id="modal-player-img-container" class="w-16 h-16 rounded-full overflow-hidden border-2 border-pink-500 flex-shrink-0 bg-slate-900 flex items-center justify-center">
          <span id="modal-player-initials" class="font-black text-xl text-white"></span>
        </div>
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <h3 id="modal-player-name" class="text-lg font-black text-white"></h3>
            <span id="modal-player-role-badge" class="badge-pink text-[10px] font-bold px-2 py-0.5 rounded"></span>
          </div>
          <p id="modal-player-eligibility" class="text-xs text-slate-400"></p>
        </div>
      </div>

      <!-- Key Performance Badges Grid -->
      <div id="modal-player-metrics-grid" class="grid grid-cols-3 gap-3">
        <!-- Injected via JS -->
      </div>

      <!-- Tactical War Room Verdict -->
      <div class="p-3.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1.5">
        <div class="text-[10px] uppercase font-bold text-pink-400 tracking-wider">War Room Scouting Assessment</div>
        <p id="modal-player-verdict" class="text-xs text-slate-300 leading-relaxed"></p>
      </div>

      <div class="pt-2 flex justify-end">
        <button onclick="closePlayerModal()" class="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white transition">
          Close Dossier
        </button>
      </div>

    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: MATCH COUNT RECONCILIATION AUDIT                                   -->
  <!-- ========================================================================= -->
  <div id="reconciliation-modal" class="fixed inset-0 z-50 modal-backdrop hidden flex items-center justify-center p-4">
    <div class="glass-card max-w-2xl w-full p-6 relative border-blue-500/40 shadow-2xl bg-[#0D1836] space-y-4 max-h-[90vh] overflow-y-auto">
      
      <button onclick="closeReconciliationModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>

      <div class="border-b border-slate-800 pb-3">
        <h3 class="text-base font-black text-white flex items-center gap-2">
          Dataset Match Count Reconciliation &amp; Audit
          <span class="badge-blue text-[10px] font-bold px-2 py-0.5 rounded">VERIFIED AUDIT</span>
        </h3>
        <p class="text-xs text-slate-400 mt-0.5">Reconciling the 883 scheduled matches vs 867 contested matches in the proprietary delivery dataset</p>
      </div>

      <div class="grid grid-cols-3 gap-3 text-center">
        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div class="text-[10px] uppercase text-slate-400 font-bold">Scheduled Matches</div>
          <div class="text-xl font-black text-white font-mono mt-1">883</div>
          <div class="text-[10px] text-slate-500">matches.csv registry</div>
        </div>
        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div class="text-[10px] uppercase text-slate-400 font-bold">Contested Matches</div>
          <div class="text-xl font-black text-pink-400 font-mono mt-1">867</div>
          <div class="text-[10px] text-slate-500">ball_by_ball.csv deliveries</div>
        </div>
        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div class="text-[10px] uppercase text-slate-400 font-bold">Abandoned Matches</div>
          <div class="text-xl font-black text-amber-400 font-mono mt-1">16</div>
          <div class="text-[10px] text-slate-500">0 balls bowled (Rain/Washouts)</div>
        </div>
      </div>

      <div class="space-y-2 text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
        <p><b class="text-white">Audit Finding:</b> Exactly 16 scheduled matches had 0 balls bowled due to persistent inclement weather and wet outfields. These matches appear in the competition fixture schedule (<code class="text-pink-400">matches.csv</code>) with status <em>Match Abandoned</em>, but produce zero rows in <code class="text-pink-400">ball_by_ball.csv</code>.</p>
        <p><b class="text-white">Verification Equation:</b> <span class="font-mono text-emerald-400 font-bold">883 Scheduled = 867 Contested + 16 Abandoned</span>. All 200,999 deliveries in the dataset originate from the 867 contested matches.</p>
      </div>

      <div>
        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Audit Log: 16 Abandoned Matches</div>
        <div class="max-h-36 overflow-y-auto rounded bg-slate-950/60 border border-slate-800 text-[11px] p-2 space-y-1 font-mono text-slate-400">
          <div>Match 31281 (2024-05-13) â€¢ Abandoned without toss/play</div>
          <div>Match 31284 (2024-05-16) â€¢ Abandoned without toss/play</div>
          <div>Match 31288 (2024-05-19) â€¢ Abandoned without toss/play</div>
          <div>Match 32610 (2024-05-22) â€¢ Abandoned without toss/play</div>
          <div>Match 32612 (2024-05-28) â€¢ Abandoned without toss/play</div>
          <div>Match 32622 (2024-05-20) â€¢ Abandoned without toss/play</div>
          <div>Match 38797 (2024-12-14) â€¢ Abandoned without toss/play</div>
          <div>Match 36564 (2024-09-15) â€¢ Abandoned without toss/play</div>
          <div>Match 36210 (2025-09-14) â€¢ Abandoned without toss/play</div>
          <div>Match 40761 (2025-05-17) â€¢ Abandoned without toss/play</div>
          <div>Match 41502 (2025-06-12) â€¢ Abandoned without toss/play</div>
          <div>Match 41503 (2025-06-14) â€¢ Abandoned without toss/play</div>
          <div>Match 42030 (2025-12-17) â€¢ Abandoned without toss/play</div>
          <div>Match 46008 (2025-09-19) â€¢ Abandoned without toss/play</div>
          <div>Match 48513 (2026-01-10) â€¢ Abandoned without toss/play</div>
          <div>Match 50189 (2026-04-29) â€¢ Abandoned without toss/play</div>
        </div>
      </div>

      <div class="pt-2 flex justify-end">
        <button onclick="closeReconciliationModal()" class="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white transition">
          Acknowledge Reconciliation
        </button>
      </div>

    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- INLINE DATA & APPLICATION JAVASCRIPT                                      -->
  <!-- ========================================================================= -->
  <script>
    // Embedded Datasets
    const BATTERS_DATA = {json.dumps(batters_data)};
    const BOWLERS_DATA = {json.dumps(bowlers_data)};
    const RR_SQUAD_DATA = {json.dumps(rr_squad_data)};
    const AUCTION_TARGETS_DATA = {json.dumps(auction_targets_data)};
    const METADATA = {json.dumps(metadata_data)};

    // State Variables
    let currentModel = 'calibrated'; // 'calibrated' or 'legacy'
    let currentBattingSort = {{ column: 'rank', asc: true }};
    let currentBowlingSort = {{ column: 'rank', asc: true }};

    // Navigation Switcher
    function switchModule(moduleId) {{
      document.querySelectorAll('.module-pane').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));

      const targetPane = document.getElementById(moduleId);
      if (targetPane) targetPane.classList.remove('hidden');

      const targetNav = document.getElementById('nav-' + moduleId);
      if (targetNav) targetNav.classList.add('active');

      // Update breadcrumb
      const titles = {{
        'module-overview': '01 Executive Overview',
        'module-batting': '02 Batting Intelligence',
        'module-bowling': '03 Bowling Intelligence',
        'module-lab': '04 Pressure Analytics Lab',
        'module-squad': '05 RR Squad War Room',
        'module-auction': '06 Auction Simulator'
      }};
      document.getElementById('breadcrumb-current').textContent = titles[moduleId] || '';
    }}

    // Model Switcher (Calibrated vs Legacy)
    function setModel(modelName) {{
      currentModel = modelName;
      const btnCal = document.getElementById('btn-model-calibrated');
      const btnLeg = document.getElementById('btn-model-legacy');

      if (modelName === 'calibrated') {{
        btnCal.className = "px-2.5 py-1 rounded-md text-[11px] font-bold transition bg-gradient-to-r from-pink-600 to-pink-700 text-white shadow";
        btnLeg.className = "px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition";
      }} else {{
        btnLeg.className = "px-2.5 py-1 rounded-md text-[11px] font-bold transition bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow";
        btnCal.className = "px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition";
      }}

      // Re-render tables & comparisons
      renderBattersTable();
      renderBowlersTable();
      updateComparison();
    }}

    // Batting Table Rendering
    function renderBattersTable() {{
      const tbody = document.getElementById('batting-table-body');
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

      // Sort
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
      filtered.forEach((b, idx) => {{
        const prsScore = (currentModel === 'calibrated' ? b.prs_calibrated : b.prs_legacy).toFixed(2);
        const deltaColor = b.delta_sr >= 0 ? 'text-emerald-400' : 'text-red-400';
        const deltaSign = b.delta_sr >= 0 ? '+' : '';
        const isTop = b.rank <= 10;
        const rankBadge = isTop ? 'bg-pink-500/20 text-pink-400 border border-pink-500/30' : 'text-slate-400';

        html += `
          <tr class="hover:bg-slate-800/40 transition">
            <td class="py-2.5 px-3 font-mono font-bold text-center">
              <span class="px-1.5 py-0.5 rounded text-[11px] ${{rankBadge}}">#${{b.rank}}</span>
            </td>
            <td class="py-2.5 px-4 font-bold text-white flex items-center gap-2">
              <span>${{b.name}}</span>
              ${{b.id === 50284 ? '<span class="badge-pink text-[9px] px-1 rounded font-bold">RR</span>' : ''}}
              ${{b.id === 24707 ? '<span class="badge-gold text-[9px] px-1 rounded font-bold">TARGET</span>' : ''}}
            </td>
            <td class="py-2.5 px-3 text-center">
              <div class="flex items-center justify-center gap-1.5">
                <span class="font-mono font-bold text-pink-400 text-xs">${{prsScore}}</span>
              </div>
            </td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_balls}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_runs}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-white">${{b.hp_sr.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_avg.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.dot_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.bound_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold ${{deltaColor}}">${{deltaSign}}${{b.delta_sr.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-center">
              <button onclick="inspectPlayer(${{b.id}}, 'batter')" class="px-2 py-1 rounded bg-slate-800 hover:bg-pink-600 hover:text-white text-[11px] font-semibold text-slate-300 transition">
                Inspect
              </button>
            </td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    function filterBatters() {{
      renderBattersTable();
    }}

    function updateBattingMinBalls(val) {{
      document.getElementById('batting-min-balls-val').textContent = val;
      renderBattersTable();
    }}

    function sortBatters(col) {{
      if (currentBattingSort.column === col) {{
        currentBattingSort.asc = !currentBattingSort.asc;
      }} else {{
        currentBattingSort.column = col;
        currentBattingSort.asc = false; // Descending default for metrics
      }}
      renderBattersTable();
    }}

    // Bowling Table Rendering
    function renderBowlersTable() {{
      const tbody = document.getElementById('bowling-table-body');
      const searchVal = document.getElementById('bowling-search').value.toLowerCase();
      const minBalls = parseInt(document.getElementById('bowling-min-balls').value, 10);
      const eligFilter = document.getElementById('bowling-eligibility').value;

      let filtered = BOWLERS_DATA.filter(b => {{
        if (b.hp_balls < minBalls) return false;
        if (searchVal && !b.name.toLowerCase().includes(searchVal)) return false;
        if (eligFilter === 'eligible' && !b.is_auction_eligible) return false;
        return true;
      }});

      // Sort
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
      filtered.forEach((b) => {{
        const prsScore = (currentModel === 'calibrated' ? b.prs_calibrated : b.prs_legacy).toFixed(2);
        const rankDisplay = eligFilter === 'eligible' ? (b.rank_eligible ? '#' + b.rank_eligible : 'N/A') : '#' + b.rank_all;
        const deltaColor = b.delta_econ <= 0 ? 'text-emerald-400' : 'text-red-400';
        const deltaSign = b.delta_econ > 0 ? '+' : '';

        html += `
          <tr class="hover:bg-slate-800/40 transition">
            <td class="py-2.5 px-3 font-mono font-bold text-center">
              <span class="px-1.5 py-0.5 rounded text-[11px] bg-blue-500/20 text-blue-300">${{rankDisplay}}</span>
            </td>
            <td class="py-2.5 px-4 font-bold text-white flex items-center gap-2">
              <span>${{b.name}}</span>
              ${{!b.is_auction_eligible ? '<span class="badge-red text-[9px] px-1 rounded font-bold">EXCLUDED</span>' : ''}}
              ${{b.id === 24070 ? '<span class="badge-pink text-[9px] px-1 rounded font-bold">#1 CLOSER</span>' : ''}}
              ${{b.id === 1469 ? '<span class="badge-blue text-[9px] px-1 rounded font-bold">#1 SPIN</span>' : ''}}
            </td>
            <td class="py-2.5 px-3 text-center">
              <span class="font-mono font-bold text-blue-400 text-xs">${{prsScore}}</span>
            </td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_balls}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-emerald-400">${{b.hp_wkts}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-white">${{b.hp_econ.toFixed(2)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.hp_sr.toFixed(1)}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.dot_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-400">${{b.bound_pct.toFixed(1)}}%</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold ${{deltaColor}}">${{deltaSign}}${{b.delta_econ.toFixed(2)}}</td>
            <td class="py-2.5 px-3 text-center">
              <button onclick="inspectPlayer(${{b.id}}, 'bowler')" class="px-2 py-1 rounded bg-slate-800 hover:bg-blue-600 hover:text-white text-[11px] font-semibold text-slate-300 transition">
                Inspect
              </button>
            </td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    function filterBowlers() {{
      renderBowlersTable();
    }}

    function updateBowlingMinBalls(val) {{
      document.getElementById('bowling-min-balls-val').textContent = val;
      renderBowlersTable();
    }}

    function sortBowlers(col) {{
      if (currentBowlingSort.column === col) {{
        currentBowlingSort.asc = !currentBowlingSort.asc;
      }} else {{
        currentBowlingSort.column = col;
        currentBowlingSort.asc = col === 'hp_econ' || col === 'hp_sr'; // Ascending for economy & strike rate
      }}
      renderBowlersTable();
    }}

    // RR Squad Audit Table Rendering
    function renderSquadTable() {{
      const tbody = document.getElementById('squad-table-body');
      let html = '';

      RR_SQUAD_DATA.forEach(p => {{
        const bRank = p.batter_rank ? '#' + p.batter_rank : '-';
        const bPrs = p.batter_prs ? p.batter_prs.toFixed(1) : '-';
        const bwRank = p.bowler_rank ? '#' + p.bowler_rank : '-';
        const bwPrs = p.bowler_prs ? p.bowler_prs.toFixed(1) : '-';
        const bwEcon = p.bowler_hp_econ ? p.bowler_hp_econ.toFixed(2) : '-';

        let verdict = '<span class="text-slate-400">Squad Depth</span>';
        if (p.player_name === 'Vaibhav Sooryavanshi') verdict = '<span class="badge-pink px-2 py-0.5 rounded font-bold">#1 Key Retention &amp; Build Around</span>';
        else if (p.player_name === 'Yashasvi Jaiswal') verdict = '<span class="badge-green px-2 py-0.5 rounded font-bold">Core Opener (PRS 55.44)</span>';
        else if (p.player_name === 'Sam Curran') verdict = '<span class="badge-red px-2 py-0.5 rounded font-bold">High Death Leak (10.21 Econ)</span>';
        else if (p.player_name === 'Tushar Deshpande') verdict = '<span class="badge-red px-2 py-0.5 rounded font-bold">Death Leak (9.84 Econ)</span>';
        else if (p.player_name === 'Jofra Archer') verdict = '<span class="badge-blue px-2 py-0.5 rounded font-bold">Pace Spearhead (PRS 48.75)</span>';
        else if (p.player_name === 'Dhruv Jurel') verdict = '<span class="badge-gold px-2 py-0.5 rounded font-bold">Crisis Closer (PRS 42.61)</span>';

        html += `
          <tr class="hover:bg-slate-800/40 transition">
            <td class="py-2 px-4 font-bold text-white">${{p.player_name}}</td>
            <td class="py-2 px-3 font-mono text-slate-300">${{bRank}}</td>
            <td class="py-2 px-3 font-mono text-pink-400 font-bold">${{bPrs}}</td>
            <td class="py-2 px-3 font-mono text-slate-300">${{bwRank}}</td>
            <td class="py-2 px-3 font-mono text-blue-400 font-bold">${{bwPrs}}</td>
            <td class="py-2 px-3 font-mono text-slate-300">${{bwEcon}}</td>
            <td class="py-2 px-4 text-xs">${{verdict}}</td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    // Auction Simulator Logic
    function updateAuctionSimulator() {{
      const pCost = parseFloat(document.getElementById('slider-pathirana').value);
      const sCost = parseFloat(document.getElementById('slider-santner').value);
      const aCost = parseFloat(document.getElementById('slider-ashutosh').value);

      document.getElementById('val-sim-pathirana').textContent = 'â‚¹' + pCost.toFixed(2) + ' Cr';
      document.getElementById('val-sim-santner').textContent = 'â‚¹' + sCost.toFixed(2) + ' Cr';
      document.getElementById('val-sim-ashutosh').textContent = 'â‚¹' + aCost.toFixed(2) + ' Cr';

      const totalSpent = pCost + sCost + aCost;
      const remaining = 35.0 - totalSpent;

      const remEl = document.getElementById('sim-remaining-purse');
      remEl.textContent = 'â‚¹' + remaining.toFixed(2) + ' Cr';
      if (remaining < 3.0) {{
        remEl.className = 'text-base font-black text-red-400';
      }} else if (remaining < 6.0) {{
        remEl.className = 'text-base font-black text-amber-400';
      }} else {{
        remEl.className = 'text-base font-black text-emerald-400';
      }}
    }}

    function setSimPreset(p, s, a) {{
      document.getElementById('slider-pathirana').value = p;
      document.getElementById('slider-santner').value = s;
      document.getElementById('slider-ashutosh').value = a;
      updateAuctionSimulator();
    }}

    // 3-Player Dynamic Comparison Logic
    function initComparisonDropdowns() {{
      const sel1 = document.getElementById('compare-p1');
      const sel2 = document.getElementById('compare-p2');
      const sel3 = document.getElementById('compare-p3');

      let optionsHtml = '';
      optionsHtml += '<optgroup label="Auction Targets & Bowlers">';
      BOWLERS_DATA.forEach(b => {{
        optionsHtml += `<option value="bowl_${{b.id}}">${{b.name}} (Bowler - PRS ${{b.prs_calibrated.toFixed(1)}})</option>`;
      }});
      optionsHtml += '</optgroup>';

      optionsHtml += '<optgroup label="Batters">';
      BATTERS_DATA.forEach(b => {{
        optionsHtml += `<option value="bat_${{b.id}}">${{b.name}} (Batter - PRS ${{b.prs_calibrated.toFixed(1)}})</option>`;
      }});
      optionsHtml += '</optgroup>';

      sel1.innerHTML = optionsHtml;
      sel2.innerHTML = optionsHtml;
      sel3.innerHTML = optionsHtml;

      // Default selections: Pathirana, Santner, Sam Curran
      sel1.value = 'bowl_24070'; // Pathirana
      sel2.value = 'bowl_1469';  // Santner
      sel3.value = 'bowl_4409';  // Sam Curran

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
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <div>
                <span class="text-[10px] text-pink-400 font-bold uppercase">${{title}}</span>
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
                <span class="font-mono font-bold text-emerald-400">${{isBat ? d.hp_sr.toFixed(1) : d.hp_econ.toFixed(2)}}</span>
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
                <span class="text-slate-400">Boundary %:</span>
                <span class="font-mono text-slate-300">${{d.bound_pct.toFixed(1)}}%</span>
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

    // Player Modal (Jos Buttler Style)
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

      // Monogram avatar
      const initials = player.name.split(' ').map(n => n[0]).join('').slice(0, 2);
      document.getElementById('modal-player-initials').textContent = initials;

      const prs = currentModel === 'calibrated' ? player.prs_calibrated : player.prs_legacy;

      let metricsHtml = '';
      if (playerType === 'batter') {{
        metricsHtml = `
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">PRS Score</span>
            <div class="text-base font-black text-pink-400 font-mono">${{prs.toFixed(2)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Strike Rate</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_sr.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Average</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_avg.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Clutch &Delta;SR</span>
            <div class="text-base font-black text-emerald-400 font-mono">+${{player.delta_sr.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Dot Ball %</span>
            <div class="text-base font-black text-slate-300 font-mono">${{player.dot_pct.toFixed(1)}}%</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Bound %</span>
            <div class="text-base font-black text-slate-300 font-mono">${{player.bound_pct.toFixed(1)}}%</div>
          </div>
        `;
      }} else {{
        metricsHtml = `
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">PRS Score</span>
            <div class="text-base font-black text-blue-400 font-mono">${{prs.toFixed(2)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Economy</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_econ.toFixed(2)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">HP Wickets</span>
            <div class="text-base font-black text-emerald-400 font-mono">${{player.hp_wkts}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Bowling SR</span>
            <div class="text-base font-black text-white font-mono">${{player.hp_sr.toFixed(1)}}</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Dot Ball %</span>
            <div class="text-base font-black text-slate-300 font-mono">${{player.dot_pct.toFixed(1)}}%</div>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-center">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Chase WPA / 100</span>
            <div class="text-base font-black text-amber-400 font-mono">${{player.chase_wpa.toFixed(2)}}</div>
          </div>
        `;
      }}
      document.getElementById('modal-player-metrics-grid').innerHTML = metricsHtml;

      // Verdict
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

    // Reconciliation Modal
    function openReconciliationModal() {{
      document.getElementById('reconciliation-modal').classList.remove('hidden');
    }}

    function closeReconciliationModal() {{
      document.getElementById('reconciliation-modal').classList.add('hidden');
    }}

    // Initializer
    window.addEventListener('DOMContentLoaded', () => {{
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

    output_path = os.path.join(DASHBOARD_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"SUCCESS: Dashboard successfully written to {output_path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
