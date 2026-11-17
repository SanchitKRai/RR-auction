import os

WORKSPACE_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\rr_pressure_analysis"
SOURCE_PY = os.path.join(WORKSPACE_DIR, "src", "build_perfect_war_room.py")
TARGET_PY = os.path.join(WORKSPACE_DIR, "src", "build_v3_master.py")

with open(SOURCE_PY, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Asset Loading
p_photos_start = text.find('# Photos')
p_photos_end = text.find('# Figures for secondary modules')
assert p_photos_start != -1 and p_photos_end != -1, "Photos landmarks not found"

new_asset_block = """# V3 Assets & Cutouts
    V3_DIR = os.path.join(ASSETS_DIR, "v3")
    CUTOUTS_DIR = os.path.join(ASSETS_DIR, "cutouts")

    # Photos & Crest
    b64_crest = load_base64(os.path.join(CUTOUTS_DIR, "rr_crest.png"))
    b64_vaibhav = load_base64(os.path.join(CUTOUTS_DIR, "vaibhav_cutout.png"))
    b64_ashutosh = load_base64(os.path.join(CUTOUTS_DIR, "ashutosh_sharma.png"))
    b64_pathirana = load_base64(os.path.join(CUTOUTS_DIR, "matheesha_pathirana.png"))
    b64_santner = load_base64(os.path.join(CUTOUTS_DIR, "mitchell_santner.png"))
    b64_banner = load_base64(os.path.join(ASSETS_DIR, "rr_banner.jpg"))
    b64_stadium = load_base64(os.path.join(ASSETS_DIR, "sawai_mansingh_stadium.jpg"))
    b64_hawa = load_base64(os.path.join(ASSETS_DIR, "rr_banner.jpg"))
    b64_hawa_night = load_base64(os.path.join(V3_DIR, "500px-Hawa_Mahal_in_Jaipur,_Rajasthan.jpg"))
    b64_flag_crop = load_base64(os.path.join(ASSETS_DIR, "royal_flag_reference_crop.png"))

    # Player Scenic Plates (V3 AI-generated Jaipur Palace Atmospheres)
    b64_scene_batter = load_base64(os.path.join(V3_DIR, "player_card_backplates", "card_batter_scene_ai.png"))
    b64_scene_finisher = load_base64(os.path.join(V3_DIR, "player_card_backplates", "card_finisher_scene_ai.png"))
    b64_scene_death = load_base64(os.path.join(V3_DIR, "player_card_backplates", "card_death_scene_ai.png"))
    b64_scene_spin = load_base64(os.path.join(V3_DIR, "player_card_backplates", "card_spin_scene_ai.png"))

    # Role Backplates & Overlays
    bg_backplate_batter = svg_to_data_uri(load_svg(os.path.join(V3_DIR, "player_card_backplates", "card_batter_backplate.svg")))
    bg_backplate_finisher = svg_to_data_uri(load_svg(os.path.join(V3_DIR, "player_card_backplates", "card_finisher_backplate.svg")))
    bg_backplate_death = svg_to_data_uri(load_svg(os.path.join(V3_DIR, "player_card_backplates", "card_death_backplate.svg")))
    bg_backplate_spin = svg_to_data_uri(load_svg(os.path.join(V3_DIR, "player_card_backplates", "card_spin_backplate.svg")))
    bg_card_vignette = svg_to_data_uri(load_svg(os.path.join(V3_DIR, "player_card_backplates", "player_card_lower_vignette.svg")))

    # KPI Icons (V3 Rich Gradient Line Family)
    svg_kpi_target = load_svg(os.path.join(V3_DIR, "kpi_icons", "kpi_target.svg"))
    svg_kpi_ball = load_svg(os.path.join(V3_DIR, "kpi_icons", "kpi_cricket_ball.svg"))
    svg_kpi_lightning = load_svg(os.path.join(V3_DIR, "kpi_icons", "kpi_lightning.svg"))
    svg_kpi_network = load_svg(os.path.join(V3_DIR, "kpi_icons", "kpi_network.svg"))
    svg_kpi_trophy = load_svg(os.path.join(V3_DIR, "kpi_icons", "kpi_trophy.svg"))

    # Chart Ambient Glows
    svg_radar_glow = load_svg(os.path.join(V3_DIR, "chart_glow", "radar_plot_glow.svg"))
    svg_trend_glow = load_svg(os.path.join(V3_DIR, "chart_glow", "chart_panel_ambient_glow.svg"))
    svg_donut_halo = load_svg(os.path.join(V3_DIR, "chart_glow", "donut_outer_halo.svg"))

    """

text = text[:p_photos_start] + new_asset_block + text[p_photos_end:]

# 2. Update CSS Slice
p_css_start = text.find('/* Hero Banner')
p_css_end = text.find('/* Badges */')
assert p_css_start != -1 and p_css_end != -1, "CSS landmarks not found"

new_css = """/* Hero Banner (Guide V3.0 Final Authentic Hawa Mahal Specification) */
    .hero-banner {{
      position: relative;
      min-height: 140px;
      height: 148px;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: #111832;
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
    }}
    .hero-banner__photo {{
      position: absolute;
      inset: 0 0 0 auto;
      width: 52%;
      height: 100%;
      object-fit: cover;
      object-position: 50% 38%;
      pointer-events: none;
      z-index: 1;
    }}
    .hero-banner::after {{
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg,
        #111832 0%,
        rgba(17,24,50,0.98) 32%,
        rgba(17,24,50,0.72) 48%,
        rgba(17,24,50,0.12) 75%,
        rgba(17,24,50,0.25) 100%);
      pointer-events: none;
      z-index: 2;
    }}
    .hero-banner__flag {{
      position: absolute;
      z-index: 3;
      right: 14px;
      top: 4px;
      width: 17%;
      max-width: 220px;
      height: 92%;
      display: flex;
      align-items: center;
      justify-content: center;
      pointer-events: none;
      filter: drop-shadow(0 10px 18px rgba(0,0,0,0.5));
    }}
    .hero-banner__content {{
      position: relative;
      z-index: 4;
      max-width: 56%;
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

    /* Player Card Hero Portrait Frame (V3.0 Final Spec) */
    .player-card {{
      position: relative;
      isolation: isolate;
      overflow: hidden;
      border-radius: 16px;
      background: #111A32;
      border: 1px solid rgba(240, 45, 155, 0.35);
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      min-height: 400px;
      transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }}
    .player-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 30px -10px rgba(240, 45, 155, 0.25);
    }}
    .player-card.border-magenta {{ border-color: rgba(240, 45, 155, 0.4); }}
    .player-card.border-magenta:hover {{ border-color: var(--magenta); box-shadow: 0 12px 30px -10px rgba(240, 45, 155, 0.35); }}
    .player-card.border-gold {{ border-color: rgba(244, 201, 93, 0.4); }}
    .player-card.border-gold:hover {{ border-color: var(--gold); box-shadow: 0 12px 30px -10px rgba(244, 201, 93, 0.35); }}
    .player-card.border-blue {{ border-color: rgba(92, 157, 255, 0.4); }}
    .player-card.border-blue:hover {{ border-color: var(--blue); box-shadow: 0 12px 30px -10px rgba(92, 157, 255, 0.35); }}

    .player-card__scene, .player-card__tint, .player-card__fade {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      pointer-events: none;
    }}
    .player-card__scene {{
      z-index: 0;
      object-position: center 38%;
    }}
    .player-card__tint {{
      z-index: 1;
      opacity: 0.55;
      mix-blend-mode: color;
    }}
    .player-card__portrait {{
      position: absolute;
      z-index: 2;
      left: 19%;
      bottom: 22%;
      height: 72%;
      width: 62%;
      object-fit: contain;
      object-position: center bottom;
      filter: drop-shadow(0 8px 18px rgba(0,0,0,0.48)) drop-shadow(0 0 10px rgba(240,45,155,0.16));
      transition: transform 0.3s ease;
    }}
    .player-card:hover .player-card__portrait {{
      transform: scale(1.04);
    }}
    .player-card__fade {{
      z-index: 3;
    }}
    .player-card > :not(img) {{
      position: relative;
      z-index: 4;
    }}

    """

text = text[:p_css_start] + new_css + text[p_css_end:]

# 3. Update Sidebar Width, Brand Header, and Footer
text = text.replace('<aside class="w-64 flex-shrink-0', '<aside class="w-72 flex-shrink-0')

p_sbh_start = text.find('<!-- RR War Room Brand Header -->')
p_sbh_end = text.find('<!-- Navigation Section -->')
assert p_sbh_start != -1 and p_sbh_end != -1, "Sidebar header landmarks not found"

new_sbh = """<!-- RR War Room Brand Header (Guide V3.0 Large Crest) -->
      <div class="px-6 py-6 border-b border-[#273452] flex items-center space-x-4">
        <img src="{b64_crest}" alt="RR Crest" class="w-12 h-12 flex-shrink-0 object-contain drop-shadow-[0_0_12px_rgba(240,45,155,0.4)]">
        <div>
          <h1 class="text-base font-black tracking-wider text-white uppercase leading-tight">RR WAR ROOM</h1>
          <p class="text-[11px] text-slate-400 font-semibold tracking-tight mt-0.5">IPL 2027 Analytics Engine</p>
        </div>
      </div>

      """
text = text[:p_sbh_start] + new_sbh + text[p_sbh_end:]

p_sbf_start = text.find('<!-- Sidebar Bottom: Palace Silhouette & Disclaimer -->')
p_sbf_end = text.find('</aside>')
assert p_sbf_start != -1 and p_sbf_end != -1, "Sidebar footer landmarks not found"

new_sbf = """<!-- Sidebar Bottom: Real Hawa Mahal Night Photograph & Disclaimer (Guide V3.0) -->
    <div class="p-4 border-t border-[#273452] relative overflow-hidden bg-[#090E22] min-h-[140px] flex flex-col justify-end">
      <!-- Real Hawa Mahal Night Photo -->
      <img src="{b64_hawa_night}" alt="Hawa Mahal at Night" class="absolute inset-0 w-full h-full object-cover object-center opacity-45 pointer-events-none">
      <!-- Vignette Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-[#090E22] via-[#090E22]/80 to-transparent pointer-events-none z-[1]"></div>
      <!-- Text content -->
      <div class="text-[10px] text-slate-300 leading-snug relative z-10 pt-8">
        <div class="font-extrabold text-white text-[11px]">Independent Research Dossier</div>
        <div>SupeRR Selector Season 2</div>
        <div class="text-slate-400 text-[9px] mt-0.5">Not an official RR publication</div>
        <div class="text-slate-500 text-[8px] mt-1">Photo: LakshayDhiman14 / CC BY-SA 4.0</div>
      </div>
    </div>
  """
text = text[:p_sbf_start] + new_sbf + text[p_sbf_end:]

# 4. Update Hero Section
p_hero_start = text.find('<!-- HERO SECTION:')
p_hero_end = text.find('<!-- FIVE TOP KPI CARDS')
assert p_hero_start != -1 and p_hero_end != -1, "Hero landmarks not found"

new_hero = """<!-- HERO SECTION: Authentic Hawa Mahal Photograph, Atmospheric Lighting & Royal Flag (Guide V3.0 Spec) -->
        <div class="hero-banner flex items-center justify-between">
          
          <!-- Layer 1: Authentic Hawa Mahal Photographic Hero Facade -->
          <img src="{b64_hawa}" alt="Hawa Mahal" class="hero-banner__photo">

          <!-- Layer 2: Floating Royal Flag at Far Right -->
          <div class="hero-banner__flag">
            <img src="{b64_flag_crop}" alt="Rajasthan Royals Flag" class="h-full w-auto object-contain">
          </div>

          <!-- Layer 3: Live Title, Subtitle and Eyebrow in Safe Left Zone -->
          <div class="hero-banner__content px-7 py-5 space-y-1.5">
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

        """
text = text[:p_hero_start] + new_hero + text[p_hero_end:]

# 5. Update KPI Icons
text = text.replace("{get_icon('icon_target', 'w-5 h-5 text-[#5C9DFF]')}", "{svg_kpi_target}")
text = text.replace("{get_icon('icon_cricket_ball', 'w-5 h-5 text-[#5C9DFF]')}", "{svg_kpi_ball}")
text = text.replace("{get_icon('icon_lightning', 'w-5 h-5 text-[#F4C95D]')}", "{svg_kpi_lightning}")
text = text.replace("{get_icon('icon_model', 'w-5 h-5 text-[#A45BEE]')}", "{svg_kpi_network}")
text = text.replace("{get_icon('icon_trophy', 'w-5 h-5 text-[#F02D9B]')}", "{svg_kpi_trophy}")

# 6. Update Analytics Charts Glow
old_radar_canvas = """            <div class="h-56 relative flex items-center justify-center pt-2">
              <canvas id="chart-squad-radar"></canvas>
            </div>"""

new_radar_canvas = """            <div class="h-56 relative flex items-center justify-center pt-2">
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-40">
                {svg_radar_glow}
              </div>
              <canvas id="chart-squad-radar" class="relative z-10"></canvas>
            </div>"""

text = text.replace(old_radar_canvas, new_radar_canvas)

old_trend_canvas = """            <div class="h-56 relative pt-2">
              <canvas id="chart-performance-trend"></canvas>
            </div>"""

new_trend_canvas = """            <div class="h-56 relative pt-2">
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-35">
                {svg_trend_glow}
              </div>
              <canvas id="chart-performance-trend" class="relative z-10"></canvas>
            </div>"""

text = text.replace(old_trend_canvas, new_trend_canvas)

old_donut_canvas = """            <div class="h-44 relative flex items-center justify-center">
              <canvas id="chart-model-balance"></canvas>
              <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none text-center">
                <span class="text-[9px] font-bold uppercase text-slate-400 tracking-wider">Model</span>
                <span class="text-[11px] font-black text-white">Weightage</span>
              </div>
            </div>"""

new_donut_canvas = """            <div class="h-44 relative flex items-center justify-center">
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-45">
                {svg_donut_halo}
              </div>
              <canvas id="chart-model-balance" class="relative z-10"></canvas>
              <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none text-center z-20">
                <span class="text-[9px] font-bold uppercase text-slate-400 tracking-wider">Model</span>
                <span class="text-[11px] font-black text-white">Weightage</span>
              </div>
            </div>"""

text = text.replace(old_donut_canvas, new_donut_canvas)

# 7. Update 4 Player Cards with V3 Layers and Cutouts
p_cards_start = text.find('<!-- Four Custom Profile Cards Grid')
p_cards_end = text.find('<!-- MODULE 02: BATTING INTELLIGENCE')
assert p_cards_start != -1 and p_cards_end != -1, "Cards landmarks not found"

new_cards = """<!-- Four Custom Profile Cards Grid (Large Integrated Player Photography - Guide V3.0) -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <!-- Card 1: Vaibhav Sooryavanshi -->
            <div class="player-card border-magenta group">
              <img src="{b64_scene_batter}" class="player-card__scene" alt="" aria-hidden="true">
              <img src="{bg_backplate_batter}" class="player-card__tint" alt="" aria-hidden="true">
              
              <div class="absolute top-3 left-3 z-10">
                <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#F02D9B] text-white shadow-md">
                  #1 BATTER OVERALL
                </span>
              </div>

              <img src="{b64_vaibhav}" alt="Vaibhav Sooryavanshi" class="player-card__portrait">
              <img src="{bg_card_vignette}" class="player-card__fade" alt="" aria-hidden="true">

              <div class="p-3.5 space-y-2 relative z-10 mt-auto bg-gradient-to-t from-[#090E22]/95 via-[#111A32]/85 to-transparent pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Vaibhav Sooryavanshi</h4>
                    <p class="text-[11px] text-slate-300 font-medium">Top-Order Aggressor • RR Incumbent</p>
                  </div>
                  <div class="text-right">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight block">PRS</span>
                    <span class="text-base font-black font-mono text-[#F02D9B] leading-none">77.62</span>
                  </div>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/70 rounded-lg text-[10px]">
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

                <button onclick="inspectPlayer(50284, 'batter')" class="w-full py-1.5 rounded-lg bg-[#090E22] hover:bg-[#F02D9B] hover:text-white border border-[#273452] hover:border-[#F02D9B] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

            <!-- Card 2: Ashutosh Sharma -->
            <div class="player-card border-gold group">
              <img src="{b64_scene_finisher}" class="player-card__scene" alt="" aria-hidden="true">
              <img src="{bg_backplate_finisher}" class="player-card__tint" alt="" aria-hidden="true">
              
              <div class="absolute top-3 left-3 z-10">
                <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#F4C95D] text-slate-950 shadow-md">
                  #1 CLUTCH FINISHER
                </span>
              </div>

              <img src="{b64_ashutosh}" alt="Ashutosh Sharma" class="player-card__portrait">
              <img src="{bg_card_vignette}" class="player-card__fade" alt="" aria-hidden="true">

              <div class="p-3.5 space-y-2 relative z-10 mt-auto bg-gradient-to-t from-[#090E22]/95 via-[#111A32]/85 to-transparent pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Ashutosh Sharma</h4>
                    <p class="text-[11px] text-slate-300 font-medium">Designated Finisher • Auction Target</p>
                  </div>
                  <div class="text-right">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight block">PRS</span>
                    <span class="text-base font-black font-mono text-[#F4C95D] leading-none">67.65</span>
                  </div>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/70 rounded-lg text-[10px]">
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

                <button onclick="inspectPlayer(24707, 'batter')" class="w-full py-1.5 rounded-lg bg-[#090E22] hover:bg-[#F4C95D] hover:text-slate-950 border border-[#273452] hover:border-[#F4C95D] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

            <!-- Card 3: Matheesha Pathirana -->
            <div class="player-card border-magenta group">
              <img src="{b64_scene_death}" class="player-card__scene" alt="" aria-hidden="true">
              <img src="{bg_backplate_death}" class="player-card__tint" alt="" aria-hidden="true">
              
              <div class="absolute top-3 left-3 z-10">
                <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#F02D9B] text-white shadow-md">
                  #1 DEATH CLOSER
                </span>
              </div>

              <img src="{b64_pathirana}" alt="Matheesha Pathirana" class="player-card__portrait">
              <img src="{bg_card_vignette}" class="player-card__fade" alt="" aria-hidden="true">

              <div class="p-3.5 space-y-2 relative z-10 mt-auto bg-gradient-to-t from-[#090E22]/95 via-[#111A32]/85 to-transparent pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Matheesha Pathirana</h4>
                    <p class="text-[11px] text-slate-300 font-medium">Express Slinger • Primary Auction Target</p>
                  </div>
                  <div class="text-right">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight block">PRS</span>
                    <span class="text-base font-black font-mono text-[#F02D9B] leading-none">68.75</span>
                  </div>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/70 rounded-lg text-[10px]">
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

                <button onclick="inspectPlayer(24070, 'bowler')" class="w-full py-1.5 rounded-lg bg-[#090E22] hover:bg-[#F02D9B] hover:text-white border border-[#273452] hover:border-[#F02D9B] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

            <!-- Card 4: Mitchell Santner -->
            <div class="player-card border-blue group">
              <img src="{b64_scene_spin}" class="player-card__scene" alt="" aria-hidden="true">
              <img src="{bg_backplate_spin}" class="player-card__tint" alt="" aria-hidden="true">
              
              <div class="absolute top-3 left-3 z-10">
                <span class="px-2.5 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#5C9DFF] text-slate-950 shadow-md">
                  #1 SPIN SQUEEZER
                </span>
              </div>

              <img src="{b64_santner}" alt="Mitchell Santner" class="player-card__portrait">
              <img src="{bg_card_vignette}" class="player-card__fade" alt="" aria-hidden="true">

              <div class="p-3.5 space-y-2 relative z-10 mt-auto bg-gradient-to-t from-[#090E22]/95 via-[#111A32]/85 to-transparent pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="font-extrabold text-white text-base tracking-tight leading-tight">Mitchell Santner</h4>
                    <p class="text-[11px] text-slate-300 font-medium">Left-Arm Spin • Tactical Auction Target</p>
                  </div>
                  <div class="text-right">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight block">PRS</span>
                    <span class="text-base font-black font-mono text-[#5C9DFF] leading-none">63.64</span>
                  </div>
                </div>

                <div class="grid grid-cols-4 gap-1 text-center py-2 px-1 border-t border-[#273452] bg-[#090E22]/70 rounded-lg text-[10px]">
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

                <button onclick="inspectPlayer(1469, 'bowler')" class="w-full py-1.5 rounded-lg bg-[#090E22] hover:bg-[#5C9DFF] hover:text-slate-950 border border-[#273452] hover:border-[#5C9DFF] text-xs font-bold text-slate-200 transition shadow-sm">
                  View Full Dossier &rarr;
                </button>
              </div>
            </div>

          </div>
        </div>

      </section>

      """

text = text[:p_cards_start] + new_cards + text[p_cards_end:]

with open(TARGET_PY, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: src/build_v3_master.py created cleanly with landmark slices.")
