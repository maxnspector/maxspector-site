#!/usr/bin/env python3
"""Build the site's HTML pages from the content files.

  Edit  content/*.yml   ->  run  python3 build.py  ->  HTML is rewritten.

Nothing else changes: the output is plain static HTML, so GitHub Pages keeps
serving it with no build step of its own. Requires only PyYAML.
"""
import sys, yaml, pathlib

ROOT = pathlib.Path(__file__).parent
ASSETS = '/assets/{slug}/'

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def media(it, slug):
    """One image or video inside a .cs-img frame."""
    ratio = (' ' + it['ratio']) if it.get('ratio') else ''
    # `frame: true` keeps the hairline on one piece when the page turns frames off.
    if it.get('frame'): ratio += ' framed'
    base = ASSETS.format(slug=slug)
    # A file name is looked up in this page's assets folder; a name that starts
    # with "/" is taken as-is, so a page can borrow a file from another folder.
    src = lambda n: n if str(n).startswith('/') else base + str(n)
    if it.get('embed'):
        # A self-contained HTML animation. `w`/`h` are the size it was authored at;
        # the page script scales it to fit and only loads it near the viewport.
        w, h = it.get('w', 1440), it.get('h', 900)
        st = []
        if it.get('bg'): st.append(f'--embed-bg:{it["bg"]}')
        if it.get('aspect'): st.append(f'aspect-ratio:{it["aspect"]}')
        if it.get('aspect_phone'): st.append(f'--aspect-phone:{it["aspect_phone"]}')
        style = f' style="{";".join(st)}"' if st else ''
        poster = ''
        if it.get('poster'):
            poster = (f'<img class="embed-poster" src="{src(it["poster"])}" '
                      f'alt="{esc(it.get("alt", ""))}" loading="lazy">')
        # `speed: 1.2` plays the animation faster (read by the shim inside the file).
        url = src(it['embed']) + (f'?speed={it["speed"]}' if it.get('speed') else '')
        attrs = (f'class="cs-img has-img is-embed{ratio}" data-embed="{url}" '
                 f'data-w="{w}" data-h="{h}" data-fit="{it.get("fit", "cover")}"'
                 + (f' data-pad="{it["pad"]}"' if it.get('pad') else '')
                 + (f' data-y="{it["y"]}"' if 'y' in it else ''))
        frame = f'<iframe title="{esc(it.get("alt", ""))}" scrolling="no"></iframe>'
        return f'      <div {attrs}{style}>{poster}{frame}</div>'
    if it.get('video'):
        v = it['video']
        return (f'      <div class="cs-img has-img{ratio}"><video muted loop playsinline preload="none" '
                f'poster="{src(v)}-poster.jpg" aria-label="{esc(it.get("alt",""))}">'
                f'<source src="{src(v)}.mp4" type="video/mp4"></video></div>')
    ast = f' style="aspect-ratio:{it["aspect"]}"' if it.get('aspect') else ''
    # `labels: [top-left, top-right, bottom-left, bottom-right]` puts the brand-plate
    # corner labels over the art as live text; `tone:` light (default) | dark | photo.
    lab = ''
    if it.get('labels'):
        spans = ''.join(f'<span>{esc(t)}</span>' for t in it['labels'])
        lab = f'<div class="cs-labels tone-{it.get("tone", "light")}" aria-hidden="true">{spans}</div>'
    return (f'      <div class="cs-img has-img{ratio}"{ast}>{lab}<img src="{src(it["img"])}" '
            f'alt="{esc(it.get("alt",""))}" loading="lazy"></div>')

LAYOUT = {
    'grid-2':     'cs-grid cs-grid-2',      # two equal columns
    'grid-3':     'cs-grid cs-grid-3',      # three equal columns
    'grid-4':     'cs-grid cs-grid-4',      # four equal columns
    'grid-5':     'cs-grid cs-grid-5',      # five — logo sets
    'grid-6':     'cs-grid cs-grid-6',      # six — logo sets
    'feature':    'cs-grid cs-grid-feature',# 2fr + 1fr, uses `columns:`
    'full':       'cs-grid',                # one item, full column width
    'bleed':      'cs-grid cs-grid-bleed',  # one item, edge to edge
    'asym-left':  'cs-grid cs-grid-asym-left',   # 2 items, wide one on the left
    'asym-right': 'cs-grid cs-grid-asym-right',  # 2 items, wide one on the right
    'feature-even': 'cs-grid cs-grid-feature-even',  # like feature, equal columns
    'text-image': 'cs-grid cs-grid-text-image',        # text then image
    'image-text': 'cs-grid cs-grid-image-text',        # image then text
    'quote':      'cs-grid cs-grid-quote',             # pull-quote, no image
}

def textblock(b):
    paras = b['text'] if isinstance(b.get('text'), list) else [b.get('text', '')]
    ps = '\n'.join(f'        <p>{esc(t)}</p>' for t in paras)
    return f'      <div class="cs-textblock">\n{ps}\n      </div>'

def quote(b):
    cite = f'<cite>{esc(b["attribution"])}</cite>' if b.get('attribution') else ''
    return f'      <p class="cs-quote">{esc(b["text"])}{cite}</p>'

def block(b, slug):
    lay = b['layout']
    cls = LAYOUT[lay]

    def wrap(inner, extra_cls='', style=''):
        # `cols:` sets desktop column widths (phones fall back to the layout's
        # stacking); `gap:` overrides the 24px gutter, e.g. 0 for butted swatches.
        if b.get('class'):   # extra hook class for one-off responsive rules
            extra_cls += ' ' + b['class']
        if b.get('cols'):
            extra_cls += ' has-cols'
            style = (style + ';' if style else '') + f'--cols:{b["cols"]}'
        if 'gap' in b:
            style = (style + ';' if style else '') + f'gap:{b["gap"]}px'
        c = f'{cls}{extra_cls} reveal'
        st = f' style="{style}"' if style else ''
        return f'    <div class="{c}"{st}>\n{inner}\n    </div>'

    if lay == 'quote':
        return wrap(quote(b))

    if lay in ('text-image', 'image-text'):
        art = '\n'.join(media(i, slug) for i in b['items'])
        parts = [textblock(b), art] if lay == 'text-image' else [art, textblock(b)]
        return wrap('\n'.join(parts))

    if lay in ('asym-left', 'asym-right'):
        # Figma: 690 + 486 across the 1200 column, block height 510
        h = b.get('height', 510)
        return wrap('\n'.join(media(i, slug) for i in b['items']),
                    ' is-locked', f'aspect-ratio:1200/{h}')

    if lay in ('feature', 'feature-even'):
        locked = 'height' in b
        cols = []
        for c in b['columns']:
            style = ''
            if locked and len(c) > 1:
                spans = ' '.join(f"{i.get('span', 1)}fr" for i in c)
                style = f' style="grid-template-rows:{spans}"'
            inner = '\n'.join('  ' + media(i, slug) for i in c)
            cols.append(f'      <div class="cs-col"{style}>\n{inner}\n      </div>')
        return wrap('\n'.join(cols),
                    ' is-locked' if locked else '',
                    f'aspect-ratio:1200/{b["height"]}' if locked else '')

    if 'height' in b:   # lock the row to 1200 x height, like asym/feature
        return wrap('\n'.join(media(i, slug) for i in b['items']),
                    ' is-locked', f'aspect-ratio:1200/{b["height"]}')
    return wrap('\n'.join(media(i, slug) for i in b['items']))


def section(s, slug):
    ground = 'cs-dark' if s.get('ground') == 'dark' else 'cs-light'
    sub = esc(s['subhead']) if s.get('subhead') else ''
    if s.get('cite'):
        sub += f'<cite>{esc(s["cite"])}</cite>'
    head = '' if not s.get('heading') else ('    <div class="cs-head reveal">\n'
            f'      <h2 class="cs-h">{esc(s["heading"])}</h2>\n'
            f'      <p class="cs-hsub">{sub}</p>\n'
            '    </div>')
    # `bleed` blocks live OUTSIDE the .wrap so they are full-width by structure,
    # with no 100vw maths that a scrollbar can push past the viewport.
    parts, buf = [], ([head] if head else [])
    for b in s['blocks']:
        if b['layout'] == 'bleed':
            if buf:
                parts.append('  <div class="wrap">\n' + '\n'.join(buf) + '\n  </div>')
                buf = []
            parts.append(block(b, slug))
        else:
            buf.append(block(b, slug))
    if buf:
        parts.append('  <div class="wrap">\n' + '\n'.join(buf) + '\n  </div>')
    return f'<section class="{ground} cs-media">\n' + '\n'.join(parts) + '\n</section>' 

def intro(p):
    i = p['intro']
    meta = '\n'.join(
        f'      <div class="cs-meta-block">\n'
        f'        <p class="cs-label">{esc(m["label"])}</p>\n'
        f'        <p class="cs-body">{esc(m["body"])}</p>\n'
        f'      </div>' for m in i['meta'])
    return ('<!-- INTRO -->\n<section class="cs-light" id="intro">\n  <div class="wrap cs-intro">\n'
            '    <div class="cs-intro-statement reveal">\n'
            f'      <p class="cs-label">{esc(i["eyebrow"])}</p>\n'
            f'      <h1 class="cs-statement">{esc(i["statement"])}</h1>\n'
            '    </div>\n    <div class="cs-intro-meta reveal">\n'
            f'{meta}\n      <p class="cs-body cs-link">{i["links_html"]}</p>\n'
            '    </div>\n  </div>\n</section>')

def build(slug):
    page = yaml.safe_load((ROOT / 'content' / f'{slug}.yml').read_text())
    art = page.get('assets', slug)   # optional: borrow another page's asset folder
    site = yaml.safe_load((ROOT / 'content' / 'site.yml').read_text())
    nav = '\n'.join(f'    <a href="{n["href"]}">{n["label"]}</a>' for n in site['nav'])
    out = (ROOT / 'templates' / 'case-study.html').read_text()
    for k, v in [('TITLE', page['title']), ('DESCRIPTION', page['description']),
                 ('COVER', ASSETS.format(slug=art) + page['cover']), ('NAV', nav),
                 # The intro (description) always comes straight after the cover.
                 # `lead:` is one headless section placed directly after the intro.
                 ('INTRO', intro(page) + ('\n\n' + section(page['lead'], art) if page.get('lead') else '')),
                 ('SECTIONS', '\n\n'.join(section(s, art) for s in page['sections']))]:
        out = out.replace('{{%s}}' % k, v)
    # `frames: off` at the top of a content file drops the hairline round every piece.
    if str(page.get('frames', 'on')).lower() in ('off', 'false', 'none'):
        out = out.replace('<body class="cs-page">', '<body class="cs-page no-frames">', 1)
    # `nav: standalone` — logo stays but links nowhere, and the menu is removed.
    if page.get('nav') == 'standalone':
        import re
        out = re.sub(r'<a href="/" aria-label="Max Spector — home">(.*?)</a>',
                     r'<span class="nav-logo">\1</span>', out, count=1, flags=re.S)
        out = re.sub(r'\s*<button class="menu-btn".*?</button>', '', out, count=1, flags=re.S)
        out = re.sub(r'<div class="overlay" id="overlay">.*?</div>\n', '', out, count=1, flags=re.S)
    dest = ROOT / f'{slug}.html'
    dest.write_text(out)
    n_img = out.count('<img src="/assets/'); n_vid = out.count('<video')
    print(f'built {dest.name}  —  {len(page["sections"])} sections, {n_img} images, {n_vid} videos')

if __name__ == '__main__':
    for slug in (sys.argv[1:] or ['fandom-brand']):
        build(slug)
