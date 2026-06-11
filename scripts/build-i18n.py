#!/usr/bin/env python3
"""
Build multi-language SEO output for ImationGroup.

Reads templates/*.html (the source of truth) and i18n.js (translations),
and generates:
  - /<lang>/<file>.html  for each of the 7 supported languages
  - /<file>.html (root)  as language-detect redirect stubs
  - /sitemap.xml         with all URLs and hreflang alternates
  - /robots.txt          pointing to the sitemap

Run locally with:  python scripts/build-i18n.py
Dependency:  pip install json5
"""
import json
import re
from pathlib import Path
import json5

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / 'templates'
SITE = 'https://imationgroup.com'
DEFAULT = 'en'

# --- Load translations from i18n.js (extract TRANSLATIONS object literal) ---
i18n_src = (REPO / 'i18n.js').read_text(encoding='utf-8')
m = re.search(r'const\s+TRANSLATIONS\s*=\s*(\{.*?\n\});', i18n_src, re.DOTALL)
assert m, 'TRANSLATIONS object not found in i18n.js'
TRANSLATIONS = json5.loads(m.group(1))
LANGS = list(TRANSLATIONS.keys())  # ['en', 'es', 'gl', 'ca', 'pt', 'eu', 'et']

PAGES = [
    {'file': 'index.html',            'title_key': 'page_title',     'noindex': False},
    {'file': 'services.html',         'title_key': 'svc_page_title', 'noindex': False},
    {'file': 'projects.html',         'title_key': 'proj_page_title','noindex': False},
    {'file': 'terms.html',            'title_key': None,             'noindex': False},
    {'file': 'privacy.html',          'title_key': None,             'noindex': False},
    {'file': 'contact-success.html',  'title_key': 'cs_page_title',  'noindex': True},
]

OG_LOCALE = {'en':'en_US','es':'es_ES','gl':'gl_ES','ca':'ca_ES','pt':'pt_PT','eu':'eu_ES','et':'et_EE'}
FLAGS = {'en':'gb','es':'es','gl':'es-ga','ca':'es-ct','pt':'pt','eu':'es-pv','et':'ee'}


def esc(s):
    s = '' if s is None else str(s)
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def get_meta_desc(t, page_file):
    if page_file == 'index.html':
        parts = [t.get('hero_tagline'), t.get('hero_description')]
        return ' — '.join(p for p in parts if p)
    if page_file == 'services.html':       return t.get('svc_hero_desc', '')
    if page_file == 'projects.html':       return t.get('proj_hero_subtitle', '')
    if page_file == 'terms.html':          return (t.get('footer_terms', 'Terms')) + ' — ImationGroup'
    if page_file == 'privacy.html':        return (t.get('footer_privacy', 'Privacy')) + ' — ImationGroup'
    if page_file == 'contact-success.html': return t.get('cs_message', '')
    return ''


def get_title(t, page):
    if page['title_key'] and t.get(page['title_key']):
        return t[page['title_key']]
    if page['file'] == 'terms.html':   return f"{t.get('footer_terms', 'Terms')} | ImationGroup"
    if page['file'] == 'privacy.html': return f"{t.get('footer_privacy', 'Privacy')} | ImationGroup"
    return 'ImationGroup'


# Regex helpers
TITLE_RE = re.compile(r'<title([^>]*?)\sdata-i18n="([^"]+)"([^>]*)>([^<]*)</title>', re.DOTALL)
TAG_RE   = re.compile(r'<(\w+)([^>]*?)\sdata-i18n="([^"]+)"([^>]*)>([^<]*)</\1>', re.DOTALL)
PH_RE1   = re.compile(r'data-i18n-placeholder="([^"]+)"([^>]*?\s)placeholder="[^"]*"')
PH_RE2   = re.compile(r'placeholder="[^"]*"(\s+[^>]*?)data-i18n-placeholder="([^"]+)"')


def apply_i18n(html, t):
    def sub_title(mm):
        before, key, after, _old = mm.groups()
        tx = t.get(key)
        if not tx: return mm.group(0)
        return f'<title{before} data-i18n="{key}"{after}>{esc(tx)}</title>'
    html = TITLE_RE.sub(sub_title, html)

    def sub_tag(mm):
        tag, a1, key, a2, _old = mm.groups()
        tx = t.get(key)
        if not tx: return mm.group(0)
        return f'<{tag}{a1} data-i18n="{key}"{a2}>{esc(tx)}</{tag}>'
    html = TAG_RE.sub(sub_tag, html)

    def sub_ph1(mm):
        key, mid = mm.groups()
        tx = t.get(key)
        if not tx: return mm.group(0)
        return f'data-i18n-placeholder="{key}"{mid}placeholder="{esc(tx)}"'
    html = PH_RE1.sub(sub_ph1, html)

    def sub_ph2(mm):
        mid, key = mm.groups()
        tx = t.get(key)
        if not tx: return mm.group(0)
        return f'placeholder="{esc(tx)}"{mid}data-i18n-placeholder="{key}"'
    html = PH_RE2.sub(sub_ph2, html)
    return html


PAGE_NAMES = ['index', 'services', 'projects', 'terms', 'privacy', 'contact-success']


def rewrite_links(html, lang):
    """href="services.html" → href="/<lang>/services.html" (preserves anchors)."""
    for p in PAGE_NAMES:
        html = re.sub(rf'href="{p}\.html', f'href="/{lang}/{p}.html', html)
    html = html.replace('src="i18n.js"', 'src="/i18n.js"')
    return html


def patch_lang_switcher(html, lang):
    """Set the language switcher button's flag and label to match this page's language at load time."""
    html = re.sub(
        r'(id="currentLangFlag"[^>]*\ssrc=")[^"]*"',
        rf'\1https://flagicons.lipis.dev/flags/4x3/{FLAGS[lang]}.svg"',
        html,
    )
    html = re.sub(
        r'(id="currentLangLabel"[^>]*>)[^<]*(</[^>]+>)',
        rf'\1{lang.upper()}\2',
        html,
    )
    return html


def strip_meta(html):
    """Remove existing og/twitter/description/keywords/canonical/hreflang so we can rebuild cleanly."""
    html = re.sub(r'\s*<meta\s+property="og:[^"]+"\s+content="[^"]*"\s*/?>', '', html)
    html = re.sub(r'\s*<meta\s+name="twitter:[^"]+"\s+content="[^"]*"\s*/?>', '', html)
    html = re.sub(r'\s*<meta\s+name="description"\s+content="[^"]*"\s*/?>', '', html)
    html = re.sub(r'\s*<meta\s+name="keywords"\s+content="[^"]*"\s*/?>', '', html)
    html = re.sub(r'\s*<meta\s+name="robots"\s+content="[^"]*"\s*/?>', '', html)
    html = re.sub(r'\s*<link\s+rel="canonical"[^>]*/?>', '', html)
    html = re.sub(r'\s*<link\s+rel="alternate"\s+hreflang="[^"]+"[^>]*/?>', '', html)
    html = re.sub(r'\s*<script\s+type="application/ld\+json"[^>]*>[\s\S]*?</script>', '', html)
    return html


def inject_seo(html, lang, page, t):
    title = get_title(t, page)
    desc = get_meta_desc(t, page['file'])
    url = f"{SITE}/{lang}/{page['file']}"
    hreflang_lines = '\n'.join(
        f'  <link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{page["file"]}" />'
        for l in LANGS
    )
    x_default = f'  <link rel="alternate" hreflang="x-default" href="{SITE}/{DEFAULT}/{page["file"]}" />'
    robots_content = 'noindex, follow' if page['noindex'] else 'index, follow'

    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "ImationGroup",
        "url": SITE,
        "logo": f"{SITE}/og-image.svg",
        "sameAs": []
    }, ensure_ascii=False)

    seo = f'''
  <link rel="canonical" href="{url}" />
{hreflang_lines}
{x_default}
  <meta name="robots" content="{robots_content}" />
  <meta name="description" content="{esc(desc)}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="ImationGroup" />
  <meta property="og:locale" content="{OG_LOCALE[lang]}" />
  <meta property="og:image" content="{SITE}/og-image.svg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{SITE}/og-image.svg" />
  <script type="application/ld+json">{json_ld}</script>
'''
    # Set <html lang="..."> attribute
    html = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang}"', html, count=1, flags=re.IGNORECASE)
    # Inject SEO block before </head>
    html = re.sub(r'</head>', seo + '</head>', html, count=1, flags=re.IGNORECASE)
    return html


def build_lang_page(lang, page):
    t = TRANSLATIONS[lang]
    src = TEMPLATES / page['file']
    html = src.read_text(encoding='utf-8')
    html = strip_meta(html)
    html = apply_i18n(html, t)
    html = patch_lang_switcher(html, lang)
    html = rewrite_links(html, lang)
    html = inject_seo(html, lang, page, t)
    out_dir = REPO / lang
    out_dir.mkdir(exist_ok=True)
    (out_dir / page['file']).write_text(html, encoding='utf-8')


def generate_root_stub(page):
    """Minimal HTML at root that detects user language and redirects to /<lang>/<file>.
    Includes hreflang + canonical (pointing to /en/<file>) so crawlers cluster all variants."""
    t = TRANSLATIONS[DEFAULT]
    title = get_title(t, page)
    desc = get_meta_desc(t, page['file'])
    canonical_url = f"{SITE}/{DEFAULT}/{page['file']}"
    hreflang_lines = '\n'.join(
        f'  <link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{page["file"]}" />'
        for l in LANGS
    )
    x_default = f'  <link rel="alternate" hreflang="x-default" href="{SITE}/{DEFAULT}/{page["file"]}" />'
    langs_json = json.dumps(LANGS)

    stub = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{canonical_url}" />
{hreflang_lines}
{x_default}
<meta name="robots" content="index, follow" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{canonical_url}" />
<meta property="og:type" content="website" />
<meta property="og:image" content="{SITE}/og-image.svg" />
<script>
(function(){{
  var L={langs_json};
  var s=null; try{{s=localStorage.getItem('ig_lang');}}catch(e){{}}
  var lang=(s&&L.indexOf(s)>-1)?s:null;
  if(!lang){{
    var nl=navigator.languages||[navigator.language||'en'];
    for(var i=0;i<nl.length&&!lang;i++){{var c=(nl[i]||'').toLowerCase().split('-')[0];if(L.indexOf(c)>-1)lang=c;}}
  }}
  if(!lang)lang='{DEFAULT}';
  location.replace('/'+lang+'/{page["file"]}');
}})();
</script>
<meta http-equiv="refresh" content="0; url=/{DEFAULT}/{page["file"]}" />
</head>
<body>
<p>Redirecting to <a href="{canonical_url}">{canonical_url}</a>…</p>
</body>
</html>
'''
    (REPO / page['file']).write_text(stub, encoding='utf-8')


def generate_sitemap():
    from datetime import date
    today = date.today().isoformat()
    items = []
    for lang in LANGS:
        for page in PAGES:
            if page['noindex']:
                continue
            url = f"{SITE}/{lang}/{page['file']}"
            alts = '\n'.join(
                f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{page["file"]}" />'
                for l in LANGS
            )
            xd = f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{DEFAULT}/{page["file"]}" />'
            priority = '1.0' if page['file'] == 'index.html' else '0.8'
            items.append(f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
{alts}
{xd}
  </url>''')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(items)}
</urlset>
'''
    (REPO / 'sitemap.xml').write_text(xml, encoding='utf-8')


def generate_robots():
    txt = f'''User-agent: *
Allow: /
Disallow: /backend/
Disallow: /scripts/
Disallow: /templates/
Disallow: /.github/
Disallow: /contact-success.html

Sitemap: {SITE}/sitemap.xml
'''
    (REPO / 'robots.txt').write_text(txt, encoding='utf-8')


def main():
    print('Building i18n + SEO output...')
    for lang in LANGS:
        for page in PAGES:
            build_lang_page(lang, page)
        print(f'  [ok] {lang}/  ({len(PAGES)} pages)')
    for page in PAGES:
        generate_root_stub(page)
    print('  [ok] root redirect stubs')
    generate_sitemap()
    print('  [ok] sitemap.xml')
    generate_robots()
    print('  [ok] robots.txt')
    print('Done.')


if __name__ == '__main__':
    main()
