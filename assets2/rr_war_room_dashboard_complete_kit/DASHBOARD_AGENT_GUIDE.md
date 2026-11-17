# RR WAR ROOM — Dashboard Agent Implementation Brief
Version: 1.0  
Purpose: Rebuild the current dashboard so it matches the premium reference mockup, not merely its colour palette.

## 1. The visual target

The target is a high-end cricket scouting command centre:
- deep navy/near-black canvas
- restrained violet atmospheric lighting
- magenta for primary emphasis and PRS
- blue for secondary comparison series
- gold for high-impact / auction-value emphasis
- crisp, readable typography
- large, photographic player profiles integrated into richly layered cards
- a wide hero banner with palace architecture and a small royal flag/crest
- dense but well-spaced executive analytics

Do not turn it into a generic purple admin template. The current implementation is already close in structure, but it looks flatter and more compressed than the target.

## 2. What is missing / what to change from the current screenshot

### A. Hero banner
Current: flat purple rectangle with a faint skyline and a small square badge.  
Target: cinematic layered hero with a more visible palace silhouette on the right, subtle radial magenta glow, dark left-side text-safe zone, and a more intentional royal flag/crest treatment.
- Use `hero_palace_horizon.svg` as the right-side architecture layer.
- Use `royal_flag.svg` as a small floating flag asset OR use the crest; do not use both at large size.
- Put the title and subtitle on the left, vertically centred.
- Keep a dark gradient overlay behind text. Never place detailed art behind the title.

### B. Player profiles — biggest visual difference
Current: small circular player cut-outs with too much empty coloured space around them.  
Target: larger, more immersive player photography, with the player's upper body occupying a substantial part of the top half of each card.
- Use licensed/approved player photos, not generated lookalikes.
- Prefer transparent-background cut-outs or clean studio portraits. If only rectangular photos are available, use `object-fit: cover` and a carefully selected `object-position`.
- Use `player_portrait_arch.svg` for a subtle arched frame OR `player_portrait_frame.svg` for a circular portrait. Do not use both on the same card.
- Avoid tiny circular thumbnails. Portrait should visually dominate the upper card region.
- Put role badge at top-left, PRS score at top-right or beside the player name.
- Place a subtle palace silhouette behind the player, low contrast only.
- Ensure player name and role remain readable over the image with a bottom gradient.

### C. Player cards
Current: card background is too bright/flat, card details are compressed, and the lower area feels crowded.
- Use the existing `card_batter_bg.svg`, `card_finisher_bg.svg`, `card_death_bg.svg`, `card_spin_bg.svg` from the original asset pack as low-opacity backgrounds.
- Add a dark translucent overlay (roughly 55–75% opacity) below the portrait to protect text contrast.
- Use `player_card_bottom_wave.svg` only as a subtle bottom accent (opacity 0.25–0.45).
- Keep cards equal height and align their bottoms.
- Card hierarchy: role badge → portrait → name + role → PRS → 4 compact stats → full dossier CTA.
- Keep stat labels muted and values bright. Use green only for positive deltas, gold for target price, magenta for PRS.
- Do not put important text over a busy skyline or photograph.

### D. Left sidebar
Current: narrow and visually plain; lower dossier panel has a simple skyline.
- Use `palace_silhouette.svg` from the original pack or `hero_palace_horizon.svg` cropped at the bottom of the sidebar.
- Add a subtle violet/magenta glow behind the bottom dossier panel.
- Keep navigation icon size consistent (20–22px), labels 14–15px, active row magenta gradient with a restrained glow.
- Keep footer dossier copy legible; do not shrink it to tiny text.

### E. Main analytics panels
Current: charts are clear but small and low-contrast.
- Increase chart title and axis/legend readability.
- Preserve the radar, trend and model-balance panels and align their top and bottom edges.
- Make gridlines subtle, not invisible.
- Radar: current squad = magenta solid line/area; league average = blue dashed line.
- Trend: PRS = magenta line; HP% = blue line/area. Use one clear axis for each metric.
- Donut: keep labels and percentages aligned; use consistent colours.
- Do not use 3D charts, bevels, or excessive glow.

## 3. Layout and sizing rules

Use responsive layout, but for a 16:9 desktop canvas (e.g. 1920×1080):
- sidebar: 260–280px fixed
- top bar: 64–76px
- page padding: 28–36px
- hero: 150–180px tall
- KPI row: 5 equal cards, 90–110px tall
- analytics row: 3 columns; approx. 1.0 : 1.75 : 1.0 widths
- profile cards: 4 equal columns, 300–360px tall
- card gutters: 16–20px
- panel radius: 14–18px
- internal panel padding: 18–22px

For smaller screens:
- collapse sidebar to icon rail or drawer
- KPI cards wrap to 2 columns
- analytics panels stack
- player cards become 2 columns, then 1 column
- never scale all text down to fit. Reflow instead.

## 4. Colour tokens

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

Use magenta for primary selection/PRS, blue for HP% or league comparison, gold for high-impact/auction target, green for positive movement. Avoid assigning random colours to the same metric on different pages.

## 5. Typography

Use a clean modern sans-serif:
- preferred: Inter, Manrope, or Plus Jakarta Sans
- page title: 28–34px / 700–800 weight
- section heading: 16–19px / 700
- card player name: 18–21px / 700
- KPI number: 24–30px / 700
- body labels: 13–15px
- chart axis labels: 11–12px minimum on desktop
- metadata: 11–12px, never below 10px

Do not use condensed or futuristic fonts for all text. Use tabular numerals for metrics.

## 6. How to use the SVG assets

The kit has two folders:
- `original_assets/`: original 20 SVG assets
- `supplemental_assets/`: new visual assets added after reviewing the current screenshot

Use:
- `rrw_crest.svg`: small sidebar/header mark. It is a generic crest, not the official team logo.
- `hero_palace_horizon.svg`: hero right-side palace artwork.
- `royal_flag.svg`: optional small decorative flag; do not let it compete with the title.
- `stadium_glow.svg`: very low-opacity page/hero atmosphere.
- `palace_silhouette.svg`: sidebar footer or card background, cropped.
- `card_*_bg.svg`: matching player-role background for each profile card.
- `player_portrait_arch.svg`: frame behind a large upper-body portrait.
- `player_portrait_frame.svg`: alternative circular photo frame.
- `player_card_bottom_wave.svg`: subtle lower card flourish.
- `royal_corner_glow.svg`: clipped glow behind a panel/card corner.
- `player_role_badge.svg`: decorative badge background; put role text as HTML/UI text on top.
- `section_divider.svg`: section separator.
- `icon_*.svg`: consistent outline icons for KPIs/navigation.

SVG files are vector assets; keep them as separate files or inline them. Do not rasterize them unnecessarily. If Power BI does not render a specific SVG source path, convert only that asset to PNG at 2× or 3× size, keeping transparency.

### Power BI notes
- For image visuals, use a publicly accessible HTTPS URL or a supported data URI, depending on the visual and tenant settings.
- For SVG data URIs, encode the complete SVG as a data URI and set the field's Data Category to Image URL where supported.
- Some built-in Power BI visuals restrict SVG/data URI rendering. If blocked, use an approved HTML/SVG custom visual or export SVG to transparent PNG.
- Avoid using local filesystem paths in a published report; local paths will not resolve for report viewers.
- Test in Power BI Desktop and Power BI Service. They can behave differently.

### Web app notes (React / CSS)
- Use `<img>` for standalone SVG assets or CSS `background-image` for decorative layers.
- Use `object-fit: cover` for photo containers and tune `object-position` per player.
- Keep text and buttons as real DOM elements, not baked into SVG artwork.
- Use `aria-hidden="true"` for decorative SVGs; provide alt text for meaningful images.
- Use `loading="lazy"` for player images below the fold.

## 7. Player photo handling

The SVG pack intentionally does NOT include player photographs. Use genuine, approved/licensed images from the project's permitted image source.
- Keep one consistent crop treatment across all cards.
- Prefer high-resolution source images (at least 700px tall for large profile cards).
- Use object-position per player; do not crop faces, shoulders, or team jersey logos awkwardly.
- Do not synthesize or alter a real player's identity.
- Add a dark bottom gradient over photos so names and scores stay readable.
- If image rights are uncertain, use neutral initials/role silhouettes until approved photos are available.

## 8. Data and factual integrity — non-negotiable

Do not invent or silently alter:
- PRS scores
- player names, roles, metrics, price targets
- match counts, ball counts, HP totals
- model accuracy or calibration
- shortlist size
- model weights or trend values

The screenshot contains a visible inconsistency: Matheesha Pathirana's PRS appears as 68.75 in the current page while the earlier reference showed 60.75. Do not choose one by guessing. Read the canonical dataset/model output and display the correct value consistently across KPI cards, player cards, filters, and dossiers.

Also verify the model balance values. The current screenshot shows Form & Consistency 10% in the earlier reference but 18% in the latest render; use the canonical model config. The percentages should sum to 100%.

Do not claim "official Rajasthan Royals" or use official franchise branding unless permission exists. Keep the research-dossier disclaimer visible.

## 9. Common mistakes to avoid

1. Making player portraits tiny circular thumbnails when the reference uses large integrated player photography.
2. Using flat, saturated colour blocks instead of layered gradients, shadows and restrained atmospheric art.
3. Making the hero skyline too faint or placing it behind text.
4. Shrinking typography to fit too many metrics.
5. Mixing accent colours inconsistently across charts and cards.
6. Using glow on every border, button and icon. Glow should be selective.
7. Putting labels or important numbers inside SVGs; keep text live and responsive.
8. Repeating fake or placeholder data in multiple components.
9. Hardcoding values that should come from the canonical data/model output.
10. Using remote player-image URLs without checking that they load, crop correctly, and are permitted.
11. Stretching SVGs out of aspect ratio.
12. Using a screenshot as the dashboard background. Build real responsive components and charts.

## 10. Acceptance checklist

Before calling the dashboard complete:
- [ ] Hero has visible, layered palace artwork and clean text-safe space.
- [ ] Player portraits are large, high quality, consistently cropped, and not tiny circles.
- [ ] Four cards have distinct role accents but consistent layout.
- [ ] Player names, PRS and all statistics are readable at 100% zoom.
- [ ] KPI row, analytics panels and profile cards align cleanly.
- [ ] Charts use consistent metric colours and correct scales.
- [ ] Sidebar footer has subtle palace art without hurting navigation readability.
- [ ] All filters, tabs and dossier buttons actually work.
- [ ] Data values match the canonical source; no invented values.
- [ ] Desktop and tablet layouts reflow rather than compress.
- [ ] No broken images, SVGs, console errors or inaccessible text.
- [ ] Disclaimer remains visible: independent research dossier / not an official publication.

## 11. Suggested build sequence

1. Lock the canonical data and resolve the two visible metric discrepancies.
2. Load the asset files and establish CSS colour/spacing/type tokens.
3. Rebuild hero banner with layered palace artwork.
4. Rebuild one player card to the target hierarchy and photo scale.
5. Duplicate the validated card for the other three profiles.
6. Refine analytics panel typography and spacing.
7. Refine sidebar footer and micro-interactions.
8. Test responsive breakpoints and published deployment.
9. Compare a 1920×1080 screenshot side-by-side with the target and fix differences.

The goal is a functional dashboard that looks like a premium executive scouting product—not a static mockup.
