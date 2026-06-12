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

try:
    import minify_html
    def minify(html):
        return minify_html.minify(
            html,
            minify_js=True, minify_css=True,
            remove_processing_instructions=True,
            keep_closing_tags=True,        # preserve </body></html> for smoke-test regex
            keep_html_and_head_opening_tags=True,  # preserve <html lang> for SEO
        )
except ImportError:
    print('  (minify-html not installed; output not minified — `pip install minify-html`)')
    def minify(html):
        return html

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

# Public profiles and contact for JSON-LD
LINKEDIN_URL = 'https://www.linkedin.com/company/112659095'
CONTACT_EMAIL = 'info@imationgroup.com'
THEME_COLOR = '#0066CC'
BRAND = 'ImationGroup'


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


def url_path(lang, page_file):
    """Public path for a page: clean, no .html. index.html -> /<lang>/, others -> /<lang>/<basename>."""
    if page_file == 'index.html':
        return f"/{lang}/"
    return f"/{lang}/{page_file[:-5]}"


def page_canonical(lang, page_file):
    return SITE + url_path(lang, page_file)


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
    """href="services.html" → clean URL href="/<lang>/services" (preserves anchors via the trailing context)."""
    for p in PAGE_NAMES:
        target = f'/{lang}/' if p == 'index' else f'/{lang}/{p}'
        html = re.sub(rf'href="{p}\.html"', f'href="{target}"', html)
        html = re.sub(rf'href="{p}\.html#', f'href="{target}#', html)
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
    """Remove existing meta/links we'll regenerate so we can rebuild cleanly."""
    pats = [
        r'\s*<meta\s+property="og:[^"]+"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="twitter:[^"]+"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="description"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="keywords"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="robots"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="theme-color"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="application-name"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="apple-mobile-web-app-[a-z-]+"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="mobile-web-app-capable"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="msapplication-[A-Za-z-]+"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="format-detection"\s+content="[^"]*"\s*/?>',
        r'\s*<meta\s+name="color-scheme"\s+content="[^"]*"\s*/?>',
        r'\s*<link\s+rel="canonical"[^>]*/?>',
        r'\s*<link\s+rel="alternate"\s+hreflang="[^"]+"[^>]*/?>',
        r'\s*<link\s+rel="icon"[^>]*/?>',
        r'\s*<link\s+rel="apple-touch-icon"[^>]*/?>',
        r'\s*<link\s+rel="manifest"[^>]*/?>',
        r'\s*<link\s+rel="me"[^>]*/?>',
        r'\s*<script\s+type="application/ld\+json"[^>]*>[\s\S]*?</script>',
    ]
    for p in pats:
        html = re.sub(p, '', html)
    return html


def build_jsonld(lang, page, t):
    """Build @graph JSON-LD: WebSite + Organization + WebPage + (BreadcrumbList) + (ItemList)."""
    site_id = f"{SITE}/#website"
    org_id = f"{SITE}/#organization"
    page_url = page_canonical(lang, page['file'])
    page_id = f"{page_url}#webpage"
    page_title = get_title(t, page)
    page_desc = get_meta_desc(t, page['file'])

    website = {
        "@type": "WebSite", "@id": site_id, "url": f"{SITE}/", "name": BRAND,
        "description": t.get('hero_description') or t.get('hero_tagline') or '',
        "inLanguage": lang, "publisher": {"@id": org_id},
    }
    organization = {
        "@type": "Organization", "@id": org_id, "name": BRAND, "url": f"{SITE}/",
        "description": t.get('about_who_p1') or t.get('hero_description') or '',
        "logo": {"@type": "ImageObject", "url": f"{SITE}/og-image.png", "width": 1200, "height": 630},
        "image": f"{SITE}/og-image.png",
        "email": CONTACT_EMAIL, "sameAs": [LINKEDIN_URL],
        "contactPoint": [{
            "@type": "ContactPoint", "email": CONTACT_EMAIL,
            "contactType": "customer service", "availableLanguage": LANGS,
        }],
    }
    webpage = {
        "@type": "WebPage", "@id": page_id, "url": page_url,
        "name": page_title, "description": page_desc,
        "isPartOf": {"@id": site_id}, "about": {"@id": org_id},
        "inLanguage": lang,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/og-image.png"},
    }
    graph = [website, organization, webpage]

    if page['file'] != 'index.html':
        crumb = {
            'services.html': t.get('nav_services', 'Services'),
            'projects.html': t.get('nav_projects', 'Projects'),
            'terms.html':    t.get('footer_terms', 'Terms of Service'),
            'privacy.html':  t.get('footer_privacy', 'Privacy Policy'),
            'contact-success.html': t.get('cs_label', 'Message received'),
        }.get(page['file'], page['file'])
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t.get('nav_home', 'Home'),
                 "item": page_canonical(lang, 'index.html')},
                {"@type": "ListItem", "position": 2, "name": crumb, "item": page_url},
            ],
        })

    if page['file'] == 'services.html':
        svc_keys = [
            ('svc_web_title', 'svc_web_subtitle'), ('svc_host_title', 'svc_host_subtitle'),
            ('svc_app_title', 'svc_app_subtitle'), ('svc_mkt_title', 'svc_mkt_subtitle'),
            ('svc_de_title',  'svc_de_subtitle'),  ('svc_ds_title',  'svc_ds_subtitle'),
        ]
        items = []
        for i, (k_t, k_d) in enumerate(svc_keys, start=1):
            if not t.get(k_t): continue
            items.append({
                "@type": "ListItem", "position": i,
                "item": {"@type": "Service", "name": t[k_t],
                         "description": t.get(k_d, ''),
                         "provider": {"@id": org_id}, "areaServed": "Worldwide"},
            })
        if items:
            graph.append({"@type": "ItemList",
                          "name": t.get('svc_hero_title') or t.get('nav_services', 'Services'),
                          "itemListElement": items})

    if page['file'] == 'projects.html':
        projs = [
            ('AutoLinked',   'https://autolinked.imationgroup.com',   t.get('proj_al_desc', '')),
            ('AutoWhatsapp', 'https://autowhatsapp.imationgroup.com', t.get('proj_aw_desc', '')),
            ('AutoX',        'https://autox.imationgroup.com',        t.get('proj_ax_desc', '')),
        ]
        items = []
        for i, (name, url, dsc) in enumerate(projs, start=1):
            items.append({
                "@type": "ListItem", "position": i,
                "item": {"@type": "SoftwareApplication", "name": name, "url": url,
                         "description": dsc,
                         "applicationCategory": "BusinessApplication",
                         "operatingSystem": "Web",
                         "publisher": {"@id": org_id},
                         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            })
        graph.append({"@type": "ItemList",
                      "name": t.get('proj_hero_title', 'Projects'),
                      "itemListElement": items})

    return {"@context": "https://schema.org", "@graph": graph}


def inject_seo(html, lang, page, t):
    title = get_title(t, page)
    desc = get_meta_desc(t, page['file'])
    url = page_canonical(lang, page['file'])
    hreflang_lines = '\n'.join(
        f'  <link rel="alternate" hreflang="{l}" href="{page_canonical(l, page["file"])}" />'
        for l in LANGS
    )
    x_default = f'  <link rel="alternate" hreflang="x-default" href="{page_canonical(DEFAULT, page["file"])}" />'
    robots_content = 'noindex, follow' if page['noindex'] else 'index, follow'
    alt_text = f"{BRAND} — {t.get('hero_tagline', 'Data Engineering and Software Solutions')}"

    json_ld = json.dumps(build_jsonld(lang, page, t), ensure_ascii=False, separators=(',', ':'))

    seo = f'''
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/favicon.svg" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="{THEME_COLOR}" />
  <meta name="color-scheme" content="light" />
  <meta name="application-name" content="{BRAND}" />
  <meta name="apple-mobile-web-app-title" content="{BRAND}" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="msapplication-TileColor" content="{THEME_COLOR}" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="robots" content="{robots_content}" />
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
{hreflang_lines}
{x_default}
  <link rel="me" href="{LINKEDIN_URL}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{BRAND}" />
  <meta property="og:locale" content="{OG_LOCALE[lang]}" />
  <meta property="og:image" content="{SITE}/og-image.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{esc(alt_text)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{SITE}/og-image.png" />
  <meta name="twitter:image:alt" content="{esc(BRAND)}" />
  <script type="application/ld+json">{json_ld}</script>
'''
    html = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang}"', html, count=1, flags=re.IGNORECASE)
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
    html = minify(html)
    out_dir = REPO / lang
    out_dir.mkdir(exist_ok=True)
    (out_dir / page['file']).write_text(html, encoding='utf-8')


def generate_root_stub(page):
    """Minimal HTML at root that detects user language and redirects to /<lang>/<file>.
    Includes hreflang + canonical (pointing to /en/<file>) so crawlers cluster all variants."""
    t = TRANSLATIONS[DEFAULT]
    title = get_title(t, page)
    desc = get_meta_desc(t, page['file'])
    canonical_url = page_canonical(DEFAULT, page['file'])
    hreflang_lines = '\n'.join(
        f'  <link rel="alternate" hreflang="{l}" href="{page_canonical(l, page["file"])}" />'
        for l in LANGS
    )
    x_default = f'  <link rel="alternate" hreflang="x-default" href="{page_canonical(DEFAULT, page["file"])}" />'
    langs_json = json.dumps(LANGS)
    redirect_path = url_path('PLACEHOLDER', page['file']).replace('/PLACEHOLDER/', '/')  # body used as template
    # Build language-specific paths (relative) for the redirect JS
    page_basename = '' if page['file'] == 'index.html' else page['file'][:-5]

    stub = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/favicon.svg" />
<link rel="manifest" href="/site.webmanifest" />
<meta name="theme-color" content="{THEME_COLOR}" />
<meta name="application-name" content="{BRAND}" />
<meta name="apple-mobile-web-app-title" content="{BRAND}" />
<link rel="canonical" href="{canonical_url}" />
{hreflang_lines}
{x_default}
<meta name="robots" content="index, follow" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{canonical_url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{BRAND}" />
<meta property="og:image" content="{SITE}/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
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
  location.replace('/'+lang+'/{page_basename}');
}})();
</script>
<meta http-equiv="refresh" content="0; url=/{DEFAULT}/{page_basename}" />
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
            url = page_canonical(lang, page['file'])
            alts = '\n'.join(
                f'    <xhtml:link rel="alternate" hreflang="{l}" href="{page_canonical(l, page["file"])}" />'
                for l in LANGS
            )
            xd = f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_canonical(DEFAULT, page["file"])}" />'
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


def generate_404():
    """Multilingual 404 page. Server-side: nginx maps error_page 404 /404.html.
    Client-side: detects browser language and shows the right block; provides
    links back to home in all 7 languages so even bots see them."""
    # Per-language strings, with English fallback for any missing key.
    msgs = []
    for lang in LANGS:
        t = TRANSLATIONS[lang]
        msgs.append({
            'lang': lang,
            'title': t.get('e404_title', 'Page not found'),
            'desc':  t.get('e404_desc',  'The page you were looking for does not exist or has moved.'),
            'home':  t.get('nav_home',   'Back to home'),
        })
    blocks = '\n'.join(
        f'<div class="msg" data-lang="{m["lang"]}" lang="{m["lang"]}" hidden>'
        f'<h1>{esc(m["title"])}</h1><p>{esc(m["desc"])}</p>'
        f'<p><a href="/{m["lang"]}/">{esc(m["home"])}</a></p></div>'
        for m in msgs
    )
    langs_json = json.dumps(LANGS)
    html = f'''<!DOCTYPE html>
<html lang="{DEFAULT}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>404 — {BRAND}</title>
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>
body{{font-family:system-ui,sans-serif;max-width:560px;margin:8vh auto;padding:0 1.5rem;color:#1a1a2e;text-align:center;line-height:1.6}}
h1{{font-size:2rem;margin-bottom:.5rem;color:#0066CC}}
p{{margin:.5rem 0}}
a{{color:#0066CC;text-decoration:none;border-bottom:1px solid #0066CC}}
a:hover{{color:#00A5A8;border-color:#00A5A8}}
.msg{{margin-bottom:2rem}}
.alts{{margin-top:2rem;font-size:.9rem;color:#666}}
.alts a{{margin:0 .4rem}}
</style>
</head>
<body>
{blocks}
<noscript>
<div class="msg" lang="{DEFAULT}">
<h1>Page not found</h1><p>The page you were looking for does not exist or has moved.</p>
<p><a href="/{DEFAULT}/">Back to home</a></p>
</div>
</noscript>
<div class="alts">
{' '.join(f'<a href="/{l}/" hreflang="{l}">{l.upper()}</a>' for l in LANGS)}
</div>
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
  var el=document.querySelector('.msg[data-lang="'+lang+'"]');
  if(el)el.removeAttribute('hidden');
  document.documentElement.lang=lang;
}})();
</script>
</body>
</html>
'''
    (REPO / '404.html').write_text(minify(html), encoding='utf-8')


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
    generate_404()
    print('  [ok] 404.html')
    generate_sitemap()
    print('  [ok] sitemap.xml')
    generate_robots()
    print('  [ok] robots.txt')
    print('Done.')


if __name__ == '__main__':
    main()
