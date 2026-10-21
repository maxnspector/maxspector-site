# maxspector.com rebuild — build log

A running record of the new hand-coded site. Newest entries at the top.

This file also lives in the repo at `docs/build-log.md`. Edit it there and
re-upload, rather than retyping it.

---

## 2026-10-18 — Fandom polish, Figma rebuilds, Campaigns page

**Fandom.** Palette tiles show hex only, secondaries taller than tertiaries (rows 3fr/2fr). Rubik panel is now purple with yellow type, Space Grotesk yellow with purple; the panels and the palette butt together. Logo row is 3fr/2fr so the cream lockup panel lines up with the three primaries (measured 120–840 both). "Visual Language" renamed "Styles and Image Treatments". Motion Design on brand cream.

**From Max's Figma layouts.** Duotone grid and icon columns rebuilt in Figma as editable layers (79:2); Max recomposed them (82:16878, 82:13986) and the social section (82:27077). Each block exported at 2x and placed to match: personas first, then characters + icons as adjacent 600×640 blocks; social as John Wick panel (640) + Knives Out (560), Bond 1200×675, Andor (472) + stories panel (728), 48px between rows. Blocks stack on phones. Removed from social: Andor Empire, Tom Cruise, Eddie, Dumbledore, the separate Bond slides.

**Campaigns page** (`content/campaigns.yml` → `campaigns.html`, art in `assets/campaigns/`). Four sections: Congregation Beth Sholom (cream), State of Fandom (#294148, cards on #558895), Kayu (cream), Franchise Features (#151516; Skywalker on #C3E9E9, Harry Potter cards on #282821). Grounds read from the live old site. Desktop cover SoF_2026_hero_01; phone cover CC_cover_02_mobile shown whole on #23CCD1 via new `cover_mobile_fit: contain` / `cover_mobile_bg:`. `links_html` is now optional in the intro. Menu and homepage Campaigns row link to `/campaigns.html`. All copy is DRAFT.

Checked at 1440 and 390: all images load, no sideways scroll. All pushed (10-18 1–4).

---

## 2026-10-17 (late evening) — Fandom Build v3, from Max's review

Max reviewed Build v2 and the core problems were process, not taste: art was put on colors Claude picked instead of the ones it had on the old site, cutouts went in uncropped and unscaled, the presentation template collage was dropped and show title cards were added without asking, and the checks only proved images loaded. Two standing rules came out of it: art keeps the background it had on the old site, and American spelling everywhere.

Build v3 was made from the old maxspector.com Fandom and Events pages and Max's original files in Linked Art. Core Brand Elements now opens with the logo reveal on white, then the primary lockup large on cream beside a smaller stacked lockup on purple, a single composed palette block, and one wide Rubik panel over two short ones. Visual Language is on white and uses Max's original duotone grid and icon columns. Social is on purple black with the carousel sets edge to edge and air between groups. Presentation is on cornflower with the template collage back. GameSpot leads with the sizzle and the brand system, no logos. Sub-Brands only, on white, sized to equal visual weight, with Max's fixed French badge. Events uses the old SDCC sequence plus the new Events folder.

`build.py` blocks take `width:` and `space:` (in `content/README.md`). British spellings fixed across the repo. Checked at 1440 and 390: 50 images load, no sideways scroll, every section looked at as a layout. New GameSpot videos not playback-tested. Not pushed. Eight open questions at the end of `docs/fandom-recompose-plan.md`.

---

## 2026-10-17 (evening) — Fandom page rebuilt web-first

All twelve recompose questions settled with Max, the asset folder checked, then the page rebuilt from a new `content/fandom-brand.yml` (old long version kept in `docs/fandom-brand-v1-backup.yml`). Nine parts: logo reveal lead, Core Brand Elements, Visual Language, Motion Design, Social Content, Presentation Design, GameSpot, Show Formats & Sub-Brands, Events (SDCC 2023). 65 images, 5 silent videos.

Brand elements are live, not saved-out plates: SVG logos on color panels, the palette as HTML tiles, type panels set in Rubik / Space Grotesk / Space Mono, and the GameSpot is / is-not lists in Kanit + JetBrains Mono. Fonts are subset woff2 in `assets/fandom-brand/fonts`. `build.py` gained `bg` / `pad` / `align` on images, `html` items (`html_class`, `ink`) and a page-level `css` block; documented in `content/README.md`.

Verified at 1440 and 390: every image loads, no sideways scroll, all brand fonts load. Video playback not tested (test browser lacks H.264); all clips decode in ffmpeg. Not pushed. Details and the review list are in the "Build v2" section of `docs/fandom-recompose-plan.md`.

---

## 2026-10-17 (later) — Fandom page recompose: walkthrough done, assets gathering

Max walked through the live Fandom pages section by section to recompose the case study in a contemporary, web-first way (reference: kylebmacy.com/Addison-AI). Every keep/cut call, the open questions and the asset status are in `docs/fandom-recompose-plan.md`. Headlines: Core Platform and Office Branding cut; GameSpot, campaign logos, By the Numbers and the SDCC party (broadened to events) come in; brand elements get rebuilt live from SVGs, real fonts and HTML swatches.

Assets are collecting in Dropbox `Max Spector Website 2026 / Case Study Files / Fandom`. Claude pulled 50 files from the design archive into `_from-design-archive/` and downloaded the brand fonts (Rubik, Space Mono, Space Grotesk). Online-only Dropbox files can't be copied from Claude's side.

Also today: homepage rows relabelled **Case Study** (Alex, Fandom) and **Collection** (Client Brands, Campaigns placeholders); menus trimmed to Alex AI, Fandom, Client Brands, Campaigns, About; slideshow slides are now links with per-slide captions and smarter autoplay; every headed section gets a link address; Alex Coordinator/Verify heroes replaced (pushed as 10-17 V4).

---

## 2026-10-17 (later) — Slideshow links into pages and sections

Featured Work removed from both menus (Max: it is a homepage area, not a
destination). Menus now: Alex AI, Fandom, Client Brands, Campaigns, About.

The Featured Work slideshow exists to show work you wouldn't otherwise see from
the homepage, especially from the two collections, so each slide now links out
to a page or straight to a section of it.

- **Section addresses.** `build.py` gives every headed section an id from its
  heading (`#office-branding`, `#brand-in-the-world`). `id:` on a section pins
  it. Documented in `content/README.md`.
- **Link check.** Every build now checks each slide link in `index.html` and
  lists any that point at a missing page or section.
- **Landing.** Case-study pages re-jump to the section once everything has
  loaded, so media settling above can't push the target off. Measured: section
  top lands at 0, heading 72px down, nav tucked away, at 1440 and 390.
- **Slides are links** (`<a class="slide" href=… data-caption=…>`). The caption
  under the slideshow now changes per slide and ends with an arrow.
- **Autoplay** pauses while the pointer or keyboard focus is on the slideshow,
  stops for good once the arrows or dots are used, and is off for visitors with
  reduced motion turned on.

Three placeholder slides with DRAFT captions, linking nowhere yet. Needs from
Max: which images go in the slideshow and which project each belongs to.

---

## 2026-10-17 (later) — Case Studies and Collections

Max decided the four destinations split in two: **Case Studies** (Alex AI,
Fandom: a deep dive into one company) and **Collections** (client brands,
campaigns: separate projects shown together). The homepage row label carries
the split.

Homepage (`index.html`, still hand-built): Alex row now links to `/alex.html`
(was the blank template) and its leftover Fandom description is replaced with
a DRAFT placeholder; the Fandom row is retitled "Fandom" and links to
`/fandom-brand.html`. Two new rows labelled "Collection": Client Brands
(big image right) and Campaigns (big image left), with placeholder titles,
DRAFT descriptions and empty image boxes. Checked at 1440 and 390: all four
rows the same height on desktop, no overflow, no script errors. Not pushed;
Max will go live once all four pages are ready.

---

## 2026-10-17 (later) — Coordinator and Verify heroes replaced

Max's narrower `Coordinator - hero_02.png` and `Verify - hero_02.png`
(1888×1422) replace the pair at the bottom of Brand in the World. Saved over
`coordinator-hero.jpg` / `verify-hero.jpg` at 1200×904, JPG q84 (~135 KB each).
The pair's `aspect:` changed from 1200/762 to 1888/1422 so nothing crops.
Measured: 588×443 per image at 1440 (was 588×373), 350×264 at 390, no
horizontal overflow. Not pushed yet.

---

## 2026-10-17 — Alex page: new hero animation, new art, Verify overlays

All rebuilt and render-checked at 1440 and 390 (no overflow, no errors).
Everything except the new lead animation went live in Max's "10-17 V1/V2"
pushes. The animation swap is the only change still to push.

**Lead animation replaced.** The embed at the top is now Max's "Alex Hero
Animation _desktop embed_11" (platform hero v3: It used to take weeks →
Initiate → Screen → Interview → … → Coordinate), saved as
`anim-hero-v11.html` with the speed shim added so `speed: 1.2` still works.
Fully self-contained (no outside requests). New poster
`anim-hero-v11-poster.jpg` is the opening frame. The old
`anim-end-to-end.html` stays in assets, unused.

**Brand in the World, bottom of page.**
- Print one-sheet removed; the digital one-sheet now fills the column at its
  own 5:3 proportions, from Max's new 2700px export (`one-sheet-digital-2400.jpg`).
- Last image is now a side-by-side pair (`grid-2`): `coordinator-hero.jpg` and
  `verify-hero.jpg`, each 1200px wide, 588×373 on the page. From Max's PNGs in
  Dropbox `Max Spector Website 2026 / Case Study Files / Alex AI`.
- Unused now: `product-scheduling.jpg`, `one-sheet-digital.jpg`,
  `one-sheet-print.jpg`. Clear out in the compression pass.

**Verify overlay alternates in Figma.** Two redesigns of the Verify hero's
UI card sit on the "All files" page of the Alex portfolio-artwork file
(x 2395, y 4070): Alt A glass card, Alt B dark compact. Max's final
Verify hero (dark green card) is what went on the page.

**AVIF.** Supported by every current browser; ship with a `<picture>` JPEG
fallback. Plan stands: Max exports full-quality PNG/JPEG, Claude right-sizes
and converts once a page's layout is final.

---

## 2026-10-16 (later) — Site structure: four case studies

Max revised the August 30 plan. The site now has four case studies:

1. **Alex AI** — leads.
2. **Fandom** — renamed from "Fandom Brand". Absorbs the events work (SDCC,
   NYCC, Pyrkon, the anniversary, Community Connect) and GameSpot, each as
   its own clearly labelled section. Fandom now occupies one page, not
   three. GameSpot needs to be easy to find because Max's resume features it.
3. **Client brands** — name still open ("Brand work" was floated). GameSpot
   stays out of it: it was in-house Fandom work, not a client.
4. **New campaign case study** — one-off campaigns that each got their own
   visual world. Starting set: State of Fandom and Harry Potter (moved off the
   Fandom page), Kayu and Beth Sholom (lifted from the client gallery tail).
   Max is hunting for more Kayu and Beth Sholom material and other candidates.
   The title should say what the page proves, not just "Campaigns".

Still to settle: which client projects get their own pages, and the trim on
the Fandom page now that it gains events and GameSpot.

Also today: section subheads (`.cs-hsub`) are no longer italic and dropped
from 16px to 14px, site-wide.

---

## 2026-10-16 (later) — Alex palette: warning red removed

Max compared three layouts without warning red and chose B. The supporting
block is now three tiles across the top (Secondary gray, Secondary sage,
Accent green) over three full-width pastel strips (mint, tan, sage). Grid is
`cols: 1fr 1fr 1fr`, `rows: 47fr 17.67fr 17.67fr 17.67fr`, same 1200/786
frame. Checked at 1440 and 390: no overflow, every label fits, and the halves
still stack on a phone. Not committed yet.

---

## 2026-10-16 — Alex page: Verify animation, swag, palette in HTML

Edits to `content/alex-ai.yml` (page published at `/alex`), all rebuilt and
render-checked, none committed yet.

**Feature Animations.** The Verify product hero is in at full column width,
between the trio and cheat detection: `anim-verify-product.html` plus
`verify-product.mp4` (Max's newer optimized cut, audio track stripped, 1.9 MB).
The chat overlay is adapted from Max's alex.com homepage Verify module and
laid out to the four "Verify product hero" storyboards. All four stages were
checked in sequence using a temporary WebM copy, because the test browser can't
decode H.264. The workflow (cadences) animation now has the hairline frame.

**Brand in the World.** Subhead is now "How Alex shows up for candidates and
customers. Photography, office signage, swag, and sales materials." Order: the
three product photos, the lobby, the sales deck grid (`sales-deck-overview.jpg`,
from Sales - Presentations), the swag set (`swag-set.jpg`, from Swag), the
one-sheets, then scheduling.

**Palette is live HTML now.** The two palette images are replaced by a new
`swatches:` item type in `build.py`. Each swatch reuses the `.cs-labels`
corner-label type, so names and hex values match the identity plates exactly
(11px at a 20px inset; 10px at 12px on phones). Text goes light or dark by the
swatch's brightness. The two halves still stack on a phone. The old
`palette-main.jpg` / `palette-support.jpg` remain in assets, unused.

**Next session starts with:** a couple of palette options where warning red
goes away.

---

## 2026-10-16 — Flush layouts, and a background for every section

**Six new arrangements**, from Figma node 62:9. The pieces touch — no gutter
between them. Each comes at content width and full bleed:

| layout | content width (1200) | full bleed (1440) |
|---|---|---|
| `flush-pair` | 600 + 600 | 720 + 720 |
| `flush-wide-pair` | 1200×675, then 600 + 600 | 1440×810, then 720 + 720 |
| `flush-pair-wide` | 600 + 600, then 1200×675 | 720 + 720, then 1440×810 |

Add `-bleed` for the edge-to-edge version. Every number was measured against
the rendered page and matches the Figma file exactly. No horizontal overflow
at 1440 or 390; on a phone the two squares stack rather than squeezing.

**Backgrounds are now named per section.** `ground:` on a section takes
`white`, `cream`, `dark`, or any hex such as `"#1B2A3A"`. Type on a custom
color is set light or dark automatically by measuring the color's
brightness. The hex must be quoted or YAML reads the `#` as a comment.

**The convention, from Max.** On the existing maxspector.com every section of
a case study has a different background, and that carries over: three
categories — white, brand cream, or a color matching the case study. The
intro under the cover is always cream. The page itself is white, and each
section paints over it. A section with no `ground:` falls back to white, but
that is a fallback, not a choice — on a finished page every section names one.
The build now prints how many are still falling back.

**A stale assumption, corrected.** Claude asked Max to choose a default while
describing the cream/white alternation as current behavior. It wasn't: on
10-04 a CSS rule had been added forcing every light section white, with the
intro pinned to cream. The question was built on a picture twelve days out of
date. That 10-04 decision has been kept, but it is now decided in `build.py`
and written onto each section rather than forced in CSS — so a named ground
is never overridden. `grounds: alternate` at the top of a content file brings
the alternation back for that page; the layout catalog is set that way.

**Still to assign:** Fandom Brand has 9 of 11 sections with no ground, Alex
has 4 of 5. Those need Max's color choices before either page follows the
convention.

**Housekeeping:** a stale `.git/HEAD.lock` blocked a commit again. Claude
can't delete inside the repo, so it was renamed to
`.git/stale-head-lock-20261016` — safe for Max to delete.

---

## 2026-10-04 — Alex AI page, V1 for a job application

Max needed his recent Alex work in front of a hiring manager today, so the
Alex AI case study got a fast V1 built on the existing page. It's generated
from `content/alex-ai.yml`, and Max pushed it live the same day.

**What's on it.** The keynote stage mock is the cover; Max chose to keep the
full-bleed zoom so it matches the Fandom page. The intro copy is Max's own:
the statement, Roles & Responsibilities, and "Learn more at alex.com". There
were no other contributors, so the Team block was dropped. There are six
sections: Brand Identity, How Alex Works, Product in Motion (dark), Feature
Animations, Product Imagery, and Brand in the World. Each section subhead
still starts with "DRAFT —".

**Brand plates.** Five new plates: the primary lockup, the mark light-on-dark
and dark-on-light, the palette, and a DM Sans specimen. They're built from the
production SVGs in Core Assets and the nine palette colors read exactly from
Figma: #082900, #EEF2E1, #6B7F66, #B7C7A7, #D3E1C9, #DFD7C0, #BAD1C0, #009B58
and #C92626. The neutral 50–950 scale was not read, so it isn't on the page.
DM Sans was pulled out of the fonts embedded in the hero animation file.

**Animations.** Eight live HTML embeds: end-to-end hiring sequence, dark
product hero, live interviews, talent match, AI interviews, identity
verification, cheat detection, and interview everyone. Four MP4s were encoded
from the 4K exports: resume screens, verify, coordinator and fraud. Using the
MP4s avoids the unpkg dependency the HTML versions of those pieces have.

**Where the art came from.** Most pieces came from the Alex AI library at
`Dropbox/Spector Documents/Design archive/Alex AI` (Videos & Animations, Core
Assets, Brand Visual Style, Portfolio Files). Five exist only in Figma, and
Max exported those himself: the scheduling phone shot, the two square social
cards, and the two blurred-office logo frames. Claude resizes and compresses
everything on its end, so Max doesn't need to optimize exports first.

**Figma limit.** Max's Starter plan caps Figma MCP calls, and the cap was hit
mid-session. Prefer library sources over Figma pulls. (Max upgraded his plan
later the same day, so the cap no longer applies.)

**Commit blocked.** GitHub Desktop refused to commit because of two empty,
stale git lock files (`.git/index.lock` and `.git/HEAD.lock`) left over from
September 25. Deleting them cleared it.

**Verified** at 1440 and 390: no horizontal overflow, no broken images, no
console errors, all 8 embeds load. The MP4s can't be checked in the headless
browser (it has no H.264 decoder). They were encoded with the recipe the
Fandom page already uses.

---

## 2026-09-26 — Contact sheets for the animation library

Dropbox had more files than the first pass saw — 49 HTML animations in the
Alex AI folder, 39 of them distinct once identical copies are collapsed. Ten
had not finished syncing when I first looked: Proctor hero (desktop and
mobile), identity verification (desktop and mobile), Verify_animation_dt_03,
Resume Screens v3 and the M3 fit-bar version, Talent Match mobile, and the two
Alex AI Interviews files.

Every one of the 39 was run in a browser and photographed at 1.5, 7 and 15
seconds. Seven contact sheets, saved to **Alex AI / animation-contact-sheets**.

**A live gallery too.** `animation-gallery.html` sits in the Alex AI folder and
runs all 39 for real, in a labeled grid, loading each as you scroll to it. It
is built by `build-animation-gallery.py` beside it — re-run that any time
files are added and the gallery rebuilds itself. Verified it works opened
straight from the Finder, no server needed.

**The dependency split.** 22 are completely self-contained and can go into a
page today. 16 pull a script from unpkg.com, and the work network blocks that
host, so those render as a flat background color and nothing else — the gray
panels on the sheets. They are not broken; they just cannot draw without the
library. Before any of them can ship, that library has to be baked into the
file. The affected pieces are the four Accelerate Hiring ones (Engage
Instantly, Evaluate Fairly, Hire Faster in two versions), Resume Screens v2
and v3, Alex Workflows desktop, Verify_animation_dt_03, and both Alex AI
Interviews files.

**Two notes for picking.** `Alex Hero Animation _standalone_4.html` shows its
own playback controls along the bottom — fine on its own, wrong inside a page.
And `Agentic-Recruiting-Platform-Dark-V2.html` is not an animation at all; it
is the whole platform web page, and it reaches out to alex.com for assets.

---

## 2026-09-26 — The animation library

**What's already on the Mac.** 36 HTML animations in the Alex AI folder. 20 of
them are completely self-contained — no external files of any kind — which is
exactly what the `embed:` type wants. Those can go straight into pages. Seven
smaller ones pull a script from unpkg.com and fonts from Google, so they'd
need that inlined before they could be counted on.

Roughly what's there: several versions of the platform hero, Talent Match,
End to End Hiring, Interview Everyone, Candidate Blueprint, the Signal Cascade
fraud pieces, Alex Workflows, and the four "Accelerate Hiring" pieces
(Engage Instantly, Hire Faster, Evaluate Fairly). Most exist in two or three
versions, so each needs a look before picking one — the same trap as the
GameSpot folder.

**Pulling one down from Netlify.** Max's machine can't reach netlify.app — the
work network blocks it — so curl and wget are out from there. Claude's own
browser can reach it and read the actual source file, which is what matters:
a deployed page saved from the rendered screen is a snapshot that won't
animate again.

Saved this way, byte-for-byte: `alex-live-interviews.html` (7 KB) from
alex-built-for-industries.netlify.app, now in Alex AI / Videos & Animations.
A dark piece — four role cards cycling through interviewing and scored states
over a live counter, looping forever with no controls. It runs on the Alex
brand dark (#082900), so it would sit naturally as one of the dark chapter
breaks.

Its only outside dependency is DM Sans from Google Fonts.

**The rule of thumb.** Small self-contained pages pull down cleanly through
the browser. Anything large or built as a bundle should come from the original
export instead — the deployed build is the wrong thing to copy.

---

## 2026-09-25 — Live HTML animations

Animations exported as single HTML files now run directly on the page. No
video file, no quality loss, and roughly a twentieth of the weight — the Alex
hero animation is 1.5 MB as HTML against 29 MB as a .mov.

**How it works.** A new `embed:` field sits alongside `img:` and `video:` in a
content file, so an animation drops into any layout the template already
knows. The animation is authored at a fixed size (1440 × 900 for this one) and
the page scales it to whatever frame it is placed in. It loads only when you
scroll near it, and a still image stands in until it is ready. With reduced
motion turned on it never loads at all — the still is all you get.

**Where it went.** The Alex hiring sequence runs as a full-bleed section on
the Alex AI page rather than as the page hero. It is a 36-second, six-step
narrative with its own controls, so it needs to be a thing you arrive at, not
something playing behind the title.

**Two bugs found and fixed while verifying.** Image frames were missing
`position: relative`, so anything layered inside one was anchored to the page
instead of the frame. And a later background rule was overriding the
animation's own ground color. Both were pre-existing; neither had shown up
until an embed exercised them.

**Also.** A file name starting with `/` is now taken as a literal path, so one
page can borrow art from another page's folder. The layout catalog gained an
animation example, and the content README documents the new fields.

Verified at 1440 and 390: no horizontal overflow, no console errors, the
animation renders and plays, the still fades out on load, and reduced motion
suppresses it entirely.

---

## Where things stand

**Built**

- Content-first build system — YAML content files compile to static HTML
- Fandom case study — Build v3 2026-10-17 late evening from Max's review:
  8 sections, 50 images, 7 videos (not yet pushed)
- Alex AI page — V1 live 2026-10-04: Max's intro copy, brand plates, 8 live
  animations, 4 videos, product and campaign art
- Campaigns collection — built 2026-10-18, four sections, draft copy
- Layout catalog — every arrangement on one page for reference, including
  the six flush layouts and a custom-color section
- Section grounds named per section: white, cream, brand dark, or any color
- Scroll motion, hover, and the coral dropdown nav

**Next session starts here**

1. **Campaigns review.** Max checks the page on staging; supply intro and subhead copy, a title for the fourth section ("Franchise Features" is a placeholder), and images for the homepage Campaigns row. Decide Beth Sholom cream vs white.
2. **Mockups.** Pick the first real-world mockups (State of Fandom keynote auditorium, Beth Sholom brochure, Kayu postcards/hangtag/catalog, franchise pages on devices); Max supplies base photos; Claude composites the real art in.
3. **Client Brands collection.** Name it and build it.
4. **Fandom leftovers:** Black History Month logo file, Spot On / SGF video, draft subheads, the slideshow link to #office-branding.
5. **Alex AI:** homepage description, section grounds, clear the "DRAFT —" subheads.

**Further out**

- Compress images once the design is locked. Right-sizing alone takes the
  Fandom page from 16.3 MB to 10.4 MB; AVIF on top takes it to 4.1 MB. 65 of
  85 images are oversized by more than a quarter even at 2× retina. Open
  question: replace the JPEGs in place, or write to a separate folder for
  comparison first.
- Bake the unpkg library into the 16 animations that need it.
- GameSpot case study — unblocked now that the brand guide has turned up.
- Sync the nav on the homepage and the old template to the shared one.
- Convert the homepage to the content system.
- Build the CMS, once a second case study has proven the content model.
- Staggered/offset pairs — the one layout from the original wish-list still
  unbuilt.
