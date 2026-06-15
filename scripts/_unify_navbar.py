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
nav_css_chunks = []
for pat in NAV_SELECTORS:
    for hit in re.finditer(pat, src):
        nav_css_chunks.append(hit.group(0))
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

for fname in INTERIORS:
    p = TPL / fname
    s = p.read_text(encoding="utf-8")
    orig = s

    # Replace the existing <nav class="navbar"> ... </nav>
    s = re.sub(r'<nav class="navbar">.*?</nav>', NAVBAR_HTML, s, count=1, flags=re.S)

    # Make sure the page imports the nav-related CSS. We inject as a NEW
    # <style> block right before </head>. If the block is already there,
    # don't double-inject.
    NAV_CSS_BLOCK = f"<!-- nav unified -->\n<style>{NAV_CSS}</style>\n"
    if "<!-- nav unified -->" not in s:
        s = s.replace("</head>", NAV_CSS_BLOCK + "</head>", 1)

    # Inject nav scripts before </body>.
    if "<!-- nav scripts unified -->" not in s:
        SCRIPTS_BLOCK = f"<!-- nav scripts unified -->\n{NAV_SCRIPTS}\n"
        s = s.replace("</body>", SCRIPTS_BLOCK + "</body>", 1)

    if s != orig:
        p.write_text(s, encoding="utf-8")
        print(f"  patched {fname}")
    else:
        print(f"  no-op  {fname}")

print("Done.")
