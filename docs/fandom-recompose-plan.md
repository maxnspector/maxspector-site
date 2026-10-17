# Fandom page recompose: plan and asset status

Started 2026-10-17. Max walked through the live maxspector.com Fandom pages section by section. This file holds every keep/cut call, the asset status, and the open questions to settle before building.

## The direction

Make the Fandom page feel contemporary and web-first. The old page has too much bespoke layout saved out as single images (print-style collages). Replace them with individual pieces in simple layouts.

Reference: kylebmacy.com/Addison-AI (the work section, not the top). Measured at 1440 wide: 28px page margin, about 32px between pieces, nearly every piece full width, mostly square plus a few 16:10 and 16:9. The open feel comes from one or two large things per screen and few repeated shapes, not from big gaps. Our `bleed` and `flush-pair` layouts already cover this.

Build rule: rebuild brand elements live (SVG logos, real type, HTML swatches) instead of saved-out plates, as on the Alex page.

## Section by section (in walkthrough order)

1. **Lead animation** — the Fandom logo animation starts the work, right after the written intro. Size open (column width or smaller).
2. **Core Brand Elements** — keep, rebuild from source: lockup, mark, wordmark (SVG), type specimens as live Rubik / Space Mono / Space Grotesk, palette as live swatches.
3. **Duotone character grid** — keep some. Group with photo treatments, iconography and illustration styles (one section or several: open). Rebuild with transparent cutouts on live colour panels.
4. **Collage illustrations** (RuPaul/Pikachu, Isabelle diagonal, etc.) — on the fence; at most one or two.
5. **Persona illustration** — keep as is, one image, column or full width (open).
6. **Icons + badges** — split them. Icons keep (live colour columns, possibly full width). The three We Build / Bring / Serve badges on the fence; separate files either way.
7. **Motion Design** — keep "For the Love of Fans" and the mark animation. Logo-reveal stills (wordmark + four Loki frames) on the fence. Drop the three small ones (Top 100 title, lower third, mark on purple). Persona network video: keep part of it, edit by timestamps (Claude can cut and join; Max reviews). Add "By the Numbers" (from the old Fandom Family Brands page).
8. **Social Content** — keep, trimmed. Cut the Wolverine / Horizon / Daredevil row. Keep the John Wick, Knives Out, February Series trio and the Bond panel.
9. **Presentation Design** — keep and grow; bring in pieces from the old standalone presentation page (All Hands 2025, 2024 Look Ahead, Reach Fans, How Should We Work Together 2025, Context Matters). Slides as individual images, full-width singles mixed with pairs.
10. **Core Platform homepage** — remove.
11. **Office Branding** — remove.
12. **GameSpot** — bring in from the old Fandom Family Brands page as its own labelled section; rework the collage. Is / is-not lists and palette as live text (Kanit + JetBrains Mono, both Google Fonts); guide pages from the PDF.
13. **Campaign and event logos** — bring over all eight (Fandom 20, Fandom Stars, AANHPI, Fandom Fest 2022, FanDNA, Global Sales Meeting, Fandom Fest, French Community).
14. **Events** — bring over only the SDCC party section from the old events page, retitled and broadened to events at Fandom.

## Open questions for Max (ask before building)

- Lead animation size: column width or smaller?
- Visual styles: one section, or separate photo treatment / iconography / illustration sections?
- Which one or two collage illustrations, if any?
- Persona illustration: column or full width?
- Badges: keep or cut; if kept, where?
- Logo-reveal stills: keep or cut?
- Social: trim further?
- Presentations: final slide pick.
- GameSpot: guide material only, or also the website review layout, the four social cards and the "Spot On" sub-brand?
- Campaign logos: join "Show Formats & Sub-Brands" as one brand-of-brands section, or stand alone?
- Events: SDCC as hero with a framing subhead, or add one or two pieces from NYCC / Pyrkon?
- Section grounds for every section (white, cream, or a Fandom palette colour).

## Decisions (2026-10-17, second session)

Max accepted these recommendations: lead animation at column width; visual styles as one section; at most one collage illustration (Max picks); badges cut; logo-reveal stills cut; GameSpot = guide material + social cards + Spot On mark, no review layout; campaign logos merge with Show Formats & Sub-Brands into one brand-of-brands section; events = SDCC only with a framing subhead; section grounds decided last, from a rendered preview.
Changed by Max: persona illustration starts at COLUMN width with the 1920px file (no larger export); cutouts (Black Widow, Isabelle, Harry, Miles/spiderverse_map) and John Wick (864px) used as is, Max will find alternatives later if they look soft; presentation slides are standalone images only (no full decks).
Social: Max added more to `Social/` (Andor Empire + Resistance, Eddie Munson wiki, Dumbledore facts, Sonic IG story, Metascore IG story, Tom Cruise By the Numbers). No longer lean.

## Asset check (2026-10-17, second session)

Now in hand: all eight campaign/event logos as SVG (`Sub-brands/`); icons as individual SVGs in dark/light/mid (`Fandomized Icons/`, the `Artboard 1xx` files are duplicates); GameSpot cards, homepage, Spot On, sizzle and review animations; Context Matters + GP slide 04 at 3840; motion files `Motion__sound_eg_1_intro_card` (Fandom logo reveal), `01-21_SonicLogo_Option1a` (mark pattern, 1200 square), `KickoffSizzle_Motion_Part1-a` (24s stats sizzle, 300+ million globe), `BytheNumbers_0314_Intro`.
Size limits: All Hands 2024/2025 (1920) and GP slide 09 (1600) are pair-only; Events folder photos (1080–2117) are pair/grid-only, use archive camera originals (3500+) for any full-width photo. GameSpot `SGF2024_SampleVideo.mp4` (186MB) and `AnimationOutExample.gif` (50MB) need compressing (Claude).
Motion confirmed by Max: "For the Love of Fans" = `Motion_+_sound_eg_4_tagline.mp4` (1920x1080, 6s). Persona network video = `KickoffSizzle_Motion_Part1-a.mov` (24s): 0:00-0:10 is a 300+ million globe and chart intro, 0:11-0:17 the persona network, 0:18-0:24 persona close-ups. Max chose 0:00-0:19.6, ending on the first close-up just before the cream wipe. Encoded to `assets/fandom-brand/motion-persona-network.mp4` (19.6s, 1.6MB, no audio) + `-poster.jpg` at 15s. Replaces the full 24s `motion-sizzle.mp4`.

## Asset status (original, first session)

Asset folder: Dropbox › Spector Documents › Art & Design Projects › Spector › Max Spector Design › Max Spector 2026 › Max Spector Website 2026 › Case Study Files › **Fandom**. Max is adding files at the top level; Claude's pulls from the design archive are in `_from-design-archive/` sorted by section.

Size rule: full-width pieces about 2900px wide, column-width about 2400px. Everything on the current page is capped at 1800px.

**In hand**
- Fandom logo SVGs (lockup, stacked, logotype, mark) and `BytheNumbers_0314_Intro.mp4` — added by Max.
- Fonts: Rubik, Space Mono, Space Grotesk + OFL licence (`01-core/fonts`).
- Palette: `01-core/fandom-palette.md` (3 lead + 8 secondary, from guidelines pp. 21–22). Lead: Red #FA005A, Yellow #FFC500, Purple #520044.
- 2022 brand guidelines PDF (`01-core`).
- Cutouts: Black Widow (996px), Isabelle (592px), Harry (521px, too small).
- Character collages A (2881px) and B (1440px).
- Five persona characters full size + icons; three values badges (1000×1439).
- Social: Glass Onion 1A/1B, February Series, Bond S1–S4.
- Slides rendered at 2880 from the GP decks: Reach Fans, How Should We Work Together 2025.
- GameSpot: 8 logo SVGs, brand guide PDF, colours PDF.
- AANHPI lockup SVG.
- 10 SDCC 2023 party photos including the welcome wall.

**Still needed from Max**
- Miles Morales cutout (not in the archive); larger Harry cutout.
- Icons as individual SVGs (archive has only large .ai files).
- Badges as SVG if kept.
- Campaign logos as SVG (only AANHPI exists; others are small PNGs).
- Motion: best originals of "For the Love of Fans" and the mark animation; persona network video original + timestamps to keep; logo-reveal stills if kept.
- Slides: Context Matters, All Hands 2025, 2024 Look Ahead at full size.
- Any online-only Dropbox files wanted (most SDCC photos, the persona composite, John Wick): make them available offline and Claude can copy them. Claude cannot download online-only files from its side.

## Build v2 (2026-10-17, second session)

Built from the decisions above. `content/fandom-brand.yml` rewritten (old long version kept at `docs/fandom-brand-v1-backup.yml`). Sections: lead logo reveal (video) · Core Brand Elements (SVG lockups on colour panels, live palette, live type panels in Rubik / Space Grotesk / Space Mono) · Visual Language (duotone cutouts on colour panels, personas at column width, 12 icons in four colour columns) · Motion Design (For the Love of Fans, persona network 0:00-0:19.6, mark pattern, By the Numbers; all silent) · Social Content (Andor pair, Tom Cruise, Eddie/Dumbledore/John Wick, Glass Onion pair, Bond) · Presentation Design (Context Matters, All Hands pair, Reach Fans + Work Together) · GameSpot (logos, Spot On, is / is-not lists set live in Kanit + JetBrains Mono, palette, 3 news/quote cards, 3 review cards) · Show Formats & Sub-Brands (3 title cards, 8 SVG logos on panels) · Events (SDCC 2023: key art, welcome wall full bleed, 3 portraits, stairs + letters, arcade neon).
build.py additions: `bg:` / `pad:` / `align: bottom` on images (colour panels), `html:` items with `html_class:` / `ink:` (live type), page-level `css:`. Fonts self-hosted in `assets/fandom-brand/fonts` (woff2, subset).
Grounds (proposed, for Max to review): lead #280033, Core white, Visual #F9EDD8, Motion #520044, Social #86D7DC, Presentation white, GameSpot #00191D, Brands white, Events #280033.
Verified by render at 1440 and 390: 65 images all load, 0px horizontal overflow, all brand fonts load. Videos not playback-tested (container Chromium has no H.264); all five decode with ffmpeg.
Draft copy for Max: Visual Language subhead, Social subhead, Events heading + subhead; Core subhead trimmed; Show Formats subhead cut to its first sentence. Eyebrow changed to "Fandom".
Open: collage illustration pick (none placed); dropped from the old page: anthem film, State of Fandom, Co-Branded, Custom Content, Office, Platform (campaign pieces belong to the new Campaigns collection).
