"""Ücretsiz modeller: assets/models/models.json → models/index.html, tr/models/index.html ve ana sayfalardaki önizleme.

  python tools/build_models.py

Yeni model: models.json'a bir kayıt ekle (resim assets/ altında, ZIP downloads/ altında), betiği çalıştır.
Ana sayfadaki bölüm <!-- models:start --> ... <!-- models:end --> arasıdır (en yeni 3 model).
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = sorted(json.load(open(os.path.join(ROOT, "assets", "models", "models.json"), encoding="utf-8")),
                key=lambda m: m["added"], reverse=True)
ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>')
T = {
    "en": dict(lang="en", kicker="Free downloads", h2="Free print-ready models",
               sub="Models we check and fix with 3D Vault before you waste filament: watertight, scaled, with print settings. "
                   "New ones every week or so.",
               dl="Download", lic="CC BY 4.0", lic_url="https://creativecommons.org/licenses/by/4.0/",
               all="All free models", home="Home", stamp="the 3D Vault stamp under the base",
               title="Free 3D printable models – 3D Vault | ADK Workshop",
               desc="Free, print-ready STL models checked with 3D Vault: watertight, scaled and tested in the slicer. CC BY 4.0.",
               note='Tag <a href="https://www.instagram.com/adk_3dvault/" target="_blank" rel="noopener">@adk_3dvault</a> when you post a print. '
                    'Want to see how we check them? <a href="{home}#features">3D Vault</a> is free on the Microsoft Store.',
               other="Türkçe", other_href="{tr}models/"),
    "tr": dict(lang="tr", kicker="Ücretsiz indir", h2="Ücretsiz, baskıya hazır modeller",
               sub="Filament harcamadan önce 3D Vault ile kontrol edip onardığımız modeller: su geçirmez, ölçekli, baskı ayarlarıyla. "
                   "Yaklaşık her hafta yenisi.",
               dl="İndir", lic="CC BY 4.0", lic_url="https://creativecommons.org/licenses/by/4.0/deed.tr",
               all="Tüm ücretsiz modeller", home="Ana sayfa", stamp="kaidenin altındaki 3D Vault damgası",
               title="Ücretsiz 3D baskı modelleri – 3D Vault | ADK Workshop",
               desc="3D Vault ile kontrol edilmiş ücretsiz, baskıya hazır STL modeller: su geçirmez, ölçekli, dilimleyicide denenmiş. CC BY 4.0.",
               note='Baskını paylaşırsan <a href="https://www.instagram.com/adk_3dvault/" target="_blank" rel="noopener">@adk_3dvault</a> etiketle. '
                    'Nasıl kontrol ettiğimizi merak ediyorsan <a href="{home}#ozellikler">3D Vault</a> Microsoft Store\'da ücretsiz.',
               other="English", other_href="{en}models/"),
}


def size(fn):
    try:
        return f"{os.path.getsize(os.path.join(ROOT, 'downloads', fn)) / 1e6:.0f} MB"
    except OSError:
        return ""


def card(m, lang, pre):
    t, e = T[lang], html.escape
    name = e(m["name"][lang])
    chips = "".join(f'<span class="chip">{e(x)}</span>' for x in m["tags"][lang])
    chips += "".join(f'<span class="chip spec">{e(x)}</span>' for x in m["specs"][lang])
    bottom = (f'<img class="bottom" src="{pre}assets/{m["bottom"]}" alt="{e(t["stamp"])}" loading="lazy">' if m.get("bottom") else "")
    extra = ""
    if m.get("extra"):
        extra = f'<a class="btn" href="{pre}downloads/{m["extra"]["file"]}" download>{e(m["extra"][lang])}</a>'
    return f'''<article class="mcard" id="{m["id"]}">
  <div class="mimg"><img class="main{" contain" if m.get("fit") == "contain" else ""}" src="{pre}assets/{m["image"]}" alt="{name}" loading="lazy">{bottom}</div>
  <div class="mbody">
    <h3>{name}</h3>
    <div class="chips">{chips}</div>
    <p>{e(m["text"][lang])}</p>
    <p class="credit">{e(m["credit"][lang])} · <a href="{t["lic_url"]}" target="_blank" rel="noopener">{t["lic"]}</a></p>
    <div class="mbtns"><a class="btn primary" href="{pre}downloads/{m["zip"]}" download>{ICON}{t["dl"]} ({size(m["zip"])})</a>{extra}</div>
  </div>
</article>'''


def page(lang):
    t = T[lang]
    pre = "../" if lang == "en" else "../../"
    home = "../" if lang == "en" else "../"
    other = t["other_href"].format(tr="../tr/", en="../../")
    cards = "\n".join(card(m, lang, pre) for m in MODELS)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{t["desc"]}">
<meta property="og:image" content="https://3dvault.adkworkshop.com/assets/{MODELS[0]["image"]}">
<meta property="og:type" content="website">
<link rel="alternate" hreflang="en" href="https://3dvault.adkworkshop.com/models/">
<link rel="alternate" hreflang="tr" href="https://3dvault.adkworkshop.com/tr/models/">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}assets/icon-32.png">
<link rel="apple-touch-icon" href="{pre}assets/icon-180.png">
<link rel="stylesheet" href="{pre}assets/site.css">
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="brand" href="{home}"><img src="{pre}assets/icon-64.png" alt="">3D Vault <small>by ADK Workshop</small></a>
    <nav>
      <a href="{home}">{t["home"]}</a>
      <a class="lang" href="{other}" hreflang="{"tr" if lang == "en" else "en"}">{t["other"]}</a>
    </nav>
  </div>
</header>

<section class="models-page">
  <div class="wrap">
    <div class="center">
      <p class="kicker">{t["kicker"]}</p>
      <h2>{t["h2"]}</h2>
      <p class="sub">{t["sub"]}</p>
    </div>
    <div class="mgrid">
{cards}
    </div>
    <p class="mnote center">{t["note"].format(home=home)}</p>
  </div>
</section>

<footer>
  <div class="wrap">
    <span>© 2026 <a href="https://adkworkshop.com/">ADK Workshop</a></span>
    <div class="links">
      <a href="{pre}privacy.html">{"Privacy policy" if lang == "en" else "Gizlilik politikası"}</a>
      <a href="mailto:support@adkworkshop.com">{"Support" if lang == "en" else "Destek"}</a>
      <a href="https://www.instagram.com/adk_3dvault/" target="_blank" rel="noopener">Instagram</a>
    </div>
  </div>
</footer>
</body>
</html>
'''


def teaser(lang):
    t = T[lang]
    pre = "" if lang == "en" else "../"
    link = "models/"
    cards = "\n".join(card(m, lang, pre) for m in MODELS[:3])
    return f'''<!-- models:start -->
<section id="free-models" class="alt">
  <div class="wrap">
    <div class="center">
      <p class="kicker">{t["kicker"]}</p>
      <h2>{t["h2"]}</h2>
      <p class="sub">{t["sub"]}</p>
    </div>
    <div class="mgrid">
{cards}
    </div>
    <p class="more"><a class="btn" href="{link}">{t["all"]} ({len(MODELS)}) →</a></p>
  </div>
</section>
<!-- models:end -->'''


def patch_home(path, lang):
    s = open(path, encoding="utf-8").read()
    if "<!-- models:start -->" in s:
        a, b = s.index("<!-- models:start -->"), s.index("<!-- models:end -->") + len("<!-- models:end -->")
    else:                                                            # ilk sefer: eski bölümü değiştir
        a = s.index('<section id="free-models"')
        b = s.index("</section>", a) + len("</section>")
    s = s[:a] + teaser(lang) + s[b:]
    open(path, "w", encoding="utf-8").write(s)


for lang, out, home in (("en", "models/index.html", "index.html"), ("tr", "tr/models/index.html", "tr/index.html")):
    p = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(page(lang))
    patch_home(os.path.join(ROOT, home), lang)
print("ok", len(MODELS), "models")
