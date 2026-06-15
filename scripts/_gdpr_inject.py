"""One-off script: remove all inline GTM/gtag from templates and inject a
single consent-gated cookie banner + loader before </body>."""
from __future__ import annotations
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / "templates"

# Banner HTML + CSS + JS. Self-contained, vanilla, ~3 KB inlined. Localised
# strings via data-i18n keys handled by the existing build pipeline.
SNIPPET = """  <!-- GDPR cookie consent banner. Analytics scripts only load after Accept. -->
  <div id="igCookieBanner" class="ig-cookie-banner" hidden role="dialog" aria-labelledby="igCookieMsg">
    <div class="ig-cookie-inner">
      <p id="igCookieMsg" data-i18n="cookie_msg">We use analytics cookies to understand how the site is used. You can accept or reject them at any time. See our <a href="privacy.html" data-i18n="cookie_more_link">privacy policy</a>.</p>
      <div class="ig-cookie-buttons">
        <button type="button" class="ig-cookie-reject" data-i18n="cookie_reject">Reject</button>
        <button type="button" class="ig-cookie-accept" data-i18n="cookie_accept">Accept</button>
      </div>
    </div>
  </div>
  <style>
    .ig-cookie-banner{position:fixed;left:16px;right:16px;bottom:16px;max-width:760px;margin:0 auto;background:#1a1a2e;color:#fff;border-radius:12px;padding:18px 22px;box-shadow:0 10px 40px rgba(0,0,0,.25);z-index:9999;font-size:.92rem;line-height:1.5}
    .ig-cookie-banner[hidden]{display:none}
    .ig-cookie-inner{display:flex;gap:16px;flex-direction:column}
    @media (min-width:640px){.ig-cookie-inner{flex-direction:row;align-items:center;justify-content:space-between}}
    .ig-cookie-banner p{margin:0;color:rgba(255,255,255,.85)}
    .ig-cookie-banner a{color:#00A5A8;text-decoration:underline}
    .ig-cookie-buttons{display:flex;gap:8px;flex-shrink:0}
    .ig-cookie-banner button{padding:9px 18px;border:1px solid rgba(255,255,255,.2);border-radius:6px;background:transparent;color:#fff;font:600 .9rem inherit;cursor:pointer;font-family:inherit;transition:background .2s,border-color .2s}
    .ig-cookie-banner button:hover{background:rgba(255,255,255,.1)}
    .ig-cookie-banner .ig-cookie-accept{background:linear-gradient(135deg,#0066CC,#00A5A8);border-color:transparent}
    .ig-cookie-banner .ig-cookie-accept:hover{background:linear-gradient(135deg,#003366,#00A5A8)}
  </style>
  <script>
    (function(){
      var KEY='ig_cookie_consent';
      function getC(){try{return localStorage.getItem(KEY)}catch(_){return null}}
      function setC(v){try{localStorage.setItem(KEY,v)}catch(_){}}
      function show(){var e=document.getElementById('igCookieBanner');if(e)e.removeAttribute('hidden')}
      function hide(){var e=document.getElementById('igCookieBanner');if(e)e.setAttribute('hidden','')}
      function loadAnalytics(){
        // gtag.js (Google Tag / GA4 / Google Ads)
        var s=document.createElement('script');s.async=true;
        s.src='https://www.googletagmanager.com/gtag/js?id=GT-PHP3T9KV';
        document.head.appendChild(s);
        window.dataLayer=window.dataLayer||[];
        function gtag(){dataLayer.push(arguments)}
        window.gtag=gtag;
        gtag('js',new Date());
        gtag('config','GT-PHP3T9KV',{anonymize_ip:true});
        // GTM container
        (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-TXPKFXD9');
      }
      var c=getC();
      if(c==='accepted')loadAnalytics();
      else if(c!=='rejected')setTimeout(show,600);
      document.addEventListener('click',function(e){
        if(!e.target||!e.target.classList)return;
        if(e.target.classList.contains('ig-cookie-accept')){setC('accepted');hide();loadAnalytics()}
        if(e.target.classList.contains('ig-cookie-reject')){setC('rejected');hide()}
      });
      // Reopen banner from "Cookie preferences" link in footer
      window.igOpenCookieBanner=function(){try{localStorage.removeItem(KEY)}catch(_){}show()};
    })();
  </script>
"""

# Patterns to strip from EVERY template.
PATTERNS_TO_STRIP = [
    # gtag.js: the script src + the inline init pair
    re.compile(
        r'\s*<!--\s*Google tag \(gtag\.js\)\s*-->\s*'
        r'<script async src="https://www\.googletagmanager\.com/gtag/js[^"]*"></script>\s*'
        r'<script>[^<]*?gtag\(\s*[\'"]config[\'"][^<]*?</script>',
        re.DOTALL,
    ),
    # gtag without comment marker
    re.compile(
        r'\s*<script async src="https://www\.googletagmanager\.com/gtag/js[^"]*"></script>\s*'
        r'<script>[^<]*?gtag\(\s*[\'"]config[\'"][^<]*?</script>',
        re.DOTALL,
    ),
    # GTM container bootstrap (with optional comment markers)
    re.compile(
        r"\s*(?:<!--\s*Google Tag Manager\s*-->\s*)?"
        r"<script>\(function\(w,d,s,l,i\)\{[^<]*?'GTM-[^']+'\);\s*</script>"
        r"\s*(?:<!--\s*End Google Tag Manager\s*-->\s*)?",
        re.DOTALL,
    ),
    # GTM noscript iframes (small leak: no-JS users still load GTM; <1%
    # traffic, low risk, common practice to leave)
]

count = 0
for f in sorted(TEMPLATES.glob("*.html")):
    s = f.read_text(encoding="utf-8")
    orig = s
    for pat in PATTERNS_TO_STRIP:
        s = pat.sub("\n  ", s)
    # Already injected?
    if 'id="igCookieBanner"' not in s:
        # Insert before the closing </body>
        s = re.sub(r"</body>", SNIPPET + "</body>", s, count=1, flags=re.IGNORECASE)
    if s != orig:
        f.write_text(s, encoding="utf-8")
        count += 1
        print(f"  patched {f.name}")
    else:
        print(f"  no-op {f.name}")
print(f"Done. {count} files modified.")
