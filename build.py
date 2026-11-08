#!/usr/bin/env python3
"""Build the site's HTML pages from the content files.

  Edit  content/*.yml   ->  run  python3 build.py  ->  HTML is rewritten.

Nothing else changes: the output is plain static HTML, so GitHub Pages keeps
serving it with no build step of its own. Requires only PyYAML.
"""
import sys, yaml, pathlib, re

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
                 + (f' data-y="{it["y"]}"' if 'y' in it else '')
                 + (f' data-zoom="{it["zoom"]}"' if it.get('zoom') else '')
                 + (f' data-cy="{it["cy"]}"' if 'cy' in it else '')
                 + (f' data-cx="{it["cx"]}"' if 'cx' in it else ''))
        frame = f'<iframe title="{esc(it.get("alt", ""))}" scrolling="no"></iframe>'
        return f'      <div {attrs}{style}>{poster}{frame}</div>'
    if it.get('swatches'):
        # Color palette drawn as live HTML (Max 2026-10-16), so the names and hex
        # values use the same corner-label type, size and 20px inset as the brand
        # plates. `cols` / `rows` are CSS grid tracks; each swatch takes
        # name, hex, optional col/row ("1 / 3"), and kind: tile (hex bottom-left,
        # the default) or strip (hex top-right).
        cells = []
        for c in it['swatches']:
            hx = c['hex']
            ink = 'rgba(238,242,225,.85)' if _luma(hx) < 0.5 else 'rgba(8,41,0,.72)'
            pos = ''.join(f'grid-{k}:{c[k]};' for k in ('column', 'row') if c.get(k))
            nm = '' if c.get('hide_name') else c['name']   # hide_name: hex only
            spans = ([nm, hx.upper()] if c.get('kind') == 'strip'
                     else [nm, '', hx.upper()])
            lab = ''.join(f'<span>{esc(t)}</span>' for t in spans)
            cells.append(f'<div class="cs-swatch" style="background:{hx};color:{ink};{pos}">'
                         f'<div class="cs-labels">{lab}</div></div>')
        st = (f'grid-template-columns:{it.get("cols", "1fr")};'
              f'grid-template-rows:{it.get("rows", "1fr")};'
              + (f'aspect-ratio:{it["aspect"]};' if it.get('aspect') else ''))
        return (f'      <div class="cs-img has-img cs-swatches{ratio}" style="{st}" role="img" '
                f'aria-label="{esc(it.get("alt", ""))}">{"".join(cells)}</div>')
    if it.get('video'):
        v = it['video']
        vst = f' style="aspect-ratio:{it["aspect"]}"' if it.get('aspect') else ''
        return (f'      <div class="cs-img has-img{ratio}"{vst}><video muted loop playsinline preload="none" '
                f'poster="{src(v)}-poster.jpg" aria-label="{esc(it.get("alt",""))}">'
                f'<source src="{src(v)}.mp4" type="video/mp4"></video></div>')
    if it.get('html'):
        # Live HTML inside the frame (Max 2026-10-17): type specimens, word lists —
        # brand elements rebuilt as real type instead of saved-out plates. Styled by
        # the page's `css:`; `bg:` paints the panel, `aspect:` sets the shape.
        st = ''.join(f'{k}:{v};' for k, v in (('background', it.get('bg')), ('color', it.get('ink')),
                                               ('aspect-ratio', it.get('aspect'))) if v)
        hc = (' ' + it['html_class']) if it.get('html_class') else ''
        return (f'      <div class="cs-img has-img cs-html{hc}{ratio}" style="{st}" role="img" '
                f'aria-label="{esc(it.get("alt", ""))}">{it["html"]}</div>')
    # `bg:` paints a color panel behind the art (logos, cutouts, icons); `pad:` insets
    # the art inside it (percent of the frame) and switches it to fit-not-crop.
    # `align: bottom` sits a cutout on the panel's bottom edge.
    sty = []
    if it.get('aspect'): sty.append(f'aspect-ratio:{it["aspect"]}')
    if it.get('bg'): sty.append(f'background:{it["bg"]}')
    if 'pad' in it:
        ratio += ' contain'
        sty.append(f'--pad:{it["pad"]}%')
    if it.get('align') == 'bottom': ratio += ' align-bottom'
    ast = f' style="{";".join(sty)}"' if sty else ''
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

    # FLUSH FAMILY (Max 2026-10-16, Figma node 62:9). No gutter between the
    # pieces — they touch. Each comes in a content-width and a full-bleed form.
    'flush-pair':            'cs-grid cs-flush cs-flush-pair',
    'flush-pair-bleed':      'cs-grid cs-flush cs-flush-pair cs-grid-bleed',
    'flush-wide-pair':       'cs-grid cs-flush cs-flush-stack is-wide-first',
    'flush-wide-pair-bleed': 'cs-grid cs-flush cs-flush-stack is-wide-first cs-grid-bleed',
    'flush-pair-wide':       'cs-grid cs-flush cs-flush-stack is-wide-last',
    'flush-pair-wide-bleed': 'cs-grid cs-flush cs-flush-stack is-wide-last cs-grid-bleed',
}

# Layouts that must be emitted OUTSIDE the .wrap so they run edge to edge.
BLEED = {'bleed', 'flush-pair-bleed', 'flush-wide-pair-bleed', 'flush-pair-wide-bleed'}

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
        # `width: 792` narrows one block and centers it in the column (Max 2026-10-17:
        # loud pieces sit smaller, with air round them). `space: 96` sets the gap above it.
        if b.get('width'):
            # `width: 90%` (Max 2026-11-01) narrows by a share of the row instead,
            # so it scales with the fluid full-width rows.
            w = str(b['width']); w = w if w.endswith('%') else f'{w}px'
            style = (style + ';' if style else '') + f'width:100%;max-width:{w};justify-self:center;margin-inline:auto'
        # `panel: '#hex'` (Max 2026-10-31): the row sits in a tinted panel with
        # generous inner padding, so cards and slides get room around them.
        # Back-to-back panels of the same block run read as one panel.
        if b.get('panel'):
            extra_cls += ' cs-panel'
            style = (style + ';' if style else '') + f'background:{b["panel"]}'
        if 'space' in b:
            style = (style + ';' if style else '') + (f'margin-top:clamp({min(b["space"], 40)}px,{b["space"] / 14.4:.2f}vw,{b["space"]}px)')
        # `air_above: 80` (Max 2026-11-01): extra white space above this row on
        # full-width pages, on top of the normal 28 row gap. Scales down on phones.
        if b.get('air_above'):
            n = b['air_above']
            extra_cls += ' air-above'
            style = (style + ';' if style else '') + f'--air:clamp({n // 2}px,{n / 14.4:.2f}vw,{n}px)'
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


# SECTION GROUNDS (Max 2026-10-16). `ground:` on a section takes
#   white | cream | dark | any hex such as "#1B2A3A"
# Leave it out and the section keeps alternating cream/white down the page.
# The alternation is worked out here rather than in CSS, so a section that
# names its own color simply sits out and the rest stay in step.
# _alt['n'] counts only the auto sections: the intro is 0 (cream), so the
# first auto media section is 1 (white) and the division after the intro holds.
_alt = {'n': 0, 'mode': 'white', 'unnamed': 0}

def _luma(hexcolor):
    """Rough perceived brightness, 0 (black) to 1 (white)."""
    h = hexcolor.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ground_of(s):
    """-> (class string, inline style string) for one section."""
    g = s.get('ground')
    if g == 'dark':
        return 'cs-dark', ''
    if g in ('white', 'cream'):
        return f'cs-light is-{g}', ''
    if isinstance(g, str) and g.startswith('#'):
        tone = 'is-on-dark' if _luma(g) < 0.5 else 'is-on-light'
        return f'cs-custom {tone}', f' style="--ground:{g}"'
    _alt['unnamed'] += 1
    _alt['n'] += 1
    # Default (Max 2026-10-04): every unnamed section sits on white, with the
    # intro alone in cream. `grounds: alternate` at the top of a content file
    # restores the cream/white alternation for that page instead.
    if _alt['mode'] == 'alternate':
        return 'cs-light is-' + ('white' if _alt['n'] % 2 else 'cream'), ''
    return 'cs-light is-white', ''


# SECTION LINK ADDRESSES (Max 2026-10-17). Every headed section gets an id
# made from its heading ("Brand in the World" -> #brand-in-the-world) so the
# homepage slideshow can link straight to it. Set `id:` on a section to pin
# the address, so renaming the heading doesn't break a link.
_ids = set()

def section_id(s):
    sid = s.get('id') or (re.sub(r'[^a-z0-9]+', '-', s['heading'].lower().replace('&', 'and')).strip('-')
                          if s.get('heading') else None)
    if not sid:
        return None
    base, n = sid, 2
    while sid in _ids:
        sid, n = f'{base}-{n}', n + 1
    _ids.add(sid)
    return sid


_rail = {'on': False}

def rail_section(s, slug, ground, gstyle, idattr):
    # `layout: rail` (Max 2026-11-07, Figma 110:592): the section label and
    # description sit in the left four columns and stick near the top while the
    # section scrolls; every piece of art runs in the right eight columns.
    # Splits and bleeds are ignored here: everything stays in the right column.
    sub = esc(s['subhead']) if s.get('subhead') else ''
    head = ''
    if s.get('heading'):
        # Max 2026-11-08 (Figma 111:2012): page name in column 1, label +
        # description from column 2. The name hides while the nav logo shows.
        head = (f'      <p class="rail-page">{esc(_rail.get("name", ""))}</p>\n'
                f'      <div class="rail-text">\n'
                f'      <h2 class="rail-label">{esc(s["heading"])}</h2>\n'
                + (f'      <p class="rail-sub">{sub}</p>\n' if sub else '')
                + '      </div>\n')
    blocks = list(s['blocks'])
    # a `head: split` piece was chosen as the section opener: it leads the column here
    if s.get('head') == 'split' and blocks:
        blocks.insert(0, blocks.pop(int(s.get('split_block', 0))))
    body = '\n'.join(block(b, slug) for b in blocks)
    if s.get('flush_bottom'):
        ground += ' cs-flush-bottom'
    return (f'<section class="{ground} cs-media"{idattr}{gstyle}>\n  <div class="wrap rail">\n'
            f'    <div class="rail-head">\n{head}    </div>\n'
            f'    <div class="rail-body">\n{body}\n    </div>\n  </div>\n</section>')

def section(s, slug):
    ground, gstyle = ground_of(s)
    sid = section_id(s)
    idattr = f' id="{sid}"' if sid else ''
    if _rail['on']:
        return rail_section(s, slug, ground, gstyle, idattr)
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
    blocks = list(s['blocks'])
    # `head: split` (Max 2026-11-01, Figma 93:31699 "Two-Column Header Row"):
    # the heading takes the left half and the section's first block sits in the
    # right half, both under the one rule. Only on `style: wide` pages.
    if head and s.get('head') == 'split' and blocks:
        # `split_block: N` lifts block N (0-based) into the right half instead,
        # so a wide opener can stay as the first full-width row underneath.
        first = blocks.pop(int(s.get('split_block', 0)))
        buf = ['    <div class="cs-head-split">\n' + head.replace('class="cs-head reveal"', 'class="cs-head"')
               + '\n' + block(first, slug) + '\n    </div>']
    for b in blocks:
        if b['layout'] in BLEED:
            if buf:
                parts.append('  <div class="wrap">\n' + '\n'.join(buf) + '\n  </div>')
                buf = []
            parts.append(block(b, slug))
        else:
            buf.append(block(b, slug))
    if buf:
        parts.append('  <div class="wrap">\n' + '\n'.join(buf) + '\n  </div>')
    # `flush_bottom: true` (Max 2026-10-28): drop the section's bottom padding so
    # a closing edge-to-edge block runs straight into the next section.
    if s.get('flush_bottom'):
        ground += ' cs-flush-bottom'
    return (f'<section class="{ground} cs-media"{idattr}{gstyle}>\n'
            + '\n'.join(parts) + '\n</section>')

def rail_intro(p):
    # Figma 110:592: kind label + page title in the left columns; statement,
    # then the meta blocks in two columns, in the right eight.
    i = p['intro']
    metas = [f'        <div class="rail-meta-block">\n          <p class="rail-label">{esc(m["label"])}</p>\n'
             f'          <p class="rail-body-text">{esc(m["body"])}</p>\n        </div>' for m in i['meta']]
    link = (f'        <p class="rail-body-text rail-link">{i["links_html"]}</p>\n' if i.get('links_html') else '')
    # links go under the last meta block, in its column (as in the Figma)
    col_a = metas[0] if metas else ''
    col_b = '\n'.join(metas[1:])
    meta = (f'      <div class="rail-meta">\n        <div class="rail-meta-col">\n{col_a}\n        </div>\n'
            f'        <div class="rail-meta-col">\n{col_b}\n{link}        </div>\n      </div>\n')
    return ('<!-- INTRO -->\n<section class="cs-light rail-intro" id="intro">\n  <div class="wrap rail">\n'
            f'    <div class="rail-head">\n      <p class="rail-label">{esc(p.get("_kind", "Case Study"))}</p>\n'
            f'      <h1 class="rail-title">{esc(i["eyebrow"])}</h1>\n    </div>\n'
            f'    <div class="rail-body">\n      <p class="rail-statement">{esc(i["statement"])}</p>\n{meta}'
            '    </div>\n  </div>\n</section>')

def intro(p):
    if _rail['on']:
        return rail_intro(p)
    i = p['intro']
    meta = '\n'.join(
        f'      <div class="cs-meta-block">\n'
        f'        <p class="cs-label">{esc(m["label"])}</p>\n'
        f'        <p class="cs-body">{esc(m["body"])}</p>\n'
        f'      </div>' for m in i['meta'])
    return ('<!-- INTRO -->\n<section class="cs-light is-cream" id="intro">\n  <div class="wrap cs-intro">\n'
            '    <div class="cs-intro-statement reveal">\n'
            f'      <p class="cs-label">{esc(i["eyebrow"])}</p>\n'
            f'      <h1 class="cs-statement">{esc(i["statement"])}</h1>\n'
            '    </div>\n    <div class="cs-intro-meta reveal">\n'
            f'{meta}\n' + (f'      <p class="cs-body cs-link">{i["links_html"]}</p>\n' if i.get('links_html') else '') +
            '    </div>\n  </div>\n</section>')

# NEXT UP (Max 2026-10-25): every case study / collection ends by pointing on to the
# next one in menu order (wrapping round). Items need `kind:` in site.yml.
# Footer Next arrow (Max 2026-11-07, Figma 110:2001): the Figma "down arrow" turned to
# point right, drawn in currentColor so it can take the hover color.
ARROW_R = ('<svg class="arrow-r" viewBox="0 0 29.061 13.7886" width="29.06" height="13.79" aria-hidden="true">'
           '<path d="M21.6363 13.2583L28.0003 6.8943L21.6363 0.5303" fill="none" stroke="currentColor" stroke-width="1.5"/>'
           '<rect y="6.1443" width="28" height="1.5" fill="currentColor"/></svg>')

def next_up(page, site):
    if page.get('nav') == 'standalone' or page.get('next') is False:
        return ''
    items = [n for n in site['nav'] if n.get('kind')]
    me = '/' + str(page.get('output', page.get('_slug'))) + '.html'
    hrefs = [n['href'] for n in items]
    if me not in hrefs and page.get('_extends'):
        me = '/' + str(page['_extends']) + '.html'   # test variants point on like their base page
    if me not in hrefs:
        return ''
    n = items[(hrefs.index(me) + 1) % len(items)]
    # Max 2026-11-07 (Figma 110:2001): Next sits in the footer row, not above it.
    return (f'  <a class="next-link" href="{n["href"]}"><span class="foot-k next-k">Next</span>'
            f'<span class="next-title">{esc(n["label"])}</span>{ARROW_R}</a>\n')

def build(slug):
    _alt['n'] = 0          # each page starts its own alternation
    _alt['unnamed'] = 0
    _ids.clear()
    page = yaml.safe_load((ROOT / 'content' / f'{slug}.yml').read_text())
    # `extends: other-slug` (Max 2026-10-31): a variant page that takes every
    # field of another content file and overrides only what it sets itself.
    # Used for the full-width test of Fandom, so content is never doubled.
    if page.get('extends'):
        base = yaml.safe_load((ROOT / 'content' / f"{page['extends']}.yml").read_text())
        base.update({k: v for k, v in page.items() if k != 'extends'})
        base['_extends'] = page['extends']
        page = base
    page['_slug'] = slug
    # `wide:` on a block (Max 2026-10-31) holds overrides used only on `style: wide`
    # pages — e.g. different `cols` — and `wide_aspect:` on an item likewise.
    # Normal pages ignore both, so one content file serves both layouts.
    if str(page.get('style', '')).lower() == 'wide':
        for sec in page['sections']:
            for b in sec['blocks']:
                if isinstance(b.get('wide'), dict):
                    b.update(b['wide'])
                for it in b.get('items', []) or []:
                    if isinstance(it, dict) and it.get('wide_aspect'):
                        it['aspect'] = it['wide_aspect']
    # `grounds_all: white` (Max 2026-10-31): every section on one ground, for tests.
    if page.get('grounds_all'):
        page['sections'] = [dict(s, ground=page['grounds_all']) for s in page['sections']]
    _alt['mode'] = str(page.get('grounds', 'white')).lower()   # white | alternate
    art = page.get('assets', slug)   # optional: borrow another page's asset folder
    site = yaml.safe_load((ROOT / 'content' / 'site.yml').read_text())
    _rail['on'] = str(page.get('layout', '')).lower() == 'rail'
    _rail['name'] = (page.get('intro') or {}).get('eyebrow', page.get('title', ''))
    if _rail['on']:
        # the label over the title: this page's kind in the menu (Case Study / Collection)
        base_href = '/' + str(page.get('_extends', slug)) + '.html'
        page['_kind'] = next((n['kind'] for n in site['nav'] if n.get('kind') and n['href'] == base_href), 'Case Study')
    nav = '\n'.join(f'    <a href="{n["href"]}">{n["label"]}</a>' for n in site['nav'])
    out = (ROOT / 'templates' / 'case-study.html').read_text()
    for k, v in [('TITLE', page['title']), ('DESCRIPTION', page['description']),
                 ('COVER', ASSETS.format(slug=art) + page['cover']), ('NAV', nav),
                 # The intro (description) always comes straight after the cover.
                 # `lead:` is one headless section placed directly after the intro.
                 ('INTRO', intro(page) + ('\n\n' + section(page['lead'], art) if page.get('lead') else '')),
                 ('SECTIONS', '\n\n'.join(section(s, art) for s in page['sections'])),
                 ('NEXT', ''), ('FOOTER', (ROOT / 'templates' / 'footer.html').read_text().replace('<!--NEXT-->\n', next_up(page, site)))]:
        out = out.replace('{{%s}}' % k, v)
    # `frames: off` at the top of a content file drops the hairline round every piece.
    if str(page.get('frames', 'on')).lower() in ('off', 'false', 'none'):
        out = out.replace('<body class="cs-page">', '<body class="cs-page no-frames">', 1)
    # `style: wide` (Max 2026-10-31, full-width test): image rows run nearly the
    # full window, with an even edge, flush splits, and growth capped at 1920px.
    if str(page.get('style', '')).lower() == 'wide':
        out = out.replace('<body class="cs-page', '<body class="cs-wide cs-page', 1)
        # `row_gap: N` (Max 2026-11-01): one spacing for the whole page — between
        # side-by-side pieces, between rows, and in the split header — so a page
        # set tighter (Client Brands, 14) lines up everywhere.
        if page.get('row_gap') is not None:
            out = out.replace('<body class="cs-wide', f'<body style="--row-gap:{int(page["row_gap"])}px" class="cs-wide', 1)
    # `theme: dark` (Max 2026-10-31): the whole page on the homepage/About dark
    # green — intro, sections (use with `grounds_all: dark`), next link, footer.
    # Dropping the cs-page class lets the footer and next link take the site's
    # default dark-page colors.
    if str(page.get('theme', '')).lower() == 'dark':
        import re as _re
        out = _re.sub(r'<body class="([^"]*)">', lambda m: '<body class="%s">' % ' '.join(
            c for c in m.group(1).split() if c != 'cs-page'), out, count=1)
        out = out.replace('<section class="cs-light is-cream" id="intro">', '<section class="cs-dark" id="intro">', 1)
    # `layout: rail` (Max 2026-11-07): body class + the Figma down arrow on the cover.
    if _rail['on']:
        out = out.replace('<body class="cs-wide', '<body class="cs-rail cs-wide', 1)
        out = out.replace('<script src="/js/footer-dock.js" defer></script>', '<script src="/js/footer-dock.js" defer></script>\n<script src="/js/rail.js" defer></script>', 1)
        out = out.replace('<svg viewBox="0 0 36 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 1L18 15 35 1"/></svg>',
                          '<svg viewBox="0 0 13 28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6.5 0V27M1.5 22L6.5 27 11.5 22"/></svg>', 1)
    # `nav: standalone` — logo stays but links nowhere, and the menu is removed.
    if page.get('nav') == 'standalone':
        import re
        out = re.sub(r'<a href="/" aria-label="Max Spector — home">(.*?)</a>',
                     r'<span class="nav-logo">\1</span>', out, count=1, flags=re.S)
        out = out.replace('<a class="dock-logo" data-dock="logo" href="/" aria-label="Max Spector — home">', '<span class="dock-logo" data-dock="logo">', 1).replace('</svg></a>\n    <a class="foot-link"', '</svg></span>\n    <a class="foot-link"', 1)
        out = re.sub(r'\s*<button class="menu-btn".*?</button>', '', out, count=1, flags=re.S)
        out = re.sub(r'<div class="overlay" id="overlay">.*?</div>\n', '', out, count=1, flags=re.S)
    # `cover_mobile:` — a portrait cover for tall screens (phones, portrait tablets).
    if page.get('cover_mobile'):
        url = ASSETS.format(slug=art) + page['cover_mobile']
        # `cover_mobile_fit: contain` shows the whole portrait art (no side crop) on
        # `cover_mobile_bg:`, which should match the art's own flat background.
        fit = (f';background-size:contain!important;background-repeat:no-repeat!important;background-position:center!important;background-color:{page.get("cover_mobile_bg", "transparent")}'
               if page.get('cover_mobile_fit') == 'contain' else '')
        out = out.replace('</head>', '<style>@media (max-aspect-ratio:4/5){.cs-cover-media.has-img'
                          f'{{background-image:url(\'{url}\')!important{fit}}}}}</style>\n</head>', 1)
    # `cover_mobile_fit: width` (Max 2026-11-08): the phone art is cropped by design
    # right at its edges, so the sides must never crop further. On tall screens the
    # cover takes the art's own shape, capped at one screen (then only top/bottom crop).
    if page.get('cover_mobile') and page.get('cover_mobile_fit') == 'width':
        from PIL import Image as _Im
        mw, mh = _Im.open(ROOT / 'assets' / art / page['cover_mobile']).size
        out = out.replace('</head>', '<style>@media (max-aspect-ratio:4/5){'
                          f'.cs-cover{{height:auto!important;aspect-ratio:{mw}/{mh};max-height:100svh}}'
                          f'.cs-rail .cs-cover{{max-height:calc(100svh - 2 * var(--wide-edge))}}}}</style>\n</head>', 1)
    # `css:` — extra styles for this page only (its brand fonts, panel type).
    if page.get('css'):
        out = out.replace('</head>', f'<style>\n{page["css"]}\n</style>\n</head>', 1)
    # `output:` names the published file (and so the URL) if it differs from the content file.
    dest = ROOT / f"{page.get('output', slug)}.html"
    dest.write_text(out)
    n_img = out.count('<img src="/assets/'); n_vid = out.count('<video')
    print(f'built {dest.name}  —  {len(page["sections"])} sections, {n_img} images, {n_vid} videos')
    # Every section on a finished case study should name its own `ground:`
    # (Max 2026-10-16). This just says how many are still falling back.
    if _alt['mode'] != 'alternate' and _alt['unnamed']:
        print(f"         {_alt['unnamed']} section(s) with no ground: — falling back to white")

def check_home_links():
    """The homepage is hand-built. Check every slideshow link that points into
    a case-study page (/page.html or /page.html#section) actually lands."""
    home = (ROOT / 'index.html').read_text()
    bad = []
    for href in re.findall(r'<a class="slide[^"]*" href="([^"]+)"', home):
        if href == '#' or not href.startswith('/'):
            continue
        page, _, anchor = href.lstrip('/').partition('#')
        f = ROOT / page
        if not f.exists():
            bad.append(f'{href}  (no page {page})')
        elif anchor and f'id="{anchor}"' not in f.read_text():
            bad.append(f'{href}  (no section #{anchor} on {page})')
    if bad:
        print('  !! slideshow links that go nowhere:')
        for b in bad:
            print('     ' + b)
    else:
        print('slideshow links: all land')


if __name__ == '__main__':
    for slug in (sys.argv[1:] or ['fandom-brand']):
        build(slug)
    check_home_links()
