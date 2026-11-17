# RR WAR ROOM — FINAL IMPLEMENTATION GUIDE (V3.0)
**Last visual upgrade specification — based on the original reference and the latest current-dashboard screenshot**

## 0. Scope and priority
This is the final visual-correction guide. The target is the user's original RR WAR ROOM reference, not the current intermediate dashboard. Preserve existing app behaviour, all data logic, routes, filters and dossier actions. Improve the art direction, missing decorative assets, image composition and responsive sizing only.

**Important distinction:** the reference is a 16:9 executive dashboard composition. The latest app screenshot is much taller and more vertically stretched. Build and validate at 1920×1080 (and 1600×900), then reflow for narrower/mobile layouts rather than making every component taller.

## 1. Visual gap audit — original vs latest build

| Area | Original target | Latest build gap | Required final correction |
|---|---|---|---|
| Sidebar width/header | Broad branded rail, large crest header | Rail and logo block too compressed | Restore a stronger left rail; target ~280–320px at 1920px desktop and ~100–116px branded header |
| Sidebar footer | Real Hawa Mahal night photograph, purple/pink illumination, text over lower fade | Generic geometric skyline | Replace with licensed night Hawa Mahal photo + `sidebar_photo_vignette.svg`; keep dossier disclaimer live |
| Hero architecture | Wide Hawa Mahal view, visible full architectural rhythm | Current photo too tightly zoomed/cropped | Use a wide, high-res photo with less zoom; tune object-position; preserve recognizable facade across the right 45–52% |
| Hero flag | Large flowing flag at far right, no small boxed thumbnail | Small framed image | Use a broad waving flag treatment, integrated into the hero; no separate white/bordered thumbnail card |
| Hero text | Strong, large title and readable subtitle | Generally good but may compress with hero photo | Keep left 50–55% text-safe; gold-highlight “Reliability”; keep dark gradient overlay |
| KPI cards | Rich outlined icons, subtle gradient surfaces, inner glow and stronger value hierarchy | Simplified icon badges and flatter surfaces | Replace icons with the provided gradient SVGs; add restrained radial light and soft shadow |
| Radar chart | Magenta glowing current squad polygon, translucent purple fill, blue dashed league average | Flat polygon and muted lighting | Add `radar_plot_glow.svg`, gradient fill, bright stroke, luminous points and dashed comparison line |
| Trend chart | Smooth magenta PRS line with glowing nodes; blue HP% area/line; translucent area fills | Lines too flat/ordinary; no ambient underglow | Add `chart_panel_ambient_glow.svg`; smooth curves; blurred under-stroke; gradient area fills; luminous nodes |
| Donut chart | Segments have subtle depth/glow and clear center label | Flat, plain segments | Add `donut_outer_halo.svg`; use subtle gradients, thin gaps and a crisp inner label; no 3D bevel |
| Player card backgrounds | Four distinct palace/stadium scenes with haze and role colour | Mostly flat gradient with repeated blocky skyline | Use four supplied SVG backplates; vary warmth and glow per role |
| Player image compositing | Big upper-body cut-out over background, no rectangle | Three white rectangular photo backgrounds | Background-remove approved photos to transparent PNG; blend into backplate; no white image panel |
| Player PRS | Large coloured PRS at right side of portrait area | Small PRS chip adjacent to name | Move score to right of image/name zone and use role-coloured luminous type |
| Card layout | Four broad, compact equal cards | Cards too tall/narrow compared with reference | Target card width:height around 1.05–1.15 on 16:9 desktop; do not vertically stretch |
| Role badges | Compact bright pink/gold/blue tags integrated at top-left | Present but less integrated | Use supplied role badge backplates with live text; match role colours |
| Typography | Clear hierarchy, larger section headings and labels | Several labels look too small/condensed | Use Inter/Manrope/Plus Jakarta Sans; increase chart text and metadata readability |
| Overall lighting | Selective ambient magenta/blue glows | Flat areas and generic gradients | Add glow only at hero edges, KPI icons, chart plots, card rim and active nav; avoid glow everywhere |

## 2. Missing asset inventory — exact handoff

### A. Hawa Mahal hero and footer photography
Use high-resolution real photographs, not a generic palace SVG as the main photo.

**Hero candidate (landscape):**
- File page: https://commons.wikimedia.org/wiki/File:Jaipur_-_Hawa_Mahal.jpg
- Author: Brijesh Gosai
- Resolution: 6,000 × 4,000 px
- License: CC BY-SA 4.0
- Attribution: “Photo: Brijesh Gosai / Wikimedia Commons, CC BY-SA 4.0”
- The hero can be cropped/colour-graded for the reference, but document edits and retain the license link.

**Sidebar footer candidate (night portrait):**
- File page: https://commons.wikimedia.org/wiki/File:Hawa_Mahal_in_Jaipur,_Rajasthan.jpg
- Author: LakshayDhiman14
- Resolution: 3,480 × 4,640 px
- License: CC BY-SA 4.0
- Attribution: “Photo: LakshayDhiman14 / Wikimedia Commons, CC BY-SA 4.0”

CC BY-SA 4.0 requires attribution and share-alike when distributing adaptations. Keep a visible credits/readme file in the repository and re-check each Commons file page before production.

Use `hero_left_gradient_overlay.svg` on top of the hero photo. Use `sidebar_photo_vignette.svg` on top of the footer/night image. The included `reference_only` crops are too small for production. `optional_ai_jaipur_palace_atmosphere.png` is an AI-generated mood plate, not a documentary Hawa Mahal photograph; use only as an optional decorative texture, not as the factual monument image.

### B. Waving RR flag and brand logo
- Use the approved official RR flag/crest artwork if available from the brand owner or supplied project files.
- `royal_flag_wave_generic.svg` is a generic placeholder showing fabric shape and fold placement only. It is **not** the official Rajasthan Royals mark.
- Do not redraw, distort or approximate official franchise marks. Place the genuine flag asset over the hero without a separate square thumbnail border.
- The top-left crest should be larger and more legible than the current tiny shield. Use an approved transparent SVG/PNG.

### C. Four separate player-card scenic backplates
Use the four delivered files in `assets/player_card_backplates/`:
- `card_batter_backplate.svg` — magenta/oxblood atmosphere
- `card_finisher_backplate.svg` — gold/bronze atmosphere
- `card_death_backplate.svg` — purple/magenta atmosphere
- `card_spin_backplate.svg` — royal-blue atmosphere

These are architectural/haze layers, not player pictures. They deliberately contain no text or people, so the player photo and all stats remain live UI content.

### D. Player photos — required preparation
The correct result uses large upper-body player cut-outs blended over the backplate.
- Use the existing approved player photo/source already used by the project, or licensed team/league photography.
- Export each player as transparent PNG/WebP with alpha; recommended 900–1400px tall where possible.
- Remove the white background cleanly, including between arms and around hair; do not leave a white rectangle or white halo.
- Keep shoulders and chest/jersey visible; crop around mid-torso, not at the neck.
- Add a restrained CSS drop shadow and a subtle bottom fade. Do not use circles as the main portrait frame.
- Do not use AI-generated lookalikes of named real players. If an approved photo is unavailable, use a neutral silhouette or initials rather than fabricating the player's likeness.

### E. Chart and KPI visual assets
- KPI icons: `assets/kpi_icons/kpi_target.svg`, `kpi_cricket_ball.svg`, `kpi_lightning.svg`, `kpi_network.svg`, `kpi_trophy.svg`.
- Chart ambient: `assets/chart_glow/chart_panel_ambient_glow.svg`.
- Radar plot: `assets/chart_glow/radar_plot_glow.svg`.
- Donut halo: `assets/chart_glow/donut_outer_halo.svg`.
- Data point sprite: `assets/chart_glow/chart_data_point_glow.svg`.

Do not bake plotted values or chart series into image assets. Charts must remain dynamic and data-driven. These assets only create background light, icon art and point decoration.

### F. Role badges and card overlays
- `assets/role_badges/role_badge_batter.svg`
- `assets/role_badges/role_badge_finisher.svg`
- `assets/role_badges/role_badge_death.svg`
- `assets/role_badges/role_badge_spin.svg`
- `assets/player_card_backplates/player_card_lower_vignette.svg`
- `assets/player_card_backplates/player_card_gradient_border.svg`

Role text and player information must remain live text, not embedded in SVGs.

## 3. Exact composition rules

### Hero banner
- Height: 128–150px at 1920×1080 desktop.
- Photo occupies right 45–52%; use `object-fit: cover`, tune `object-position` to show the facade rather than zooming into a few windows.
- Title text zone occupies left 50–56%; keep heading and subtitle above photo detail via the left gradient overlay.
- Hawa Mahal should be recognizable at first glance. Avoid the current over-tight close crop.
- Flag uses the far-right 12–18% of the banner, larger and waving, without a boxed-thumbnail frame.
- Do not place the flag over the central facade.

### Sidebar
- Desktop width: 280–320px at 1920px, adapt proportionally but preserve enough width for the long labels.
- Brand header height: 100–116px.
- Make logo/crest large enough to read; brand name and IPL analytics subtitle should have a clear two-line hierarchy.
- Footer image: use the licensed vertical Hawa Mahal night photo, darkened with vignette; place title/disclaimer as live text over the lower section.
- Maintain clear separation between Analytics Suite and Tools & Reports.

### KPI row
- Five equal-height tiles.
- Value should be the dominant typographic element; label is secondary; trend/change third.
- Use the supplied outline icons at 36–48px. Put icons inside tinted circular/soft-square wells.
- Use subtle top-left radial highlight, not a neon border around every tile.

### Analytics row
- Three panels in ratio approximately `1 : 1.9 : 1`.
- Use the same panel background/border/radius across all three.
- Radar: pink outer line and data points; translucent magenta-purple fill; blue dashed league average; subtle ambient radial glow behind plot.
- Trend: smooth magenta PRS line; blue HP% line/area; translucent gradients under both series; point glow around nodes; thin dark gridlines; axes remain readable.
- Donut: preserve data categories/weights; create a luminous outer halo and controlled gradients; label text aligned on the right.
- Keep chart labels around 11–12px or larger at 1920×1080. Do not reduce text just to squeeze into panels.

### Player cards — most important section
- Four equal-width cards on desktop.
- Aim for card width:height ratio between 1.05 and 1.15, similar to the original compact reference.
- Layer order (back to front):
  1. photo-like scenic plate (`card_*_scene_ai.png`) as the background atmosphere
  2. role-coloured SVG backplate/gradient overlay (`card_*_backplate.svg`)
  3. transparent player cut-out PNG/WebP (large upper-body, centred slightly left)
  4. photo drop-shadow / soft rim light (CSS)
  5. top-left role badge backplate + live text
  6. bottom vignette
  7. player name, role descriptor and PRS score
  8. metric row(s), then dossier CTA
- No white image rectangle. No separate white image frame. No small circular avatar as the main player image.
- Player portrait must occupy roughly 58–68% of the card height in the upper portion; its background must be transparent.
- PRS is placed toward the right edge of the portrait/name region and colour-coded by role.
- Keep metrics to a consistent grid: label small and muted, value bright and tabular.
- Ensure CTA stays in the same bottom alignment across all four cards.

### Sidebar footer and ambient scenery
- Do not use the generic geometric skyline as the only footer image.
- Use the licensed night Hawa Mahal photo plus `sidebar_photo_vignette.svg`.
- Generic skyline/palace SVGs can remain as very subtle supporting texture, but must not replace the actual monument photo.

## 4. Chart glow implementation guidance

For SVG chart libraries, render a blurred duplicate path underneath the sharp data path:
```css
.chart-series-glow {
  fill: none;
  stroke: var(--series-color);
  stroke-width: 8px;
  opacity: .28;
  filter: blur(7px);
}
.chart-series-main {
  fill: none;
  stroke: var(--series-color);
  stroke-width: 2.8px;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.chart-area {
  opacity: .24;
}
.chart-point {
  fill: #fff;
  stroke: var(--series-color);
  stroke-width: 2px;
  filter: drop-shadow(0 0 5px var(--series-color));
}
```
For Canvas/Power BI visuals, use supported gradient fills, transparent area shading, shadows and data-point formatting; test in the published service. If the visual cannot produce the glow, use a transparent `chart_panel_ambient_glow.svg` behind it and retain native dynamic chart elements above.

The original reference does **not** show a separate IPL logo watermark behind the charts. Do not add one as a supposed missing reference asset. The missing effect is the magenta/blue luminous chart styling.



## 4A. React/CSS reference for player photo compositing
Use this pattern with the V3 files. Adjust paths to the app's public asset folder.

```jsx
<article className="player-card player-card--batter">
  <img className="player-card__scene" src="/assets/card_batter_scene_ai.png" alt="" aria-hidden="true" />
  <img className="player-card__tint" src="/assets/card_batter_backplate.svg" alt="" aria-hidden="true" />
  <img className="player-card__portrait" src="/players/vaibhav-sooryavanshi-cutout.png" alt="Vaibhav Sooryavanshi" />
  <img className="player-card__fade" src="/assets/player_card_lower_vignette.svg" alt="" aria-hidden="true" />
  {/* Keep badge, player name, PRS, statistics and CTA as live components. */}
</article>
```

```css
.player-card { position:relative; isolation:isolate; overflow:hidden; aspect-ratio:1.1 / 1; border-radius:16px; background:#111a32; border:1px solid rgba(240,45,155,.35); }
.player-card__scene,.player-card__tint,.player-card__fade { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; pointer-events:none; }
.player-card__scene { z-index:0; object-position:center 38%; }
.player-card__tint { z-index:1; opacity:.55; mix-blend-mode:color; }
.player-card__portrait { position:absolute; z-index:2; left:19%; bottom:22%; height:72%; width:62%; object-fit:contain; object-position:center bottom; filter:drop-shadow(0 8px 18px rgba(0,0,0,.48)) drop-shadow(0 0 10px rgba(240,45,155,.16)); }
.player-card__fade { z-index:3; }
.player-card > :not(img) { position:relative; z-index:4; }
```

The source portrait must have real transparency. CSS blend modes do not reliably remove a white rectangle. If the current player photo has a white background, create a transparent cut-out with a proper background-removal tool and inspect hair, sleeves and arm edges at 100% zoom.

## 4B. Hero crop implementation
```css
.hero { position:relative; overflow:hidden; min-height:140px; border-radius:18px; }
.hero__photo { position:absolute; inset:0 0 0 auto; width:56%; height:100%; object-fit:cover; object-position:50% 42%; }
.hero__overlay { position:absolute; inset:0; width:100%; height:100%; pointer-events:none; }
.hero__flag { position:absolute; z-index:3; right:14px; top:4px; width:17%; max-width:230px; height:94%; object-fit:contain; filter:drop-shadow(0 10px 18px rgba(0,0,0,.42)); }
.hero__copy { position:relative; z-index:4; max-width:58%; }
```
Use the Wikimedia landscape photo as the actual factual Hawa Mahal image. Tune `object-position` with the full-resolution file; do not use the low-resolution screenshot crop.

## 5. Design tokens

```css
:root {
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
}
```
Fonts: Inter, Manrope or Plus Jakarta Sans. Keep headings semibold/bold; numerals tabular. Do not use a condensed font for body copy.

## 6. Responsive and layout constraints
- Desktop target: 1920×1080 and 1600×900, 16:9.
- At widths below 1280px, reduce sidebar width and allow content to scroll/reflow; do not compress text into micro-labels.
- At tablet, change 4 player columns to 2; at mobile, use 1 column and collapse sidebar.
- Avoid a 4:3 stretched composition at desktop. Do not make the cards vertically elongated to consume spare height.
- Maintain consistent spacing grid: 8px base, 16–24px internal panel padding, 12–16px card gaps.
- Keep consistent corner radius: 12–18px; card borders 1px, glow borders subtle.

## 7. Things not to do
1. Do not use white-background rectangular player photos.
2. Do not use circular headshots as the main player portrait.
3. Do not use a generic skyline where the original uses Hawa Mahal photography.
4. Do not over-zoom the hero photo; show the architectural façade, not just a few windows.
5. Do not place the flag inside a tiny bordered thumbnail card.
6. Do not use flat line charts with no area fill, glow or point lighting.
7. Do not add a fake IPL watermark behind charts; it is not present in the reference.
8. Do not turn every panel border neon; lighting must be selective.
9. Do not bake text, player names, data or chart values into image assets.
10. Do not redraw official RR/IPL logos from memory; use approved brand artwork.
11. Do not invent player likenesses. Use licensed photography and transparent cut-outs.
12. Do not modify values, DAX measures, model outputs or filters while changing the visual layer.
13. Do not remove existing routes, interactions, tooltips, filters or dossier navigation.

## 8. Data integrity checks
The latest original reference and latest implementation both show:
- Matheesha Pathirana PRS: `68.75`
- Form & Consistency weight: `10%`

Keep these values only if they match canonical model/config outputs. Verify all weights sum to 100%. Do not hard-code screenshot values over the model/data source. Keep the independent research / not an official RR publication disclaimer visible.

## 9. Final implementation order
1. Import all V3 SVG assets and inspect the two photo source pages.
2. Add the high-resolution landscape Hawa Mahal image and night photo; document attribution and share-alike license in the repository.
3. Fix the hero crop and flag composition first.
4. Fix the sidebar width/logo header and replace the footer skyline with the night photo.
5. Rebuild one player card with transparent portrait + role backplate + fade + PRS placement.
6. Confirm no white rectangle remains; only then apply the pattern to all four players.
7. Upgrade KPI icons and surfaces.
8. Upgrade radar, trend and donut chart lighting without changing any chart data.
9. Validate spacing at 1920×1080 and 1600×900.
10. Run a regression check on every filter, tab, route, dossier button, tooltip and PDF/report control.

## 10. Final acceptance checklist
- [ ] 16:9 desktop composition matches the original hierarchy and density.
- [ ] Sidebar header/logo no longer looks compressed.
- [ ] Sidebar footer uses a real Hawa Mahal night photograph and live disclaimer.
- [ ] Hero uses a high-res recognizable Hawa Mahal photo, not an over-zoomed crop.
- [ ] Flag is large, waving and unboxed; official RR flag/logo used only from approved assets.
- [ ] Five KPI cards use the matching gradient icon family and restrained inner glow.
- [ ] Radar has magenta glow/fill and blue dashed comparison series.
- [ ] Trend has smooth magenta/blue lines, area gradient and glowing points.
- [ ] Donut has subtle outer halo and clean multi-colour segments.
- [ ] Four player cards use four distinct palace-scene backplates.
- [ ] Four player photos are large transparent upper-body cut-outs with no white boxes.
- [ ] Role badges match batter/gold/death/spin colour coding.
- [ ] PRS score sits prominently on the portrait side, not as a tiny detached chip.
- [ ] Stats and CTA align across the four cards.
- [ ] No fake IPL watermark has been added behind charts.
- [ ] All data, model outputs and interactions remain unchanged.
- [ ] Brand disclaimer and third-party image credits are present.
- [ ] No broken images, console errors or missing SVGs in production build.

**Definition of done:** the final screen should visually read like the original premium reference at first glance: photographic Hawa Mahal hero + flag, photographic palace footer, four cinematic player cards with transparent cut-outs, glowing analytics, and the same functioning data experience. This is the last visual pass; do not invent additional decoration once these requirements are met.
