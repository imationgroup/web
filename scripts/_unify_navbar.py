"""Replace the simplified <nav class="navbar"> of every interior template
with the full navbar from templates/index.html, so the header is byte-
identical across the static site. The build script rewrites the in-page
anchors (#about etc.) to /<lang>/#anchor for interior pages so the links
actually go somewhere meaningful."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TPL = REPO / "templates"

# 1. Extract the full navbar block from index.html.
src = (TPL / "index.html").read_text(encoding="utf-8")
m = re.search(r'<nav class="navbar">.*?</nav>', src, re.S)
assert m, "couldn't find <nav class=\"navbar\"> in index.html"
NAVBAR_HTML = m.group(0)

# 2. Extract the CSS rules from index.html that style the navbar, lang
#    switcher and logo. We need to give the interiors the same styling.
#    Pulling the entire <style> block of index would be too invasive; instead
#    keep an exact whitelist of selectors. Using a literal set (not a regex)
#    sidesteps the trap where a regex anchored only at the dropdown name
#    silently strips a parent prefix -- e.g. `.nav-projects.open
#    .nav-projects-dropdown` would be captured as a bare
#    `.nav-projects-dropdown` rule and force the dropdown to stay open on
#    every page.
def _norm_sel(s):
    # Collapse whitespace, strip whitespace around combinators (>, +, ~) so
    # ".nav-projects > a" and minified ".nav-projects>a" hash the same, and
    # unify "::before" vs ":before" so equality holds.
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s*([>+~])\s*", r"\1", s)
    s = s.replace("::", ":")
    return s


NAV_SELECTORS = {_norm_sel(s) for s in [
    ".navbar", ".navbar.scrolled",
    ".nav-container",
    ".logo", ".logo img", ".logo .logo-text",
    ".nav-links", ".nav-links a", ".nav-links a:after",
    ".nav-links a::after", ".nav-links a:hover", ".nav-links a:hover::after",
    ".nav-links a:hover:after",
    ".nav-projects", ".nav-projects > a", ".nav-projects > a:before",
    ".nav-projects > a::before", ".nav-projects.open > a:before",
    ".nav-projects.open > a::before",
    ".nav-projects-dropdown", ".nav-projects.open .nav-projects-dropdown",
    ".nav-projects-dropdown li a", ".nav-projects-dropdown li a:after",
    ".nav-projects-dropdown li a::after", ".nav-projects-dropdown li a:hover",
    ".nav-projects-dropdown li.divider",
    ".lang-switcher",
    ".lang-btn", ".lang-btn:hover", ".lang-btn.open",
    ".lang-dropdown", ".lang-dropdown.active",
    ".lang-option", ".lang-option:hover", ".lang-option.active",
    ".lang-flag-icon", ".lang-chevron",
    ".mobile-menu-btn", ".mobile-menu-btn span",
    ".mobile-menu-btn.open", ".mobile-menu-btn.open span",
    ".divider",
]}


def _iter_rules(css):
    """Yield (selector, raw_rule_text) for each top-level rule in css.

    Skips @media / @keyframes / @supports etc -- callers handle those
    separately via _split_top_and_media. CSS /* ... */ comments are
    stripped first so they don't get absorbed into the next selector.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i, n = 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            return
        sel = css[i:brace]
        if sel.lstrip().startswith("@"):
            depth, j = 1, brace + 1
            while j < n and depth > 0:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            i = j
            continue
        end = css.find("}", brace)
        if end == -1:
            return
        yield sel.strip(), css[i:end + 1]
        i = end + 1
def _split_top_and_media(css):
    """Return (top_level_css, [(media_query, inner_css), ...]).

    Walks the string and balances braces so @media blocks are extracted as
    units, not chopped open. Without this, nav rules inside @media (e.g.
    `.nav-links{display:none}` in the mobile breakpoint) get re-emitted as
    top-level rules and hide the nav links on desktop too.
    """
    media_blocks = []
    top_parts = []
    i = 0
    while i < len(css):
        if css[i:i+6] == "@media":
            brace = css.find("{", i)
            if brace == -1:
                break
            mq = css[i:brace]
            depth = 1
            j = brace + 1
            while j < len(css) and depth > 0:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            media_blocks.append((mq.strip(), css[brace + 1:j - 1]))
            i = j
        else:
            top_parts.append(css[i])
            i += 1
    return "".join(top_parts), media_blocks


_top, _media = _split_top_and_media(src)
nav_css_chunks = []
seen = set()
for sel, rule in _iter_rules(_top):
    if _norm_sel(sel) in NAV_SELECTORS:
        norm = re.sub(r"\s+", " ", rule).strip()
        if norm not in seen:
            seen.add(norm)
            nav_css_chunks.append(rule)
# Nav rules that live inside @media -- re-wrap them in their original query.
for mq, inner in _media:
    inner_hits = []
    inner_seen = set()
    for sel, rule in _iter_rules(inner):
        if _norm_sel(sel) in NAV_SELECTORS:
            norm = re.sub(r"\s+", " ", rule).strip()
            if norm not in inner_seen:
                inner_seen.add(norm)
                inner_hits.append(rule)
    if inner_hits:
        nav_css_chunks.append(f"{mq}{{{' '.join(inner_hits)}}}")
NAV_CSS = "\n".join(nav_css_chunks)
print(f"Extracted {len(nav_css_chunks)} nav-related CSS rules ({len(NAV_CSS)} chars).")

# 3. Extract the body scripts that drive the navbar (lang dropdown, mobile
#    menu, projects dropdown). They live in <script> blocks at the end of
#    body in index.html. Grab any script that mentions lang-option /
#    langToggle / navProjects / mobile-menu-btn / scrolled.
SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.S)
scripts_needed = []
for sc in SCRIPT_RE.finditer(src):
    body = sc.group(0)
    if any(k in body for k in ("langToggle", "lang-option", "navProjects",
                                "mobile-menu-btn", "navbar.scrolled",
                                "currentLangFlag")):
        scripts_needed.append(body)
NAV_SCRIPTS = "\n".join(scripts_needed)
print(f"Extracted {len(scripts_needed)} nav-related script blocks.")

# 4. For each interior template, splice in the new navbar.
INTERIORS = ["services.html", "projects.html", "terms.html", "privacy.html",
             "contact-success.html"]

# Old per-template CSS rules that fight the unified nav. These had higher
# specificity than our injected `.logo` etc., so they were winning the
# cascade and producing subtle metrics differences (e.g. logo font-size
# 1.4rem on interiors vs 1.35rem on the home).
STRIP_PATTERNS = [
    # Old per-template nav CSS that fights the unified rules. Specificity
    # ties go to source order, and a property set in the OLD .navbar block
    # but absent from the unified one (e.g. padding: 16px 0) is not
    # overridden -- so we strip the whole old block.
    r"\s*\.navbar[^a-zA-Z-]*\{[^}]*\}",            # the bare .navbar rule
    r"\s*\.navbar\.scrolled[^{]*\{[^}]*\}",
    r"\s*\.navbar\s+\.container[^{]*\{[^}]*\}",
    r"\s*\.navbar\s+\.logo[^{]*\{[^}]*\}",
    r"\s*\.navbar\s+\.back-link[^{]*\{[^}]*\}",
    r"\s*\.nav-container[^a-zA-Z-]*\{[^}]*\}",
    r"\s*\.nav-right[^{]*\{[^}]*\}",
    r"\s*\.back-link[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.back-link:hover[^{]*\{[^}]*\}",
    r"\s*\.lang-switch[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.lang-switch\s+button[^{]*\{[^}]*\}",
    r"\s*\.lang-switch\s+button\.active[^{]*\{[^}]*\}",
    r"\s*\.lang-btn[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.lang-btn:hover[^{]*\{[^}]*\}",
    r"\s*\.lang-btn\.open[^{]*\{[^}]*\}",
    r"\s*\.lang-flag-icon[^{]*\{[^}]*\}",
    r"\s*\.lang-dropdown[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.lang-dropdown\.active[^{]*\{[^}]*\}",
    r"\s*\.lang-option[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.lang-option:hover[^{]*\{[^}]*\}",
    r"\s*\.lang-option\.active[^{]*\{[^}]*\}",
    r"\s*\.lang-chevron[^{]*\{[^}]*\}",
    r"\s*\.lang-switcher[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.mobile-menu-btn[^{a-zA-Z-]*\{[^}]*\}",
    r"\s*\.mobile-menu-btn\s+span[^{]*\{[^}]*\}",
    # Old simplified `.logo` rule from the previous interior patch.
    r"\s*\.logo\{[^}]*font-size:\s*1\.25rem[^}]*\}",
    r"\s*\.logo\s+img\{[^}]*width:\s*32px[^}]*\}",
    # Bare .logo block that doesn't use display:inline-flex (= an old version)
    r"\s*\.logo\s*\{(?![^}]*inline-flex)[^}]*\}",
]

for fname in INTERIORS:
    p = TPL / fname
    s = p.read_text(encoding="utf-8")
    orig = s

    # 1. Strip the conflicting CSS rules from the interior's own <style>.
    for pat in STRIP_PATTERNS:
        s = re.sub(pat, "", s)

    # 2. Replace the existing <nav class="navbar"> ... </nav>.
    s = re.sub(r'<nav class="navbar">.*?</nav>', NAVBAR_HTML, s, count=1, flags=re.S)

    # 3. Inject the nav-related CSS from index.html as a NEW <style> right
    #    before </head>. Idempotent via marker comment.
    NAV_CSS_BLOCK = f"<!-- nav unified -->\n<style>{NAV_CSS}</style>\n"
    if "<!-- nav unified -->" in s:
        # Replace the previous block so re-running the script keeps things up
        # to date with the home CSS.
        s = re.sub(r"<!-- nav unified -->\s*<style>[^<]*</style>\s*",
                   lambda _: NAV_CSS_BLOCK, s, count=1, flags=re.S)
    else:
        s = s.replace("</head>", NAV_CSS_BLOCK + "</head>", 1)

    # 4. Inject nav scripts before </body>.
    SCRIPTS_BLOCK = f"<!-- nav scripts unified -->\n{NAV_SCRIPTS}\n"
    if "<!-- nav scripts unified -->" in s:
        s = re.sub(r"<!-- nav scripts unified -->.*?(?=</body>)",
                   lambda _: SCRIPTS_BLOCK, s, count=1, flags=re.S)
    else:
        s = s.replace("</body>", SCRIPTS_BLOCK + "</body>", 1)

    if s != orig:
        p.write_text(s, encoding="utf-8")
        print(f"  patched {fname}")
    else:
        print(f"  no-op  {fname}")

print("Done.")
