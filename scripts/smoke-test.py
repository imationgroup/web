#!/usr/bin/env python3
"""Smoke test for imationgroup.com — runs after each deploy.

Verifies:
  - sitemap.xml + robots.txt + favicon.svg + site.webmanifest serve
  - every URL in sitemap returns 200
  - every language home, services, projects has correct canonical, hreflang,
    JSON-LD and og:url
  - root redirect stubs still work
  - no broken markdown-style hrefs leaked into production (regression guard
    for the Google Fonts bug fixed on 2026-06-12)
  - contact API endpoint responds (405 to HEAD = alive)

Usage:
  python3 scripts/smoke-test.py              # tests https://imationgroup.com
  python3 scripts/smoke-test.py http://...   # tests a different origin
  BASE_URL=... python3 scripts/smoke-test.py # same, via env var

Exit code 0 if all checks pass, 1 otherwise. Designed to be lightweight
(stdlib only, ~30 HTTP requests total) so it fits in a GitHub Actions step.
"""
from __future__ import annotations
import json
import os
import re
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from xml.etree import ElementTree as ET
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('BASE_URL', 'https://imationgroup.com')).rstrip('/')
API = os.environ.get('API_URL', 'https://api.imationgroup.com')
LANGS = ['en', 'es', 'gl', 'ca', 'pt', 'eu', 'et']
INDEXED_PAGES = ['', 'services', 'projects']  # '' = home
ROOT_STUBS = ['services.html', 'projects.html', 'terms.html', 'privacy.html']

fails: list[str] = []
passes = 0


def ok(msg: str) -> None:
    global passes
    passes += 1
    print(f"  [ok]   {msg}")


def fail(msg: str) -> None:
    fails.append(msg)
    print(f"  [FAIL] {msg}")


def fetch(url: str, method: str = 'GET', timeout: int = 15) -> tuple[int, str, dict]:
    req = urllib.request.Request(url, method=method, headers={'User-Agent': 'imationgroup-smoke/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode('utf-8', errors='replace') if method == 'GET' else ''
            return r.status, body, dict(r.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace') if method == 'GET' else ''
        return e.code, body, dict(e.headers or {})
    except Exception as e:
        return 0, str(e), {}


def status_only(url: str) -> int:
    return fetch(url, method='HEAD')[0]


# ────────────────────────────── checks ──────────────────────────────────────

def check_basics():
    print('\n[1/6] Basic assets')
    for path, accepted_cts in [
        ('/favicon.svg',       ['image/svg']),
        ('/site.webmanifest',  ['manifest+json']),
        ('/robots.txt',        ['text']),
        ('/og-image.png',      ['image/png']),
        ('/og-image.svg',      ['image/svg']),  # kept as fallback
    ]:
        code, body, headers = fetch(BASE + path)
        ct = headers.get('Content-Type', '').lower()
        if code != 200:
            fail(f"{path} -> {code} (want 200)")
            continue
        if not any(c in ct for c in accepted_cts):
            fail(f"{path} content-type '{ct}' not in accepted {accepted_cts}")
            continue
        ok(f"{path} 200 ({ct.split(';')[0]})")

    # robots.txt must reference the sitemap
    code, body, _ = fetch(BASE + '/robots.txt')
    if 'Sitemap:' in body and 'sitemap.xml' in body:
        ok('robots.txt references sitemap')
    else:
        fail('robots.txt missing Sitemap directive')

    # site.webmanifest must parse and have name
    code, body, _ = fetch(BASE + '/site.webmanifest')
    try:
        m = json.loads(body)
        if m.get('name'):
            ok(f"webmanifest valid (name='{m['name']}')")
        else:
            fail("webmanifest missing 'name'")
    except json.JSONDecodeError as e:
        fail(f"webmanifest invalid JSON: {e}")


def check_sitemap() -> list[str]:
    print('\n[2/6] Sitemap')
    code, body, headers = fetch(BASE + '/sitemap.xml')
    if code != 200:
        fail(f"/sitemap.xml -> {code}")
        return []
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        fail(f"sitemap.xml invalid XML: {e}")
        return []
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = [e.text for e in root.findall('sm:url/sm:loc', ns) if e.text]
    if not locs:
        fail('sitemap has zero <loc>')
        return []
    ok(f"sitemap parses, {len(locs)} URLs")

    # Spot-check expected URLs are present (clean URLs, no .html)
    expected = {f"{BASE}/{l}/" for l in LANGS} | {f"{BASE}/{l}/services" for l in LANGS}
    missing = expected - set(locs)
    if missing:
        fail(f"sitemap missing {len(missing)} expected URLs, e.g. {sorted(missing)[:3]}")
    else:
        ok(f"sitemap contains all home + services URLs for {len(LANGS)} languages")

    # Any URL with .html in path is a regression
    dirty = [u for u in locs if u.endswith('.html')]
    if dirty:
        fail(f"sitemap has {len(dirty)} URLs with .html suffix (regression): {dirty[:2]}")
    else:
        ok('sitemap uses clean URLs (no .html)')
    return locs


def check_all_urls_200(urls: list[str]):
    print(f'\n[3/6] Reachability of {len(urls)} sitemap URLs (parallel HEADs)')
    bad: list[tuple[str, int]] = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for url, code in zip(urls, ex.map(status_only, urls)):
            if code != 200:
                bad.append((url, code))
    if bad:
        for u, c in bad[:5]:
            fail(f"{u} -> {c}")
        if len(bad) > 5:
            fail(f"(+{len(bad) - 5} more)")
    else:
        ok(f"all {len(urls)} URLs return 200")


class HeadExtractor(HTMLParser):
    """Pulls structured info out of <link>, <meta>, <script type=ld+json> tags.
    Robust to attribute reordering and quote-stripping done by HTML minifiers."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = None
        self.og_url = None
        self.hreflang: dict[str, str] = {}
        self.ldjson_blocks: list[str] = []
        self._in_ldjson = False
        self._buf = []
    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or '') for k, v in attrs}
        if tag == 'link':
            rel = a.get('rel', '').lower()
            if rel == 'canonical':
                self.canonical = a.get('href')
            elif rel == 'alternate':
                hl = a.get('hreflang')
                if hl:
                    self.hreflang[hl.lower()] = a.get('href', '')
        elif tag == 'meta':
            if a.get('property', '').lower() == 'og:url':
                self.og_url = a.get('content')
        elif tag == 'script':
            if a.get('type', '').lower() == 'application/ld+json':
                self._in_ldjson = True; self._buf = []
    def handle_endtag(self, tag):
        if tag == 'script' and self._in_ldjson:
            self.ldjson_blocks.append(''.join(self._buf)); self._in_ldjson = False
    def handle_data(self, data):
        if self._in_ldjson:
            self._buf.append(data)


def check_seo_per_lang():
    print(f'\n[4/7] Per-language SEO (canonical, hreflang, og:url, JSON-LD)')
    markdown_href_re = re.compile(r'href=["\'\s]*\[[^\]]+\]\(https?://')

    for lang in LANGS:
        bad = []
        for page in INDEXED_PAGES:
            url = f"{BASE}/{lang}/{page}" if page else f"{BASE}/{lang}/"
            code, body, _ = fetch(url)
            if code != 200:
                bad.append(f"{url} -> {code}"); continue

            p = HeadExtractor()
            p.feed(body)

            if p.canonical != url:
                bad.append(f"{url} canonical='{p.canonical}'"); continue
            if p.og_url != url:
                bad.append(f"{url} og:url='{p.og_url}'"); continue
            missing = set(LANGS) - set(p.hreflang)
            if missing:
                bad.append(f"{url} missing hreflang {sorted(missing)}"); continue
            if 'x-default' not in p.hreflang:
                bad.append(f"{url} missing x-default"); continue
            if not p.ldjson_blocks:
                bad.append(f"{url} no JSON-LD"); continue
            try:
                data = json.loads(p.ldjson_blocks[0])
                graph = data.get('@graph', [data])
                types = {item.get('@type') for item in graph}
                if 'Organization' not in types or 'WebPage' not in types:
                    bad.append(f"{url} JSON-LD types={types}"); continue
            except json.JSONDecodeError as e:
                bad.append(f"{url} JSON-LD invalid: {e}"); continue

            if markdown_href_re.search(body):
                bad.append(f"{url} has markdown-wrapped href!"); continue

        if bad:
            for msg in bad: fail(msg)
        else:
            ok(f"/{lang}/ ({len(INDEXED_PAGES)} pages) - canonical, hreflang, JSON-LD all good")


def check_404_page():
    print(f'\n[5/8] 404 page')
    # Hit a URL that should 404 (no template ever named "this-page-does-not-exist")
    bogus = f"{BASE}/smoke-test-this-page-does-not-exist"
    code, body, _ = fetch(bogus)
    if code != 404:
        fail(f"GET {bogus} -> {code} (want 404)"); return
    # Must mention all 7 languages and link to /<lang>/
    missing = [l for l in LANGS if f'/{l}/' not in body]
    if missing:
        fail(f"404 page missing links for {missing}"); return
    ok(f"404 returns 404 status + links to all {len(LANGS)} languages")


def check_redirects_and_stubs():
    print(f'\n[6/8] .html -> clean URL redirects + root stubs')

    def head_no_follow(url: str) -> tuple[int, str]:
        opener = urllib.request.build_opener(NoRedirect)
        req = urllib.request.Request(url, method='HEAD',
                                     headers={'User-Agent': 'imationgroup-smoke/1.0'})
        try:
            with opener.open(req, timeout=10) as r:
                return r.status, r.headers.get('Location', '')
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get('Location', '') if e.headers else ''

    # /<lang>/index.html -> /<lang>/  (301)
    for lang in ['en', 'es']:
        code, loc = head_no_follow(f"{BASE}/{lang}/index.html")
        want = f"{BASE}/{lang}/"
        if code == 301 and loc == want:
            ok(f"/{lang}/index.html -> 301 {loc}")
        else:
            fail(f"/{lang}/index.html -> {code} {loc} (want 301 {want})")

    # /<lang>/services.html -> /<lang>/services  (301)
    for lang in ['en', 'es']:
        code, loc = head_no_follow(f"{BASE}/{lang}/services.html")
        want = f"{BASE}/{lang}/services"
        if code == 301 and loc == want:
            ok(f"/{lang}/services.html -> 301 {loc}")
        else:
            fail(f"/{lang}/services.html -> {code} {loc} (want 301 {want})")

    # Root stubs: /services.html -> 301 /services -> 200 (serves stub via try_files)
    for stub_html, clean in [('services.html', 'services'), ('projects.html', 'projects'),
                             ('terms.html', 'terms'), ('privacy.html', 'privacy')]:
        code, loc = head_no_follow(f"{BASE}/{stub_html}")
        want = f"{BASE}/{clean}"
        if code == 301 and loc == want:
            ok(f"/{stub_html} -> 301 /{clean}")
        else:
            fail(f"/{stub_html} -> {code} {loc} (want 301 {want})")

    # Clean root paths return 200 (stub HTML with JS redirect)
    for path in ['services', 'projects']:
        code = status_only(f"{BASE}/{path}")
        if code != 200:
            fail(f"/{path} -> {code}")
        else:
            ok(f"/{path} 200 (root stub via try_files)")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        return None  # don't follow


def check_security_headers():
    print(f'\n[7/8] Security headers')
    _, _, headers = fetch(f"{BASE}/en/services")
    # Header name comparison is case-insensitive in HTTP
    h = {k.lower(): v for k, v in headers.items()}
    required = {
        'strict-transport-security': 'max-age=',
        'x-content-type-options':    'nosniff',
        'x-frame-options':           'SAMEORIGIN',
        'referrer-policy':           'strict-origin',
        'permissions-policy':        'interest-cohort',
    }
    for name, must_contain in required.items():
        v = h.get(name, '')
        if must_contain.lower() in v.lower():
            ok(f"{name}: {v}")
        else:
            fail(f"{name} missing or wrong (got '{v}', want substring '{must_contain}')")


def check_backend():
    print(f'\n[8/8] Backend API')
    code = status_only(f"{API}/api/contact")
    if code == 405:
        ok(f"{API}/api/contact -> 405 (alive, allows POST)")
    elif code == 200:
        ok(f"{API}/api/contact -> 200")
    else:
        fail(f"{API}/api/contact -> {code} (expected 405 or 200, anything else = backend down)")


# ────────────────────────────── main ────────────────────────────────────────

def main():
    print(f"Smoke test against {BASE}")
    check_basics()
    locs = check_sitemap()
    if locs:
        check_all_urls_200(locs)
    check_seo_per_lang()
    check_404_page()
    check_redirects_and_stubs()
    check_security_headers()
    check_backend()

    print()
    print('-' * 60)
    total = passes + len(fails)
    if fails:
        print(f"FAIL  {len(fails)}/{total} checks failed:")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)
    print(f"PASS  {passes}/{total} checks")


if __name__ == '__main__':
    main()
