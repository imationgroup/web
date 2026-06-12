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
    # site.webmanifest is accepted with manifest+json, json, or octet-stream
    # (nginx default for unknown extension). Chrome reads it either way.
    for path, accepted_cts in [
        ('/favicon.svg',       ['image/svg']),
        ('/site.webmanifest',  ['manifest+json', 'json', 'octet-stream']),
        ('/robots.txt',        ['text']),
        ('/og-image.svg',      ['image/svg']),
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


def check_seo_per_lang():
    print(f'\n[4/6] Per-language SEO (canonical, hreflang, og:url, JSON-LD)')
    page_re = re.compile(r'<link rel="canonical" href="([^"]+)"')
    og_re = re.compile(r'<meta property="og:url" content="([^"]+)"')
    hreflang_re = re.compile(r'<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)"')
    ldjson_re = re.compile(r'<script type="application/ld\+json"[^>]*>(.+?)</script>', re.S)
    markdown_href_re = re.compile(r'href="\[[^\]]+\]\(https?://')

    for lang in LANGS:
        for page in INDEXED_PAGES:
            url = f"{BASE}/{lang}/{page}" if page else f"{BASE}/{lang}/"
            code, body, _ = fetch(url)
            if code != 200:
                fail(f"GET {url} -> {code}")
                continue

            m = page_re.search(body)
            if not m:
                fail(f"{url} no canonical")
                continue
            if m.group(1) != url:
                fail(f"{url} canonical mismatch: '{m.group(1)}'")
                continue

            mo = og_re.search(body)
            if not mo or mo.group(1) != url:
                fail(f"{url} og:url missing or mismatch")
                continue

            hl = {l: u for l, u in hreflang_re.findall(body)}
            missing_langs = set(LANGS) - set(hl.keys())
            if missing_langs:
                fail(f"{url} missing hreflang for {sorted(missing_langs)}")
                continue
            if 'x-default' not in hl:
                fail(f"{url} missing x-default hreflang")
                continue

            ld = ldjson_re.search(body)
            if not ld:
                fail(f"{url} no JSON-LD")
                continue
            try:
                data = json.loads(ld.group(1))
                graph = data.get('@graph', [data])
                types = {item.get('@type') for item in graph}
                if 'Organization' not in types or 'WebPage' not in types:
                    fail(f"{url} JSON-LD missing Organization/WebPage (got {types})")
                    continue
            except json.JSONDecodeError as e:
                fail(f"{url} JSON-LD invalid: {e}")
                continue

            if markdown_href_re.search(body):
                fail(f"{url} has markdown-wrapped href (regression!)")
                continue

        ok(f"/{lang}/ ({len(INDEXED_PAGES)} pages) - canonical, hreflang, JSON-LD all good")


def check_root_stubs():
    print(f'\n[5/6] Root redirect stubs')
    for stub in ROOT_STUBS:
        code = status_only(f"{BASE}/{stub}")
        if code != 200:
            fail(f"/{stub} -> {code}")
        else:
            ok(f"/{stub} 200 (stub serves for legacy crawlers)")
    # Clean root paths also work via try_files
    for path in ['services', 'projects']:
        code = status_only(f"{BASE}/{path}")
        if code != 200:
            fail(f"/{path} -> {code}")
        else:
            ok(f"/{path} 200 (clean root path)")


def check_backend():
    print(f'\n[6/6] Backend API')
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
    check_root_stubs()
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
