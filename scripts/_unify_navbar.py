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
#    pull only the nav-related selectors.
NAV_SELECTORS = [
    r"\.navbar\s*\{[^}]+\}",
    r"\.navbar\.scrolled\s*\{[^}]+\}",
    r"\.nav-container\s*\{[^}]+\}",
    r"\.logo\s*\{[^}]+\}",
    r"\.logo\s+img\s*\{[^}]+\}",
    r"\.logo\s+\.logo-text\s*\{[^}]+\}",
    r"\.nav-links\s*\{[^}]+\}",
    r"\.nav-links\s+a[^{]*\{[^}]+\}",
    r"\.nav-links\s+a:after\s*\{[^}]+\}",
    r"\.nav-links\s+a:hover[^{]*\{[^}]+\}",
    r"\.nav-projects[^{]*\{[^}]+\}",
    r"\.nav-projects-dropdown[^{]*\{[^}]+\}",
    r"\.nav-projects-dropdown\s+[^{]+\{[^}]+\}",
    r"\.nav-projects\.open[^{]*\{[^}]+\}",
    r"\.lang-switcher[^{]*\{[^}]+\}",
    r"\.lang-btn[^{]*\{[^}]+\}",
    r"\.lang-btn:hover[^{]*\{[^}]+\}",
    r"\.lang-btn\.open[^{]*\{[^}]+\}",
    r"\.lang-dropdown[^{]*\{[^}]+\}",
    r"\.lang-dropdown\.active[^{]*\{[^}]+\}",
    r"\.lang-option[^{]*\{[^}]+\}",
    r"\.lang-option:hover[^{]*\{[^}]+\}",
    r"\.lang-option\.active[^{]*\{[^}]+\}",
    r"\.lang-flag-icon[^{]*\{[^}]+\}",
    r"\.lang-chevron[^{]*\{[^}]+\}",
    r"\.mobile-menu-btn[^{]*\{[^}]+\}",
    r"\.mobile-menu-btn\s+span[^{]*\{[^}]+\}",
    r"\.mobile-menu-btn\.open[^{]*\{[^}]+\}",
    r"\.mobile-menu-btn\.open\s+span[^{]*\{[^}]+\}",
    r"\.divider[^{]*\{[^}]+\}",
]
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
for pat in NAV_SELECTORS:
    for hit in re.finditer(pat, _top):
        nav_css_chunks.append(hit.group(0))
# Now handle nav rules that live inside @media -- re-wrap them in their query.
for mq, inner in _media:
    inner_hits = []
    for pat in NAV_SELECTORS:
        for hit in re.finditer(pat, inner):
            inner_hits.append(hit.group(0))
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
