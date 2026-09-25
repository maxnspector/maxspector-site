# Editing the site content

The pages in this repo are **generated** from the files in this folder.
You edit a `.yml` file, run one command, and the HTML is rewritten for you.

Never edit `fandom-brand.html` directly — the next build overwrites it.

## Making a change

1. Open the file you want in any text editor.
2. In Terminal, from the repo folder, run:

       python3 build.py

3. Commit and push in GitHub Desktop as usual.

To build just one page: `python3 build.py fandom-brand`.

---

## Everyday edits

**Change some words.** Find the line and type over it. Headings, subheads and
body copy are all plain text.

**Swap an image.** Change the file name after `img:`. The file needs to be in
`assets/fandom-brand/` — write just the name, not the path.

**Add an image.** Add another entry under `items:`, matching the indentation of
the one above it:

      - img: new-picture.jpg
        alt: What the picture shows
        ratio: wide

**Reorder sections.** Move a whole `- heading:` block up or down the list.

**Delete a section.** Delete the block. The cream-and-white alternation
re-sorts itself, so nothing downstream breaks.

**Alt text** is the description read aloud by screen readers and shown if an
image fails to load. Worth writing properly — it's also read by search engines.

---

## What's in this folder

- **`site.yml`** — the dropdown menu and the footer. Shared by every page, so
  changing the menu here changes it everywhere at once.
- **`fandom-brand.yml`** — the Fandom Brand case study: cover, intro copy, and
  every section in order.
- **`_layouts.yml`** — a demo page showing every layout. Not part of the site.
  Build it with `python3 build.py _layouts` and open `_layouts.html`.
- **`README.md`** — this file.

---

## How a page is put together

    sections:
      - heading: Motion Design            # the big serif headline
        subhead: Expressing the brand…    # the small italic line under it
        ground: dark                      # optional — see "Two rules" below
        blocks:
          - layout: grid-2
            items:
              - img: motion-hero.jpg
                alt: Animated logo build
                ratio: video

A **section** is one titled chunk of the page. Each section holds one or more
**blocks**, and each block is a row of images in a particular arrangement.

---

## Reference: layouts

`python3 build.py _layouts` builds a page showing all of these together.

| `layout:`    | what it does                                        |
|--------------|-----------------------------------------------------|
| `grid-2`     | two equal columns                                   |
| `grid-3`     | three equal columns                                 |
| `grid-4`     | four equal columns                                  |
| `grid-5`     | five across — logo sets                             |
| `grid-6`     | six across — logo sets                              |
| `feature`    | a wide column beside a narrow one                   |
| `full`       | one item across the content column                  |
| `bleed`      | one item, edge to edge past the margins             |
| `asym-left`  | two images, the wide one on the left (690 / 486)     |
| `asym-right` | the same, reversed                                  |
| `feature-even` | like `feature`, but equal columns                 |
| `text-image` | words on the left, image on the right               |
| `image-text` | the same, reversed                                  |
| `quote`      | a centred pull-quote, no image                      |

Most layouts just take a list of `items:`. Three need something different.

**`asym-left` and `asym-right`** take two images. They are locked to a fixed
shape, so `ratio` is ignored inside them — the images fill their frames.

**`feature`** nests one level deeper, because each column holds its own list:

    - layout: feature
      columns:
        - - img: illo-icons.jpg
            ratio: wide
          - img: illo-photo-treatments.jpg
            ratio: wide
        - - img: illo-values.jpg
            ratio: tall

### Locking a block to a fixed shape

Add `height:` to a `feature` and the whole block locks to that proportion,
measured against the 1200 grid — so `height: 1112` is the same shape you drew
in Figma. The columns then divide that height between them instead of each
image keeping its own ratio.

Inside a locked block, `span:` sets how tall each image is relative to the
others in its column. They can be any numbers — use the ones from your Figma
file and it will match:

    - layout: feature
      height: 1112
      columns:
        - - img: left-top.jpg
          - img: left-bottom.jpg
        - - img: right-1.jpg
            span: 300
          - img: right-2.jpg
            span: 464
          - img: right-3.jpg
            span: 300

Leave `span:` out and the images divide the height evenly. Leave `height:` out
and the block behaves normally, with each image keeping its own `ratio`.

**The three word-based layouts** take `text:` instead of, or as well as,
images:

    - layout: quote
      text: This work is an investment in company culture.
      attribution: Fandom's Chief Revenue Officer

    - layout: text-image
      text:                     # one line, or a list for several paragraphs
        - First paragraph.
        - Second paragraph.
      items:
        - img: illo-comic-characters.jpg
          ratio: wide

---

## Reference: image shapes

`ratio` sets the shape of the frame. Leave it out for a square.

| `ratio:`   | shape | good for                  |
|------------|-------|---------------------------|
| *(none)*   | 1:1   | logos, social posts       |
| `photo`    | 3:2   | single frames, full bleed |
| `wide`     | 16:10 | most layouts and spreads  |
| `video`    | 16:9  | video frames, slides      |
| `portrait` | 4:5   | tall social cards         |
| `tall`     | 3:4   | posters, standing artwork |
| `pano`     | 21:9  | wide banners              |
| `ultra`    | 3:1   | very wide strips          |

The image is cropped to fill the frame, so pick the shape closest to the
artwork to avoid losing anything important at the edges.

---

## Reference: video

Use `video:` with the file name **without** its extension:

      - video: motion-anthem
        alt: Brand anthem film
        ratio: video

It expects two files in the assets folder: `motion-anthem.mp4` and
`motion-anthem-poster.jpg`. The poster is the still shown before the video
starts. Videos play silently, loop, and only run while on screen.

---

## Reference: animations

An animation exported as a single HTML file runs live on the page — no video
file, no loss of quality, and a fraction of the weight. Use `embed:` in place
of `img:`:

      - embed: hero-animation.html
        poster: hero-animation-poster.jpg
        alt: The Alex hiring sequence, animated
        ratio: wide
        w: 1440
        h: 900
        bg: "#EEF2E1"

| field     | what it does                                                     |
|-----------|------------------------------------------------------------------|
| `embed`   | the HTML file in the assets folder                                |
| `poster`  | a still shown until the animation has loaded (optional, advised)  |
| `w` / `h` | the size the animation was designed at — 1440 x 900 unless told   |
| `bg`      | the animation's own background colour, so the frame matches it    |
| `fit`     | `cover` fills the frame and crops; `contain` fits it all in       |

The animation only loads once you scroll near it, so it costs nothing until
it is wanted. With reduced motion turned on it never loads at all and the
poster stands in.

To borrow a file from another page's assets folder, write the whole path
starting with a slash — `/assets/alex-ai/hero-animation.html`. This works for
images and video too.

---

## Two rules worth knowing

**Backgrounds alternate on their own.** Light sections run cream, white, cream,
white down the page, and `ground: dark` marks a chapter break. The alternation
counts from the top, so leave the cover and the intro where they are.

**Watch out for colons in your writing.** If a line of text contains a colon
followed by a space, wrap that whole line in "double quotes" — otherwise the
build stops with an error. Everything else can be typed plainly.
