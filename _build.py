#!/usr/bin/env python3
"""Builds the static pages from _src/*.html: fills the shared head, header and footer.
   python3 _build.py      (writes index.html, products.html, about.html, contact.html, privacy.html,
                           thanks.html, 404.html, ar/index.html, ar/privacy.html, ar/thanks.html)
   Files and folders starting with "_" are skipped by GitHub Pages (Jekyll), so _src and this script stay private."""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src"
SITE = "https://limitlessgoals.ae"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&{ar}display=swap" rel="stylesheet">')

def head(meta, p, lang):
    ar = "family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&" if lang == "ar" else ""
    alt = ""
    if "en" in meta and "ar" in meta:
        alt = (f'<link rel="alternate" hreflang="en" href="{SITE}/{meta["en"]}">\n'
               f'<link rel="alternate" hreflang="ar" href="{SITE}/{meta["ar"]}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{SITE}/{meta["en"]}">\n')
    canon = meta.get("canon", "")
    robots = '<meta name="robots" content="noindex">\n' if meta.get("noindex") else ""
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["title"]}</title>
<meta name="description" content="{meta["desc"]}">
{robots}<link rel="canonical" href="{SITE}/{canon}">
{alt}<meta property="og:type" content="website">
<meta property="og:site_name" content="Limitless Goals">
<meta property="og:title" content="{meta["title"]}">
<meta property="og:description" content="{meta["desc"]}">
<meta property="og:url" content="{SITE}/{canon}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="theme-color" content="#14214f">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add("js")</script>
{FONTS.format(ar=ar)}
<link rel="stylesheet" href="{p}css/site.css">'''

NAV = {
 "en": [("products.html", "Products"), ("about.html", "About"), ("contact.html", "Contact")],
 "ar": [("../products.html", "المنتجات <small lang=\"en\">(EN)</small>"), ("../about.html", "من نحن <small lang=\"en\">(EN)</small>"), ("#enquiry", "تواصل معنا")],
}

def header(page, p, lang, other):
    links = "".join(
        f'<a class="link" href="{p if lang=="en" else ""}{h}"{" aria-current=page" if h.split("/")[-1]==page and lang=="en" else ""}>{t}</a>'
        for h, t in NAV[lang])
    home = f"{p}index.html" if lang == "en" else "index.html"
    if lang == "ar": home = "./"
    else: home = f"{p}./" if p else "./"
    skip = "تخطَّ إلى المحتوى" if lang == "ar" else "Skip to content"
    menu = "القائمة" if lang == "ar" else "Menu"
    lang_link = (f'<a class="top__lang" href="{other}" lang="ar" hreflang="ar">عربي</a>' if lang == "en"
                 else f'<a class="top__lang" href="{other}" lang="en" hreflang="en">EN</a>')
    logo_label = "Limitless Goals, home" if lang == "en" else "Limitless Goals، الصفحة الرئيسية"
    return f'''<a class="skip" href="#main">{skip}</a>
<header class="top"><div class="wrap top__in">
  <a class="top__logo" href="{home}"><img src="{p}img/logo.svg" alt="{logo_label}" width="168" height="84"></a>
  <nav class="nav" id="nav" aria-label="{'الرئيسية' if lang=='ar' else 'Main'}">{links}</nav>
  <a class="top__tel" href="tel:+971547799003"><span class="roll"><span data-text="+971 54 779 9003" dir="ltr">+971 54 779 9003</span></span></a>
  {lang_link}
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav"><span></span><b class="vh">{menu}</b></button>
</div></header>'''

def footer(p, lang):
    if lang == "ar":
        return f'''<footer class="foot" lang="ar"><div class="wrap">
  <div class="foot__grid">
    <div><img class="foot__logo" src="{p}img/logo-white.svg" alt="Limitless Goals" width="190" height="95">
      <p>Limitless Goals Import &amp; Export Services<br>شركة تجارة عامة، الإمارات العربية المتحدة</p>
      <!-- TODO(Mans): add the registered office address and trade licence number here once published. Do not invent. -->
    </div>
    <div><h2>تواصل</h2><ul>
      <li><a class="link" href="mailto:info@limitlessgoals.ae">info@limitlessgoals.ae</a></li>
      <li><a class="link" href="tel:+971547799003"><bdi>+971 54 779 9003</bdi></a></li>
      <li><span>فاكس <bdi>04 393 9670</bdi></span></li>
    </ul></div>
    <div><h2>الصفحات</h2><ul>
      <li><a class="link" href="./">الرئيسية</a></li>
      <li><a class="link" href="../products.html">المنتجات (EN)</a></li>
      <li><a class="link" href="../about.html">من نحن (EN)</a></li>
      <li><a class="link" href="../contact.html">نموذج الاستفسار (EN)</a></li>
    </ul></div>
    <div><h2>قانوني</h2><ul>
      <li><a class="link" href="privacy.html">سياسة الخصوصية</a></li>
      <li><span>لا نستخدم ملفات تعريف ارتباط للتتبع.</span></li>
    </ul></div>
  </div>
  <div class="foot__base"><span>© <bdi>2026</bdi> Limitless Goals Import &amp; Export Services. جميع الحقوق محفوظة.</span><a class="link" href="../index.html" lang="en" hreflang="en">English</a></div>
</div></footer>'''
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot__grid">
    <div><img class="foot__logo" src="{p}img/logo-white.svg" alt="Limitless Goals" width="190" height="95">
      <p>Limitless Goals Import &amp; Export Services<br>General trading, United Arab Emirates</p>
      <!-- TODO(Mans): add the registered office address and trade licence number here once published. Do not invent. -->
    </div>
    <div><h2>Contact</h2><ul>
      <li><a class="link" href="mailto:info@limitlessgoals.ae">info@limitlessgoals.ae</a></li>
      <li><a class="link" href="tel:+971547799003">+971 54 779 9003</a></li>
      <li><span>Fax 04 393 9670</span></li>
    </ul></div>
    <div><h2>Pages</h2><ul>
      <li><a class="link" href="{p}products.html">Products</a></li>
      <li><a class="link" href="{p}about.html">About</a></li>
      <li><a class="link" href="{p}contact.html">Contact</a></li>
      <li><a class="link" href="{p}ar/" lang="ar" hreflang="ar">العربية</a></li>
    </ul></div>
    <div><h2>Legal</h2><ul>
      <li><a class="link" href="{p}privacy.html">Privacy policy</a></li>
      <li><span>We don't use tracking cookies.</span></li>
    </ul></div>
  </div>
  <div class="foot__base"><span>© 2026 Limitless Goals Import &amp; Export Services. All rights reserved.</span><span>Photos: Unsplash, credited in the page source.</span></div>
</div></footer>'''

def build(src):
    raw = src.read_text()
    m = re.match(r"<!--META\n(.*?)\nMETA-->\n", raw, re.S)
    meta = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if l.strip())}
    for k in ("noindex",): meta[k] = meta.get(k) == "true"
    body = raw[m.end():]
    out = meta["out"]; lang = meta.get("lang", "en")
    p = meta.get("prefix", "")
    page = out.split("/")[-1]
    dirattr = ' dir="rtl"' if lang == "ar" else ""
    html = f'''<!doctype html>
<html lang="{lang}"{dirattr}>
<head>
{head(meta, p, lang)}
</head>
<body>
{header(page, p, lang, meta.get("other", "ar/"))}
{body.strip()}
{footer(p, lang)}
<script src="{p}js/site.js" defer></script>
</body>
</html>
'''
    dest = ROOT / out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print("wrote", out)

for f in sorted(SRC.rglob("*.html")):
    build(f)
