# -*- coding: utf-8 -*-
"""Generator statycznej wersji testowej strony Jubilat.

Uruchomienie:  python _src/build.py      (z katalogu repozytorium albo dowolnego)
Wynik: pliki HTML w katalogu repozytorium (index.html, sklepy/..., eleganza/...), assets/img, sitemap.xml, robots.txt.
Treści i dane: _src/dane.py. Meta (title/description/H1/slug): _src/seo_0511/META.json. FAQ: _src/seo_0511/TRESCI.md.
Każda podstrona = osobny szablon w WordPressie (patrz _src/WORDPRESS.md).
"""
import hashlib, html, json, os, re, shutil, sys, datetime
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import dane as D  # noqa: E402

WIZ = ROOT / "wizualizacja" / "img"
RAW = SRC / "raw"
LIVE = SRC / "live_0511"
OUT_IMG = ROOT / "assets" / "img"
OUT_IMG.mkdir(parents=True, exist_ok=True)
DZIS = datetime.date.today().isoformat()

e = lambda s: html.escape(str(s), quote=True)
META = {m["slug"]: m for m in json.loads((SRC / "seo_0511" / "META.json").read_text(encoding="utf-8"))["strony"]}
PYTANIA = []  # pytania do klienta zbierane w trakcie budowania

# ------------------------------------------------------------------ obrazy
from PIL import Image  # noqa: E402
IMG_CACHE = {}


def _zapisz(im, base, w, alpha):
    p_av, p_wb = OUT_IMG / f"{base}-{w}.avif", OUT_IMG / f"{base}-{w}.webp"
    if p_av.exists() and p_wb.exists():
        return
    r = im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if not alpha:
        r = r.convert("RGB")
    r.save(p_av, quality=52, speed=6)
    r.save(p_wb, quality=78, method=6)


def przygotuj(key, src, widths, crop=None, alpha=False):
    """Tworzy warianty AVIF/WebP; crop = (szer, wys) proporcje przycięcia środka."""
    if key in IMG_CACHE:
        return IMG_CACHE[key]
    im = Image.open(src)
    im = im.convert("RGBA" if alpha else "RGB")
    if crop:
        cw, ch = crop
        tr = cw / ch
        if im.width / im.height > tr:
            nw = round(im.height * tr); x = (im.width - nw) // 2
            im = im.crop((x, 0, x + nw, im.height))
        else:
            nh = round(im.width / tr); y = round((im.height - nh) * 0.4)
            im = im.crop((0, y, im.width, y + nh))
    ws = sorted({min(w, im.width) for w in widths})
    for w in ws:
        _zapisz(im, key, w, alpha)
    info = {"key": key, "ws": ws, "ratio": im.height / im.width}
    IMG_CACHE[key] = info
    return info


def pic(P, info, alt, sizes="100vw", cls="", lazy=True, prio=False, img_cls="", style=""):
    k, ws = info["key"], info["ws"]
    big = ws[-1]
    w0 = ws[min(len(ws) - 1, 1)] if len(ws) > 1 else big
    h = round(w0 * info["ratio"])
    ss = lambda ext: ", ".join(f"{P.a('assets/img/' + k + '-' + str(w) + '.' + ext)} {w}w" for w in ws)
    attrs = ' loading="lazy" decoding="async"' if lazy else ""
    if prio:
        attrs += ' fetchpriority="high"'
    return (f'<picture{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>'
            f'<source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<img src="{P.a("assets/img/" + k + "-" + str(w0) + ".webp")}" srcset="{ss("webp")}" sizes="{sizes}" width="{w0}" height="{h}" alt="{e(alt)}"{attrs}'
            f'{(" class=" + chr(34) + img_cls + chr(34)) if img_cls else ""}{(" style=" + chr(34) + style + chr(34)) if style else ""}></picture>')


def url_img(info, w=None):
    w = w or info["ws"][-1]
    return f"assets/img/{info['key']}-{w}.webp"


FOTO_PL = {
    "dh": WIZ / "dh.jpg", "s-lniana": RAW / "s.31-scaled.avif", "s-makowskiego": RAW / "s.19-scaled.avif",
    "s-mazowiecka": RAW / "IMG_6877.avif", "s-rydla": RAW / "IMG_6881-002.avif", "s-modrzewiowa": RAW / "s.27-scaled.avif",
    "s-nastawach": RAW / "s.32-scaled.avif", "s-orla": RAW / "s.25-scaled.avif", "s-przegorzalska": RAW / "s28.avif",
    "bar-zaczek": RAW / "bar-mleczny-zaczek-68788408d0331.avif", "bar-flisak": RAW / "bar_2_bg.avif",
}
FOTO_ALT = {
    "dh": "Dom Handlowy Jubilat przy al. Krasińskiego, modernistyczny budynek z przeszkloną fasadą i neonem JUBILAT na dachu",
    "bar-zaczek": "Wejście do baru mlecznego Żaczek przy ul. Czarnowiejskiej",
    "bar-flisak": "Bar mleczny Flisak przy ul. Kościuszki, witryna z menu",
}


def foto_pl(p, kw="duze"):
    src = FOTO_PL[p["foto"]]
    if kw == "kw":
        return przygotuj(p["foto"] + "-kw", src, [96, 192], crop=(1, 1))
    return przygotuj(p["foto"], src, [480, 820, 1280, 1600])


def alt_pl(p):
    return FOTO_ALT.get(p["foto"], f"Sklep Jubilat przy {p['adres']} w Krakowie, widok wejścia")


# ------------------------------------------------------------------ czas, godziny
DNI_TYG = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
MIES = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"]


def hh(s):
    h, m = s.split(":")
    return f"{int(h)}:{m}"


def zakres(g):
    return f"{hh(g[0])}-{hh(g[1])}" if g else "nieczynne"


def data_pl(iso, rok=True):
    y, m, d = map(int, iso.split("-"))
    return f"{d} {MIES[m - 1]}" + (f" {y}" if rok else "")


def data_kr(iso):
    y, m, d = iso.split("-")
    return f"{d}.{m}.{y}"


def nh_przyszle(n=8):
    return [d for d in D.NIEDZIELE_HANDLOWE if d >= DZIS][:n]


def nh_tekst(lim=3):
    l = nh_przyszle(lim)
    if not l:
        return ""
    # "6, 13 i 20 grudnia" gdy ten sam miesiąc
    mies = {x[5:7] for x in l}
    if len(mies) == 1:
        dni = [str(int(x[8:])) for x in l]
        return (", ".join(dni[:-1]) + " i " + dni[-1] if len(dni) > 1 else dni[0]) + " " + MIES[int(l[0][5:7]) - 1]
    return ", ".join(data_pl(x, False) for x in l)


def tabela_godz(g, caption=None, nh_daty=True):
    nh = nh_tekst(3) if (nh_daty and g.get("nh")) else ""
    rows = [("pt", "Poniedziałek - piątek", g["pt"]), ("sob", "Sobota", g["sob"]), ("nh", "Niedziela handlowa", g.get("nh")),
            ("nd", "Pozostałe niedziele i święta", None)]
    out = f'<table class="gt" data-gt>' + (f"<caption>{e(caption)}</caption>" if caption else "")
    for r, n, v in rows:
        extra = f'<span class="nh-daty">najbliższe: {e(nh)}</span>' if r == "nh" and nh else ""
        out += f'<tr data-r="{r}"><th scope="row">{n}{extra}</th><td>{zakres(v)}</td></tr>'
    return out + "</table>"


def tabela_mini(g, tytul=None):
    out = f'<tr><td class="dzial" colspan="2">{e(tytul)}</td></tr>' if tytul else ""
    for r, n, v in [("pt", "Poniedziałek-piątek", g["pt"]), ("sob", "Sobota", g["sob"]), ("nh", "Niedziela handlowa", g.get("nh")), ("nd", "Pozostałe niedziele i święta", None)]:
        out += f'<tr data-r="{r}"><td>{n}</td><td>{zakres(v)}</td></tr>'
    return out


def tel_href(t):
    return "tel:+48" + re.sub(r"\D", "", t)


def prowadz(p):
    return f"https://www.google.com/maps/dir/?api=1&amp;destination={p['lat']},{p['lng']}"


PL = {p["id"]: p for p in D.PLACOWKI}
# dzielnice wg pakietu SEO (TRESCI.md)
DZIELNICE = {"lniana": "Tonie, Prądnik Biały", "makowskiego": "Azory", "mazowiecka": "Krowodrza", "rydla": "Bronowice", "modrzewiowa": "Wola Justowska",
             "nastawach": "Półwsie Zwierzynieckie", "orla": "Bielany", "przegorzalska": "Przegorzały"}
SKLEPY = [p for p in D.PLACOWKI if p["typ"] == "sklep"]
BARY = [PL["zaczek"], PL["flisak"]]
DH = PL["dh"]


def path_pl(p):
    if p["typ"] == "dh":
        return "dom-handlowy/"
    if p["typ"] == "bar":
        return f"bary-mleczne/{p['slug']}/"
    return f"sklepy/{p['slug']}/"


# ------------------------------------------------------------------ FAQ z TRESCI.md
def wczytaj_faq():
    t = (SRC / "seo_0511" / "TRESCI.md").read_text(encoding="utf-8")
    out = {}
    for key, body in re.findall(r"<!-- faq:(\w+) -->(.*?)<!-- /faq -->", t, re.S):
        qa = re.findall(r"\*\*(.+?\?)\*\*\s*\n(.+?)(?=\n\s*\n|\Z)", body, re.S)
        lst = []
        for q, a in qa:
            a = re.sub(r"\s*\*\*\[DO POTWIERDZENIA[^\]]*\]\*\*", "", a).strip()
            lst.append([q.strip(), " ".join(a.split())])
        out[key] = lst
    # poprawka: kontakt w sprawie rekrutacji wg ogłoszeń (plakaty ofert)
    for x in out.get("praca", []):
        if x[0].startswith("Z kim się kontaktować"):
            x[1] = "Z działem rekrutacji: tel. 780 191 147, e-mail rekrutacja@jubilat.com.pl. W treści wiadomości prosimy wpisać stanowisko, na które aplikujesz."
    return out


FAQ = wczytaj_faq()


def faq_html(key, tytul="Najczęstsze pytania"):
    lst = FAQ.get(key)
    if not lst:
        return ""
    items = "".join(f'<details class="faq-q"><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>' for q, a in lst)
    return f'<section class="sek faq" aria-labelledby="faq-{key}"><div class="wrap faq-uklad"><h2 id="faq-{key}">{tytul}</h2><div class="faq-lista">{items}</div></div></section>'


def faq_ld(key):
    lst = FAQ.get(key)
    if not lst:
        return None
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in lst]}


# ------------------------------------------------------------------ JSON-LD
B = D.CANONICAL_BASE
ORG_ID = B + "/#organization"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def godz_ld(g):
    out = [{"@type": "OpeningHoursSpecification", "dayOfWeek": [f"https://schema.org/{d}" for d in DAYS], "opens": g["pt"][0], "closes": g["pt"][1]}]
    if g.get("sob"):
        out.append({"@type": "OpeningHoursSpecification", "dayOfWeek": ["https://schema.org/Saturday"], "opens": g["sob"][0], "closes": g["sob"][1]})
    return out


def specjalne_ld(g, sklep=True):
    sp = []
    for d in D.NIEDZIELE_HANDLOWE:
        if d >= DZIS and g.get("nh"):
            sp.append({"@type": "OpeningHoursSpecification", "validFrom": d, "validThrough": d, "opens": g["nh"][0], "closes": g["nh"][1], "description": "Niedziela handlowa"})
    if sklep:
        for d, n in D.SWIETA.items():
            if d >= DZIS:
                sp.append({"@type": "OpeningHoursSpecification", "validFrom": d, "validThrough": d, "opens": "00:00", "closes": "00:00", "description": f"{n} - nieczynne"})
    return sorted(sp, key=lambda x: x["validFrom"])


def adres_ld(p):
    a = {"@type": "PostalAddress", "streetAddress": p["adres"], "addressLocality": "Kraków", "addressRegion": "małopolskie", "addressCountry": "PL"}
    if p.get("kod"):
        a["postalCode"] = p["kod"]
    return a


def placowka_ld(p, img_abs):
    typ = {"dh": "DepartmentStore", "sklep": "GroceryStore", "bar": "Restaurant"}[p["typ"]]
    d = {"@type": typ, "@id": B + "/" + path_pl(p) + "#placowka", "name": p["nazwa"], "url": B + "/" + path_pl(p),
         "parentOrganization": {"@id": ORG_ID}, "image": img_abs, "address": adres_ld(p),
         "geo": {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lng"]},
         "telephone": "+48 " + p["tel"], "openingHoursSpecification": godz_ld(p["godz"]),
         "specialOpeningHoursSpecification": specjalne_ld(p["godz"], sklep=p["typ"] != "bar"),
         "hasMap": f"https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lng']}"}
    if p["typ"] == "bar":
        d["servesCuisine"] = "Kuchnia polska"
        d["hasMenu"] = B + "/" + path_pl(p) + "#menu"
    else:
        d["paymentAccepted"] = "Gotówka, karta płatnicza, bony towarowe i podarunkowe HS Jubilat, Pluxee"
        d["currenciesAccepted"] = "PLN"
    return d


def org_ld():
    return {"@type": "Organization", "@id": ORG_ID, "name": D.FIRMA["nazwa"], "url": B + "/", "logo": B + "/assets/img/logo-jubilat.png",
            "address": {"@type": "PostalAddress", "streetAddress": D.FIRMA["ulica"], "postalCode": D.FIRMA["kod"], "addressLocality": "Kraków", "addressCountry": "PL"},
            "telephone": "+48 " + D.FIRMA["tel"], "email": D.FIRMA["email"], "taxID": D.FIRMA["nip"].replace("-", ""),
            "identifier": [{"@type": "PropertyValue", "propertyID": "KRS", "value": D.FIRMA["krs"]}, {"@type": "PropertyValue", "propertyID": "REGON", "value": D.FIRMA["regon"]}],
            "sameAs": [u for _, u in D.FIRMA["social"]]}


def okruszki_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": B + "/" + p} for i, (n, p) in enumerate(trail)]}


# ------------------------------------------------------------------ strona (kontekst ścieżek)
NAV = [("Sklepy i godziny", "sklepy/"), ("Dom Handlowy", "dom-handlowy/"), ("Bary mleczne", "bary-mleczne/"), ("Gazetka", "gazetka/"),
       ("Okazje", "okazje/"), ("Wynajem", "lokale-na-wynajem/"), ("Historia", "historia/")]
PANEL = [("Sklepy i godziny otwarcia", "sklepy/"), ("Dom Handlowy Jubilat", "dom-handlowy/"), ("Produkty unikatowe", "produkty-unikatowe/"),
         ("Bary mleczne Żaczek i Flisak", "bary-mleczne/"), ("Gazetka", "gazetka/"), ("Okazje, rabaty i aplikacja", "okazje/"),
         ("Niedziele handlowe i święta", "niedziele-handlowe/")]
PANEL2 = [("Aktualności", "aktualnosci/"), ("Praca", "praca/"), ("Lokale na wynajem", "lokale-na-wynajem/"), ("Historia", "historia/"), ("Kontakt", "kontakt/")]

STRONY = []  # (path, title) do sitemap


class P:
    def __init__(self, path):
        self.path = path  # '' = strona główna, 'sklepy/' itd.

    def a(self, target):
        up = self.path.count("/")
        r = "../" * up + target
        return r or "./"


def hash_pliku(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()[:8]


def typo(doc):
    """Twarde spacje po spójnikach jednoliterowych i skrótach (tylko w tekście, poza skryptami)."""
    czesci = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", doc, flags=re.S)
    for i, c in enumerate(czesci):
        if not c or c.startswith("<"):
            continue
        c = re.sub(r"(?<![\w&])([aiouwzAIOUWZ]|ul\.|al\.|nr|tel\.|pl\.) (?=\S)", lambda m: m.group(1) + " ", c)
        czesci[i] = c
    return "".join(czesci)


def okruszki(Pp, trail):
    li = '<li><a href="' + Pp.a("") + '">Strona główna</a></li>'
    for i, (n, p) in enumerate(trail):
        if i == len(trail) - 1:
            li += f'<li aria-current="page">{e(n)}</li>'
        else:
            li += f'<li><a href="{Pp.a(p)}">{e(n)}</a></li>'
    return f'<nav class="okruszki" aria-label="Okruszki"><ol>{li}</ol></nav>'


TEL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'


def dane_js():
    pl = []
    for p in D.PLACOWKI:
        x = {"id": p["id"], "typ": p["typ"], "n": p["krotka"], "lat": p["lat"], "lng": p["lng"], "g": p["godz"], "u": path_pl(p)}
        if p.get("dzialy"):
            x["dz"] = [d["godz"] for d in p["dzialy"]]
        pl.append(x)
    return {"pl": pl, "nh": D.NIEDZIELE_HANDLOWE, "sw": list(D.SWIETA.keys()), "skr": D.SKROCONE,
            "menu": {"od": D.MENU["od"], "do": D.MENU["do"]}}


DANE_JSON = json.dumps(dane_js(), ensure_ascii=False, separators=(",", ":"))


def strona(path, *, meta_slug=None, title=None, desc=None, body="", body_cls="", ld=None, mob=None, theme="#ffffff",
           og_img=None, preload_img="", nav_akt=None, fonts_el=False, noindex_extra=False, extra_head=""):
    Pp = P(path)
    m = META.get(meta_slug or ("/" + path), {})
    title = title or m.get("title")
    desc = desc or m.get("description")
    assert title and desc, path
    canon = B + "/" + path
    css_v, js_v = hash_pliku(ROOT / "assets/css/site.css"), hash_pliku(ROOT / "assets/js/site.js")
    og = B + "/" + (og_img or "assets/img/og-jubilat.jpg")
    robots = '<meta name="robots" content="noindex, nofollow">' if (D.PREVIEW or noindex_extra) else ""
    graph = [g for g in (ld or []) if g]
    ld_html = f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>' if graph else ""
    pre = (f'<link rel="preload" href="{Pp.a("assets/fonts/hanken.woff2")}" as="font" type="font/woff2" crossorigin>'
           f'<link rel="preload" href="{Pp.a("assets/fonts/newsreader.woff2")}" as="font" type="font/woff2" crossorigin>')
    if fonts_el:
        pre += f'<link rel="preload" href="{Pp.a("assets/fonts/inria-regular.woff2")}" as="font" type="font/woff2" crossorigin>'
    nav = "".join(f'<a href="{Pp.a(u)}"{" aria-current=" + chr(34) + "page" + chr(34) if nav_akt == u else ""}>{n}</a>' for n, u in NAV)
    panel = "".join(f'<a href="{Pp.a(u)}"{" aria-current=" + chr(34) + "page" + chr(34) if nav_akt == u else ""}>{n}</a>' for n, u in PANEL)
    panel2 = "".join(f'<a href="{Pp.a(u)}">{n}</a>' for n, u in PANEL2)
    el_akt = ' aria-current="page"' if nav_akt == "eleganza/" else ""
    mob = mob or ("Godziny otwarcia", "sklepy/")
    mob_tel = mob[2] if len(mob) > 2 else D.FIRMA["tel"]
    wyk = (f' <a class="st-wyk" href="{D.WYKONANIE["url"]}" rel="noopener">{e(D.WYKONANIE["tekst"])}</a>' if D.WYKONANIE else "")
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in D.FIRMA["social"])
    test = '<p class="st-test">Wersja testowa strony. Po odbiorze treści przeniesiemy do panelu WordPress.</p>' if D.TEST_NOTES else ""
    doc = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
{robots}
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL"><meta property="og:site_name" content="Jubilat">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="{Pp.a("assets/img/favicon-32.png")}" sizes="32x32"><link rel="apple-touch-icon" href="{Pp.a("assets/img/apple-touch-icon.png")}">
{pre}{preload_img}
<link rel="stylesheet" href="{Pp.a("assets/css/site.css")}?v={css_v}">
{extra_head}{ld_html}
</head>
<body{(" class=" + chr(34) + body_cls + chr(34)) if body_cls else ""}>
<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="{Pp.a("")}" aria-label="Jubilat - strona główna"><img src="{Pp.a("assets/img/logo-jubilat.webp")}" width="306" height="74" alt="Jubilat Handlowa Spółdzielnia"></a>
    <a class="top-el" href="{Pp.a("eleganza/")}"{el_akt}><img src="{Pp.a("assets/img/eleganza-znak-bordo.webp")}" width="183" height="242" alt="">Eleganza</a>
    <nav class="menu" aria-label="Menu główne">{nav}</nav>
    <a class="top-tel" href="{tel_href(D.FIRMA["tel"])}" aria-label="Zadzwoń: {D.FIRMA["tel"]}">{TEL_SVG}<span>{D.FIRMA["tel"]}</span></a>
    <button class="burger" type="button" aria-label="Otwórz menu" aria-expanded="false" aria-controls="panel"><span></span><span></span></button>
  </div>
</header>
<div class="panel" id="panel" hidden>
  <nav aria-label="Menu mobilne"><a class="panel-el" href="{Pp.a("eleganza/")}">Salon Eleganza</a>{panel}</nav>
  <nav class="panel-grupa" aria-label="Spółdzielnia">{panel2}</nav>
  <p class="panel-kontakt">al. Krasińskiego 1, 31-111 Kraków<br><a href="{tel_href(D.FIRMA["tel"])}">{D.FIRMA["tel"]}</a> · <a href="mailto:{D.FIRMA["email"]}">{D.FIRMA["email"]}</a></p>
</div>
<main id="tresc">
{body}
</main>
<footer class="stopka">
  <div class="wrap">
    <div class="st-gora">
      <div>
        <a class="st-marka" href="{Pp.a("")}"><img src="{Pp.a("assets/img/znak-96.png")}" width="48" height="48" alt="" loading="lazy">Handlowa Spółdzielnia<br>JUBILAT</a>
        <p class="st-adres">al. Zygmunta Krasińskiego 1<br>31-111 Kraków<br><a href="{tel_href(D.FIRMA["tel"])}">{D.FIRMA["tel"]}</a><br><a href="mailto:{D.FIRMA["email"]}">{D.FIRMA["email"]}</a></p>
      </div>
      <div><h2>Zakupy</h2><ul>
        <li><a class="st-el" href="{Pp.a("eleganza/")}">Salon Eleganza</a></li>
        <li><a href="{Pp.a("sklepy/")}">Sklepy i godziny</a></li><li><a href="{Pp.a("dom-handlowy/")}">Dom Handlowy</a></li>
        <li><a href="{Pp.a("produkty-unikatowe/")}">Produkty unikatowe</a></li><li><a href="{Pp.a("bary-mleczne/")}">Bary mleczne</a></li>
        <li><a href="{Pp.a("gazetka/")}">Gazetka</a></li><li><a href="{Pp.a("okazje/")}">Okazje i aplikacja</a></li>
        <li><a href="{Pp.a("niedziele-handlowe/")}">Niedziele handlowe</a></li></ul></div>
      <div><h2>Spółdzielnia</h2><ul>
        <li><a href="{Pp.a("aktualnosci/")}">Aktualności</a></li><li><a href="{Pp.a("praca/")}">Praca</a></li>
        <li><a href="{Pp.a("lokale-na-wynajem/")}">Lokale na wynajem</a></li><li><a href="{Pp.a("historia/")}">Historia</a></li>
        <li><a href="{Pp.a("kontakt/")}">Kontakt</a></li></ul></div>
      <div><h2>Obserwuj nas</h2><ul>{social}</ul></div>
    </div>
    <div class="st-dol">
      <p><span>© Handlowa Spółdzielnia JUBILAT w Krakowie</span><a href="{Pp.a("polityka-prywatnosci/")}">Polityka prywatności</a></p>
      <p>{wyk}</p>
    </div>
    {test}
  </div>
</footer>
<div class="mob" id="mob">
  <a class="mob-tel" href="{tel_href(mob_tel)}">{TEL_SVG}Zadzwoń</a>
  <a class="mob-cta" href="{mob[1] if mob[1].startswith(("#", "http")) else Pp.a(mob[1])}"{" target=" + chr(34) + "_blank" + chr(34) + " rel=" + chr(34) + "noopener" + chr(34) if mob[1].startswith("http") else ""}>{mob[0]}</a>
</div>
<script id="dane" type="application/json">{DANE_JSON}</script>
<script src="{Pp.a("assets/js/site.js")}?v={js_v}" defer data-root="{Pp.a("")}"></script>
</body>
</html>
'''
    doc = re.sub(r"\n\s*\n", "\n", doc)
    doc = typo(doc)
    f = ROOT / (path + "index.html") if not path.endswith(".html") else ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc, encoding="utf-8")
    if not noindex_extra and not path.endswith(".html"):
        STRONY.append(path)
    return Pp


def ph(Pp, trail, h1, lead="", meta_html="", foto=None, foto_alt="", foto_cap="", st_id=None):
    st = f'<p class="st" data-st="{st_id}"></p>' if st_id else ""
    tekst = f'<div class="ph-in">{okruszki(Pp, trail)}<h1{" class=" + chr(34) + "h1-dl" + chr(34) if len(html.unescape(h1)) > 44 else ""}>{h1}</h1>' + (f'<p class="ph-lead">{lead}</p>' if lead else "") + st + (f'<div class="ph-meta">{meta_html}</div>' if meta_html else "") + "</div>"
    if foto:
        cap = f"<figcaption>{e(foto_cap)}</figcaption>" if foto_cap else ""
        return f'<section class="ph ph-foto">{tekst}<figure>{pic(Pp, foto, foto_alt, sizes="(max-width: 760px) 100vw, 55vw", lazy=False, prio=True)}{cap}</figure></section>'
    return f'<section class="ph">{tekst}</section>'


def preload_hero(Pp, info, sizes="(max-width: 760px) 100vw, 55vw"):
    ss = ", ".join(f"{Pp.a('assets/img/' + info['key'] + '-' + str(w) + '.avif')} {w}w" for w in info["ws"])
    return f'<link rel="preload" as="image" type="image/avif" imagesrcset="{ss}" imagesizes="{sizes}" fetchpriority="high">'


# ------------------------------------------------------------------ zasoby stałe
def zasoby():
    # logo, znak, favikony, logotypy Eleganzy
    lg = Image.open(WIZ / "logo.webp").convert("RGBA")
    lg.save(OUT_IMG / "logo-jubilat.webp", quality=92); lg.save(OUT_IMG / "logo-jubilat.png")
    zn = Image.open(WIZ / "znak.png").convert("RGBA")
    for s, n in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (96, "znak-96.png")]:
        zn.resize((s, s), Image.LANCZOS).save(OUT_IMG / n)
    zn.resize((96, 96), Image.LANCZOS).save(OUT_IMG / "znak.png")
    shutil.copy(WIZ / "eleganza" / "znak-bordo.webp", OUT_IMG / "eleganza-znak-bordo.webp")
    for n in ["logo-bialy.webp", "logo-bordo.webp", "znak-bialy.webp"]:
        shutil.copy(WIZ / "eleganza" / n, OUT_IMG / ("eleganza-" + n))
    md = OUT_IMG / "marki"; md.mkdir(exist_ok=True)
    for k, *_ in D.MARKI:
        s = WIZ / "eleganza" / "marki" / f"{k}.webp"
        if s.exists():
            shutil.copy(s, md / f"{k}.webp")
    # obraz OG
    og = Image.open(WIZ / "dh.jpg").convert("RGB")
    w, h = og.size; nh_ = round(w * 630 / 1200); y = round((h - nh_) * .35)
    og.crop((0, y, w, y + nh_)).resize((1200, 630), Image.LANCZOS).save(OUT_IMG / "og-jubilat.jpg", quality=82)
    el = Image.open(WIZ / "eleganza" / "lb" / "schody.jpg").convert("RGB")
    w, h = el.size; nh_ = round(w * 630 / 1200); y = round((h - nh_) * .45)
    el.crop((0, y, w, y + nh_)).resize((1200, 630), Image.LANCZOS).save(OUT_IMG / "og-eleganza.jpg", quality=82)
    # gazetka: PDF + podglądy stron
    gd = ROOT / "assets" / "pdf"; gd.mkdir(parents=True, exist_ok=True)
    shutil.copy(LIVE / "gazetka_10.pdf", gd / D.GAZETKA["plik"])
    import fitz
    doc = fitz.open(LIVE / "gazetka_10.pdf")
    tmp = SRC / "_tmp_gaz"; tmp.mkdir(exist_ok=True)
    for i in range(doc.page_count):
        f = tmp / f"s{i + 1}.png"
        if not f.exists():
            doc[i].get_pixmap(dpi=110).save(f)
    # regulamin aplikacji jako PDF (z grafik stron ze starej strony)
    reg = gd / "regulamin-aplikacji-jubilat.pdf"
    if not reg.exists():
        ims = []
        for i in range(6):
            im = Image.open(RAW / f"85c51dd1be22c0d187d37f23ba9815cf-{i}-1.webp").convert("RGB")
            ims.append(im.resize((1240, round(im.height * 1240 / im.width)), Image.LANCZOS))
        ims[0].save(reg, save_all=True, append_images=ims[1:], resolution=150, quality=80)


# ------------------------------------------------------------------ fragmenty wspólne
def lista_placowek(Pp, tylko=None):
    items = []
    for p in D.PLACOWKI:
        if tylko and p["typ"] not in tylko:
            continue
        kw = foto_pl(p, "kw")
        rodzaj = {"dh": "Dom handlowy", "sklep": "Sklep spożywczo-przemysłowy", "bar": "Bar mleczny"}[p["typ"]]
        nazwa = p["nazwa"] if p["typ"] in ("dh", "bar") else p["krotka"]
        adr = f'<p class="pl-dod">{e(p["adres"])}{", " + p["kod"] + " Kraków" if p.get("kod") else ""}</p>' if p["typ"] in ("dh", "bar") else ""
        dod = ""
        tab = f'<table>{tabela_mini(p["godz"], "Stoisko spożywcze" if p.get("dzialy") else None)}'
        if p.get("dzialy"):
            dod = f'<p class="pl-dod" data-st="dh:1" data-st-pre="HOME i Eleganza: "></p>'
            tab += tabela_mini(p["dzialy"][1]["godz"], "HOME i Salon Eleganza")
        tab += "</table>"
        typ_f = "sklep" if p["typ"] in ("dh", "sklep") else "bar"
        items.append(f'''<li class="pl" id="pl-{p["id"]}" data-id="{p["id"]}" data-typ="{typ_f}">
<a class="pl-foto-a" href="{Pp.a(path_pl(p))}" tabindex="-1" aria-hidden="true">{pic(Pp, kw, "", sizes="96px", img_cls="pl-foto")}</a>
<div class="pl-tresc"><p class="pl-rodzaj">{rodzaj}</p><h3><a href="{Pp.a(path_pl(p))}">{e(nazwa)}</a></h3>{adr}
<p class="pl-status" data-st="{p["id"]}"></p>{dod}
<div class="pl-akcje"><a class="tel" href="{tel_href(p["tel"])}">{p["tel"]}</a><a href="{prowadz(p)}" target="_blank" rel="noopener">Prowadź</a><button type="button" class="pokaz-godz" aria-expanded="false">Godziny</button></div>
<div class="godz" hidden>{tab}</div></div></li>''')
    return "".join(items)


def sekcja_placowek(Pp, naglowek_h="h2", tytul="Gdzie i do której otwarte", opis="", link=True):
    cnt_all, cnt_s, cnt_b = len(D.PLACOWKI), len(SKLEPY) + 1, 2
    opis = opis or "Status liczymy na bieżąco, razem z niedzielami handlowymi i świętami. Dotknij numeru, żeby zadzwonić, albo „Prowadź”, żeby wyznaczyć trasę."
    link_html = f'<p class="sek-stopka"><a class="link-dalej" href="{Pp.a("niedziele-handlowe/")}">Niedziele handlowe i święta</a></p>' if link else ""
    return f'''<div class="sek-glowa"><{naglowek_h}>{tytul}</{naglowek_h}><p>{opis}</p></div>
<div class="filtry" role="toolbar" aria-label="Filtry placówek">
  <div class="seg" role="group" aria-label="Rodzaj placówki">
    <button type="button" class="on" data-f="all" aria-pressed="true">Wszystkie <b>{cnt_all}</b></button>
    <button type="button" data-f="sklep" aria-pressed="false">Sklepy <b>{cnt_s}</b></button>
    <button type="button" data-f="bar" aria-pressed="false">Bary <b>{cnt_b}</b></button>
  </div>
  <label class="przel"><input type="checkbox" id="tylkoOtw"> <span>Tylko otwarte teraz</span></label>
  <button class="btn btn-linia btn-geo" id="geoBtn" type="button"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>Najbliżej mnie</button>
</div>
<p class="geo-info" id="geoInfo" hidden></p>
<div class="pl-uklad">
  <div class="mapa-box"><div id="mapa" data-mapa="all" role="region" aria-label="Mapa placówek Jubilat"><p class="mapa-zast">Mapa wczyta się po przewinięciu.</p></div></div>
  <ol class="lista" id="lista">{lista_placowek(Pp)}</ol>
</div>
<p class="pusto-info" id="pustoInfo" hidden>Teraz żadna placówka z tej grupy nie jest otwarta. Wyłącz filtr „Tylko otwarte teraz”, żeby zobaczyć godziny.</p>
<p class="pieczywo"><b>Nie marnuj pieczywa:</b> codziennie od 19:00 do zamknięcia pieczywo 10% taniej we wszystkich sklepach sieci Jubilat.</p>{link_html}'''


def pietra_html(Pp, linki=True):
    d = DH["dzialy"]
    el_h = f'<a class="p-el" href="{Pp.a("eleganza/")}">Salon Eleganza</a>' if linki else '<span class="p-el">Salon Eleganza</span>'
    g = lambda x: f'pn-pt {zakres(x["pt"])}<br>sob {zakres(x["sob"])}<br>niedz. handlowa {zakres(x["nh"])}'
    return f'''<ol class="pietra">
<li class="p-el-wiersz"><span class="p-poz">II-III piętro</span><div class="p-tresc"><h3>{el_h}</h3><p class="p-haslo">Prawdziwy luksus szyty w Polsce</p>
<p>Odzież damska, męska i dziecięca, obuwie i galanteria, a także tekstylia, walizki, artykuły szkolno-biurowe i zabawki. 95% asortymentu od polskich producentów.</p>
<p class="marki">{", ".join(n for _, n, *_ in D.MARKI)}</p></div><p class="p-godz">{g(d[2]["godz"])}</p></li>
<li><span class="p-poz">I piętro</span><div class="p-tresc"><h3>Stoisko HOME ze strefą Beauty</h3>
<p>Drobne AGD, żarówki, baterie i przedłużacze, rzeczy do kuchni i łazienki, w większości od polskich producentów. W strefie Beauty kosmetyki do makijażu i pielęgnacji, akcesoria do domowego SPA i kosmetyki lokalnych manufaktur, między innymi krakowskiej La-Le.</p></div><p class="p-godz">{g(d[1]["godz"])}</p></li>
<li><span class="p-poz">Parter</span><div class="p-tresc"><h3>Sklep spożywczy z delikatesami</h3>
<p>Pieczywo i ciasta, nabiał z małych mleczarni, mięso i wędliny, owoce i warzywa, <a class="link-w" href="{Pp.a("produkty-unikatowe/")}">produkty unikatowe</a>. Opłacisz tu rachunki, wypłacisz gotówkę (cashback), zapłacisz kartą lub bonami Pluxee.</p></div><p class="p-godz">{g(d[0]["godz"])}</p></li>
</ol>'''


def polka_html(Pp, ile=None):
    out = ""
    for k, n, pr, wag, cena in D.PRODUKTY[:ile]:
        info = przygotuj("p-" + k, WIZ / f"p-{k}.jpg", [220, 440])
        out += f'<li class="prod">{pic(Pp, info, n, sizes="(max-width: 760px) 42vw, 220px")}<div class="prod-in"><p class="cena">{cena} zł</p><h3>{e(n)}</h3><p>{e(pr)}, {wag}</p></div></li>'
    return f'<ul class="polka" id="polka">{out}</ul>'


def menu_lista(bar, krotko=False):
    dni = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
    od = datetime.date.fromisoformat(D.MENU["od"])
    out = ""
    for i, (z, d2, c) in enumerate(D.MENU[bar]):
        dt = od + datetime.timedelta(days=i)
        if krotko:
            out += f'<li data-dzien="{i + 1}"><span class="md">{dni[i]}, {dt.day}.{dt.month:02d}</span><span>{e(z)}, {e(d2[0].lower() + d2[1:])}</span><span class="mc">{c} zł</span></li>'
        else:
            out += f'<li data-dzien="{i + 1}"><span class="md">{dni[i]}<small>{dt.day} {MIES[dt.month - 1]}</small></span><span class="mz">{e(z)}<span>{e(d2)}</span></span><span class="mc">{c} zł</span></li>'
    return out


def menu_zakres():
    a, b = datetime.date.fromisoformat(D.MENU["od"]), datetime.date.fromisoformat(D.MENU["do"])
    return f"{a.day}-{b.day} {MIES[b.month - 1]} {b.year}" if a.month == b.month else f"{a.day} {MIES[a.month - 1]} - {b.day} {MIES[b.month - 1]} {b.year}"


def bar_karta(Pp, p, h="h3"):
    info = foto_pl(p)
    m = D.MENU[p["id"]]
    naj = min(m, key=lambda x: float(x[2].replace(",", ".")))[2]
    dow = " ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' if False else f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in p["dowoz"])
    dow = ", ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in p["dowoz"])
    g = p["godz"]
    gtxt = f'pn-pt {zakres(g["pt"])}' + (f', sob {zakres(g["sob"])}' if g["sob"] else ", sobota nieczynne") + ", niedziela nieczynne"
    return f'''<article class="bar">
<a href="{Pp.a(path_pl(p))}" tabindex="-1" aria-hidden="true">{pic(Pp, info, alt_pl(p), sizes="(max-width: 760px) 100vw, 50vw", img_cls="bar-foto")}</a>
<{h}><a href="{Pp.a(path_pl(p))}">{e(p["nazwa"].replace("Bar mleczny ", "Bar "))}</a></{h}>
<p class="bar-adr">{e(p["adres"])}, {p["kod"]} Kraków</p>
<p class="bar-status" data-st="{p["id"]}"></p>
<div class="dzis" data-menu-dzis="{p["id"]}"><p class="dzis-tyt">Zestaw zupa i drugie danie</p><p class="dzis-danie">w menu tygodnia {menu_zakres()} od {naj} zł</p></div>
<details class="menu-tyg"><summary>Menu tygodnia {menu_zakres()}</summary><ul data-menu="{p["id"]}">{menu_lista(p["id"], True)}</ul></details>
<p class="bar-godz">{gtxt}</p>
<div class="bar-akcje"><a class="btn btn-ciem" href="{tel_href(p["tel"])}">Zadzwoń: {p["tel"]}</a><a class="btn btn-linia" href="{Pp.a(path_pl(p))}">Menu i dojazd</a></div>
<p class="dowoz">Z dowozem: {dow}</p>
</article>'''


def gaz_status():
    G = D.GAZETKA
    if DZIS > G["do"]:
        return "Oferta zakończona " + data_pl(G["do"], False) + ". Nowa gazetka pojawi się tu wkrótce."
    if DZIS < G["od"]:
        return "Gazetka zacznie obowiązywać wkrótce."
    return "Gazetka aktualna, ważna do " + data_pl(G["do"], False) + "."


def okazje_html(Pp, cls="okazje-lista"):
    out = ""
    for o in D.OKAZJE:
        info = przygotuj(o["img"], WIZ / f"{o['img']}.jpg", [380])
        out += (f'<li class="ok" data-od="{o["od"]}" data-do="{o["do"]}">{pic(Pp, info, o["nazwa"], sizes="(max-width: 760px) 45vw, 230px")}'
                f'<div class="ok-in"><p class="cena">{o["cena"]} <small>{o["jedn"]}</small></p><h3 class="ok-h">{e(o["nazwa"])}</h3>'
                f'<p>Najniższa cena z 30 dni: {o["min30"]}</p><p class="ok-daty">{data_kr(o["od"])[:5]}-{data_kr(o["do"])}</p></div></li>')
    return f'<ul class="{cls}" data-pusto="brakOkazji">{out}</ul><p class="brak-okazji" id="brakOkazji" hidden>Nowe okazje pojawią się tu wkrótce. Zajrzyj do <a class="link" href="{Pp.a("gazetka/")}">gazetki</a>.</p>'


def test_uw(txt):
    return f'<p class="test-uw"><b>Wersja testowa:</b> {txt}</p>' if D.TEST_NOTES else ""


def komunikaty_html(Pp):
    items = ""
    for k in D.KOMUNIKATY:
        link = f' <a href="{Pp.a(k["link"][1])}">{k["link"][0]}</a>' if k.get("link") else ""
        items += f'<p data-od="{k["od"]}" data-do="{k["do"]}"{" hidden" if not (k["od"] <= DZIS <= k["do"]) else ""}>{e(k["tekst"])}{link}</p>'
    return f'<aside class="kom" aria-label="Komunikaty"><div class="kom-in">{items}</div></aside>'


def akt_lista(Pp, lst, h="h2", skrot=False):
    out = ""
    for a in lst:
        logo = ""
        if not skrot:
            if a.get("img"):
                logo = f'<a class="akt-logo" href="{Pp.a("aktualnosci/" + a["slug"] + "/")}" tabindex="-1" aria-hidden="true"><img src="{Pp.a("assets/img/marki/" + a["img"] + ".webp")}" alt="" loading="lazy"></a>'
            else:
                logo = "<span></span>"
        out += (f'<li class="akt"><p class="akt-data"><b>{data_kr(a["data"])}</b>{e(a["kat"])}</p><div><{h}><a href="{Pp.a("aktualnosci/" + a["slug"] + "/")}">{e(a["tytul"])}</a></{h}>'
                f'<p>{e(skroc(a["tresc"][0], 170))}</p></div>{logo}</li>')
    return f'<ol class="akt-lista{" akt-skrot" if skrot else ""}">{out}</ol>'


def skroc(t, n):
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:-") + "…"


# ================================================================== STRONY
def s_home():
    Pp = P("")
    dh = foto_pl(DH)
    co = f'''<ul class="hero-co">
<li><a href="{Pp.a("dom-handlowy/")}"><span>Parter</span><b>Duży sklep spożywczy z&nbsp;delikatesami</b></a></li>
<li><a href="{Pp.a("dom-handlowy/")}"><span>I piętro</span><b>Stoisko gospodarcze HOME i&nbsp;Beauty</b></a></li>
<li class="hero-co-el"><a href="{Pp.a("eleganza/")}"><span>II-III piętro</span><b>Salon Eleganza</b></a></li>
<li><a href="{Pp.a("sklepy/")}"><span>Osiedla</span><b>8 sklepów w&nbsp;Krakowie</b></a></li>
<li><a href="{Pp.a("bary-mleczne/")}"><span>Obiady</span><b>Bary mleczne Żaczek i&nbsp;Flisak</b></a></li></ul>'''
    el_f = [przygotuj("lb-" + k, WIZ / "eleganza" / "lb" / f"{k}.jpg", [360, 533]) for k in ("k56", "k16", "k13")]
    el_alt = ["Kobieta w bordowym komplecie i płaszczu z kolekcji jesień-zima Salonu Eleganza", "Para w granatowym garniturze i czarnej sukience koktajlowej", "Kobaltowy komplet z żakietem z baskinką"]
    el_imgs = "".join(pic(Pp, f, a, sizes="(max-width: 760px) 50vw, 20vw") for f, a in zip(el_f, el_alt))
    gaz = przygotuj("gazetka-okladka", SRC / "_tmp_gaz" / "s1.png", [300, 600, 900])
    sala = przygotuj("sala", RAW / "IMG_1333-edited-scaled.webp", [600, 1000, 1600])
    hist = "".join(f'<li><span class="rok">{r}</span><p>{e(t)}</p></li>' for r, t in D.HISTORIA)
    body = f'''<section class="hero">
  <figure class="hero-foto">{pic(Pp, dh, FOTO_ALT["dh"], sizes="(max-width: 760px) 100vw, 58vw", lazy=False, prio=True)}<figcaption>Dom Handlowy Jubilat, otwarty w 1969 r.</figcaption></figure>
  <div class="hero-in">
    <p class="hero-adres">al. Krasińskiego 1, przy moście Dębnickim</p>
    <h1>Dom Handlowy Jubilat, sklepy i&nbsp;bary mleczne w&nbsp;Krakowie</h1>
    {co}
    <div class="hero-cta"><a class="btn btn-ciem" href="{Pp.a("sklepy/")}">Godziny i mapa sklepów</a></div>
    <p class="teraz" id="teraz" aria-live="polite"><span class="kropka"></span><span id="terazTxt">Sprawdzamy godziny otwarcia…</span></p>
  </div>
</section>
{komunikaty_html(Pp)}
<section class="el-baner" aria-labelledby="elBanerTyt">
  <div class="el-baner-in">
    <div class="el-baner-tekst">
      <img class="el-baner-logo" src="{Pp.a("assets/img/eleganza-logo-bialy.webp")}" width="727" height="466" loading="lazy" alt="Eleganza - świat dobrych ubrań">
      <h2 id="elBanerTyt">Prawdziwy luksus szyty w&nbsp;Polsce</h2>
      <p>Odzież damska, męska i dziecięca, obuwie i galanteria na II i III piętrze Domu Handlowego. 95% kolekcji pochodzi od polskich producentów, m.in. Domu Mody Skórska, Ferii, Red Button i Michy.</p>
      <a class="btn el-btn" href="{Pp.a("eleganza/")}">Zobacz kolekcję jesień-zima</a>
      <p class="el-baner-godz">II-III piętro. Pn-pt 9:00-20:00, sob 9:00-19:00</p>
    </div>
    <div class="el-baner-foto">{el_imgs}</div>
  </div>
</section>
<section class="sek placowki" id="placowki"><div class="wrap">{sekcja_placowek(Pp)}</div></section>
<section class="sek dh" id="dom-handlowy"><div class="wrap">
  <div class="sek-glowa"><h2>Dom Handlowy Jubilat</h2><p>Około 6 800 m² nad zakolem Wisły, niedaleko Wawelu. Pełny wybór artykułów spożywczych i przemysłowych znanych producentów, a obok nasze stoiska handlowe i usługowe firm. Telefon do Domu Handlowego: <a href="tel:+48126193300">12 619 33 00</a>.</p></div>
  {pietra_html(Pp)}
  <p class="sek-stopka"><a class="link-dalej" href="{Pp.a("dom-handlowy/")}">Piętra, usługi i dojazd</a></p>
</div></section>
<section class="sek produkty" id="produkty"><div class="wrap">
  <div class="sek-glowa sek-glowa-row"><div><h2>Produkty unikatowe</h2><p>Nabiał z małych mleczarni, ręcznie robione łazanki i pierogi, miody, syropy i herbaty. Ceny z jubilat.com.pl, stan na {D.PRODUKTY_STAN}.</p></div>
  <div class="strzalki"><button type="button" data-kier="-1" aria-label="Przewiń produkty w lewo">‹</button><button type="button" data-kier="1" aria-label="Przewiń produkty w prawo">›</button></div></div>
  {polka_html(Pp)}
  <p class="sek-stopka"><a class="link-dalej" href="{Pp.a("produkty-unikatowe/")}">Wszystkie produkty unikatowe</a></p>
</div></section>
<section class="sek bary" id="bary"><div class="wrap">
  <div class="sek-glowa"><h2>Bary mleczne Żaczek i Flisak</h2><p>Domowe obiady w dni powszednie. Zestaw zupa i drugie danie w menu tygodnia {menu_zakres()}. Zamówisz też z dowozem przez Wolt, Bolt Food i Glovo.</p></div>
  <div class="bary-uklad">{"".join(bar_karta(Pp, b) for b in BARY)}</div>
</div></section>
<section class="sek gazetka" id="gazetka"><div class="wrap gaz-uklad">
  <div class="gaz-okladka">
    <a href="{Pp.a("gazetka/")}">{pic(Pp, gaz, "Okładka gazetki Domu Handlowego Jubilat: Jesienne okazje", sizes="(max-width: 760px) 44vw, 300px")}</a>
    <div><h2>Gazetka</h2><p>{e(D.GAZETKA["tytul"])}, oferta ważna od {data_kr(D.GAZETKA["od"])[:5]} do {data_kr(D.GAZETKA["do"])} r.</p><p class="st" data-gazetka data-gaz-od="{D.GAZETKA['od']}" data-gaz-do="{D.GAZETKA['do']}">{gaz_status()}</p>
    <a class="btn btn-linia" href="{Pp.a("gazetka/")}">Przeglądaj gazetkę</a></div>
  </div>
  <div class="okazje">
    <h3>Okazje z aplikacji</h3>
    <p class="okazje-opis">Ceny dla klientów z aplikacją Jubilat albo kartą lojalnościową Społem lub Jubilat. Obok najniższa cena z ostatnich 30 dni.</p>
    {okazje_html(Pp)}
    <p class="przypis">Najniższe ceny z 30 dni podano ze stoiska spożywczego DH Jubilat, al. Krasińskiego 1. <a class="link" href="{Pp.a("okazje/")}">Okazje, rabaty i aplikacja</a></p>
    {test_uw("produkty i ceny z okazji 20-26.10.2026, daty ustawione przykładowo, żeby pokazać, jak karty same pojawiają się i znikają w podanym terminie.")}
  </div>
</div></section>
<section class="sek aplikacja" id="aplikacja"><div class="wrap app-uklad">
  <div class="app-tekst"><h2>Aplikacja Jubilat</h2>
    <ul class="app-lista"><li>Za każde wydane 10 zł dostajesz 1 punkt, a na start 100 punktów.</li><li>Punkty wymieniasz na e-bony o wartości 5, 20 i 40 zł.</li><li>Punkty zbierasz w sklepach Jubilat, w Salonie Eleganza, na stoisku HOME oraz w barach Flisak i Żaczek.</li><li>Masz dostęp do okazji i akcji specjalnych w całej sieci.</li></ul>
    {app_przyciski()}
    <p class="app-pomoc">Pomoc w sprawie aplikacji: <a href="tel:+48780191172">780 191 172</a>, pn-pt 7:00-15:00.</p></div>
  <div class="rabaty"><h3>3% rabatu dla krakowskich rodzin</h3><p>Posiadacze kart Krakowska Duża Rodzina, Rodzina 3+ oraz Krakowskie Rodziny z Niepełnosprawnym Dzieckiem dostają 3% rabatu we wszystkich naszych sklepach. Wystarczy pokazać kartę przy kasie.</p>
    <p class="male">Rabat od zakupów za min. 5 zł. Nie obejmuje alkoholu, wyrobów tytoniowych, prasy, doładowań telefonicznych oraz toreb.</p>
    <h3>Bony towarowe dla firm</h3><p>Bony o nominałach 10, 20 i 50 zł do wykorzystania w DH Jubilat i sklepach sieci. Zamówienia: <a href="mailto:marketing@jubilat.com.pl">marketing@jubilat.com.pl</a>.</p></div>
</div></section>
<section class="sek akt-sek" id="aktualnosci"><div class="wrap dwie dwie-75">
  <div><div class="sek-glowa"><h2>Aktualności</h2></div>{akt_lista(Pp, D.AKTUALNOSCI[:3], h="h3", skrot=True)}<p class="sek-stopka"><a class="link-dalej" href="{Pp.a("aktualnosci/")}">Wszystkie aktualności</a></p></div>
  <div class="wyn-teaser"><figure class="wyn-foto">{pic(Pp, sala, "Sala konferencyjna w Domu Handlowym Jubilat", sizes="(max-width: 1060px) 100vw, 40vw")}</figure>
    <h2>Sala i lokale na wynajem</h2><p>Sala konferencyjna do 80 miejsc, biura, lokal użytkowy przy ul. Machaya 1 i magazyny.</p>
    <p class="sek-stopka"><a class="link-dalej" href="{Pp.a("lokale-na-wynajem/")}">Oferta wynajmu</a></p>
    <h2 class="praca-h">Praca w Jubilacie</h2><p>Szukamy m.in. kierownika sklepu, zastępcy kierownika i kasjerów-sprzedawców.</p>
    <p class="sek-stopka"><a class="link-dalej" href="{Pp.a("praca/")}">Oferty pracy</a></p></div>
</div></section>
<section class="sek historia" id="historia"><div class="wrap hist-uklad">
  <div class="hist-intro"><h2>Historia</h2><p>Jubilat to modernistyczna plomba u zbiegu ul. Zwierzynieckiej i al. Krasińskiego. Dwie przeszklone kondygnacje parteru, wysunięte piętra handlowe w ścianie kurtynowej, nad nimi dekoracyjny raster elewacji, a na dachu neon z nazwą.</p>
    <figure class="znak"><img src="{Pp.a("assets/img/znak-96.png")}" width="72" height="72" alt="Znak firmowy Jubilat: skrzydełko z czapki Merkurego" loading="lazy"><figcaption>Nasz znak to stylizowane skrzydełko z czapki Merkurego, patrona kupców.</figcaption></figure>
    <p class="sek-stopka"><a class="link-dalej" href="{Pp.a("historia/")}">Cała historia</a></p></div>
  <ol class="os">{hist}</ol>
</div></section>
{faq_html("home")}
{kontakt_sek(Pp)}'''
    wsite = {"@type": "WebSite", "@id": B + "/#website", "url": B + "/", "name": "Jubilat", "inLanguage": "pl-PL", "publisher": {"@id": ORG_ID}}
    strona("", meta_slug="/", body=body, ld=[org_ld(), wsite, placowka_ld(DH, B + "/" + url_img(dh)), faq_ld("home")], mob=("Godziny otwarcia", "sklepy/"),
           preload_img=preload_hero(Pp, dh, "(max-width: 760px) 100vw, 58vw"))


def app_przyciski():
    return '''<div class="sklepy-app">
<a class="app-btn" href="https://apps.apple.com/app/6756414653" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.6c0-2.4 2-3.5 2-3.6-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.2-2.8.8-3.5.8-.7 0-1.8-.8-3-.8A4.5 4.5 0 0 0 4.7 9.5c-1.6 2.8-.4 6.9 1.1 9.2.8 1.1 1.7 2.3 2.9 2.3 1.1-.1 1.6-.8 3-.8s1.8.8 3 .7c1.2 0 2-1.1 2.8-2.2.9-1.3 1.2-2.5 1.2-2.6 0 0-2.3-.9-2.3-3.5zM14.1 5.6c.6-.8 1.1-1.8 1-2.9-.9 0-2.1.6-2.7 1.4-.6.7-1.1 1.8-1 2.8 1 .1 2-.5 2.7-1.3z"/></svg><span><small>Pobierz z</small>App Store</span></a>
<a class="app-btn" href="https://play.google.com/store/apps/details?id=pl.loyaltyclub.spolemjubilat" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2.8 13.6 12 4 21.2c-.3-.2-.5-.6-.5-1V3.8c0-.4.2-.8.5-1zm10.7 10.3 2.3 2.2-10.6 6 8.3-8.2zm3.6-3.4 2.7 1.5c.7.4.7 1.4 0 1.8l-2.7 1.5-2.6-2.5 2.6-2.3zM6.4 2.7l10.6 6-2.3 2.2-8.3-8.2z"/></svg><span><small>Pobierz z</small>Google Play</span></a></div>'''


def kontakt_sek(Pp, el=False):
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in D.FIRMA["social"])
    salon = '<div><dt>Salon</dt><dd><a href="tel:+48126193332">12 619 33 32</a></dd></div>' if el else ""
    return f'''<section class="sek kontakt" id="kontakt"><div class="wrap kont-uklad">
  <div><h2>Kontakt</h2><p class="kont-firma">Handlowa Spółdzielnia JUBILAT<br>al. Zygmunta Krasińskiego 1, 31-111 Kraków</p><p class="sek-stopka"><a class="link-dalej" href="{Pp.a("kontakt/")}">Wszystkie kontakty</a></p></div>
  <dl class="kont-dl">{salon}<div><dt>Telefon</dt><dd><a href="{tel_href(D.FIRMA["tel"])}">{D.FIRMA["tel"]}</a></dd></div><div><dt>E-mail</dt><dd><a href="mailto:{D.FIRMA["email"]}">{D.FIRMA["email"]}</a></dd></div><div><dt>Faks</dt><dd>{D.FIRMA["faks"]}</dd></div><div><dt>Praca</dt><dd><a href="{Pp.a("praca/")}">Aktualne oferty pracy</a></dd></div></dl>
  <ul class="social">{social}</ul>
</div></section>'''


def s_sklepy():
    Pp = P("sklepy/")
    m = META["/sklepy/"]
    lead = "Dom Handlowy przy al. Krasińskiego i osiem sklepów osiedlowych w zachodniej i północnej części Krakowa. Na mapie widać, który jest najbliżej, a przy każdym adresie godziny na dziś, także w niedziele handlowe i w święta."
    body = ph(Pp, [("Sklepy", "sklepy/")], e(m["h1"]), lead) + f'''
<section class="sek placowki"><div class="wrap">{sekcja_placowek(Pp, "h2", "Mapa i godziny wszystkich placówek", "Wybierz rodzaj placówki albo włącz „Najbliżej mnie”. Nazwa placówki prowadzi do jej strony z pełnymi godzinami i dojazdem.")}</div></section>
<section class="sek"><div class="wrap dwie">
  <div class="blok"><h2>W każdym sklepie Jubilat</h2><p>{e(D._SKLEP_OPIS)}</p><ul class="lista-kr">{"".join(f"<li>{e(u)}</li>" for u in D._SKLEP_USLUGI)}</ul></div>
  <div class="blok"><h2>Niedziele handlowe</h2><p>W niedziele handlowe otwieramy wszystkie placówki poza sklepem przy Placu Na Stawach i barami mlecznymi. Najbliższe: <b>{nh_tekst(3)}</b>.</p>
  {tabela_nh()}<p class="sek-stopka"><a class="link-dalej" href="{Pp.a("niedziele-handlowe/")}">Niedziele handlowe i święta w 2026 i 2027</a></p></div>
</div></section>
{faq_html("sklepy")}'''
    items = [{"@type": "ListItem", "position": i + 1, "url": B + "/" + path_pl(p), "name": p["nazwa"]} for i, p in enumerate(D.PLACOWKI)]
    strona("sklepy/", body=body, ld=[okruszki_ld([("Sklepy", "sklepy/")]), {"@type": "ItemList", "itemListElement": items}, faq_ld("sklepy")], nav_akt="sklepy/",
           mob=("Najbliżej mnie", "#placowki"))


def tabela_nh():
    rows = [("Dom Handlowy, stoisko spożywcze", "8:00-20:00"), ("Dom Handlowy, HOME i Salon Eleganza", "10:00-18:00"),
            ("Sklepy osiedlowe", "9:00-17:00"), ("Sklep przy Placu Na Stawach", "nieczynne"), ("Bary Żaczek i Flisak", "nieczynne")]
    return '<table class="gt"><caption>Godziny w niedzielę handlową</caption>' + "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows) + "</table>"


def s_sklep(p):
    path = path_pl(p)
    Pp = P(path)
    m = META["/" + path]
    info = foto_pl(p)
    meta = f'<a class="btn btn-ciem" href="{tel_href(p["tel"])}">Zadzwoń: {p["tel"]}</a><a class="btn btn-linia" href="{prowadz(p)}" target="_blank" rel="noopener">Wyznacz trasę</a>'
    dzielnica = DZIELNICE.get(p["id"], "")
    lead = f"{e(p['adres'])}, Kraków{(' (' + e(dzielnica) + ')') if dzielnica else ''}. Sklep spożywczo-przemysłowy Handlowej Spółdzielni Jubilat."
    inne = "".join(f'<li><a href="{Pp.a(path_pl(q))}"><b>{e(q["krotka"] if q["typ"] == "sklep" else q["nazwa"])}</b><span class="st" data-st="{q["id"]}"></span></a></li>' for q in [DH] + SKLEPY if q is not p)
    nh_uw = "W niedziele handlowe sklep jest nieczynny." if not p["godz"].get("nh") else f"Najbliższe niedziele handlowe: {nh_tekst(3)}."
    body = ph(Pp, [("Sklepy", "sklepy/"), (p["krotka"], path)], e(m["h1"]), lead, meta, foto=info, foto_alt=alt_pl(p), st_id=p["id"]) + f'''
<section class="sek"><div class="wrap dwie">
  <div class="blok"><h2>Godziny otwarcia</h2>{tabela_godz(p["godz"])}<p class="godz-uw">{nh_uw} W święta ustawowo wolne od pracy sklep jest nieczynny, a w Wielką Sobotę czynny najdłużej do 14:00.</p></div>
  <div class="blok"><h2>Adres i dojazd</h2><dl class="dane"><div><dt>Adres</dt><dd>{e(p["adres"])}, Kraków</dd></div><div><dt>Telefon</dt><dd><a href="{tel_href(p["tel"])}">{p["tel"]}</a></dd></div></dl>
  <div class="mapa-mini" data-mapa="{p["id"]}" role="region" aria-label="Mapa: {e(p["nazwa"])}"><p class="mapa-zast">Mapa wczyta się po przewinięciu.</p></div></div>
</div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap dwie">
  <div class="blok"><h2>W tym sklepie kupisz</h2><p>{e(p["opis"])}</p></div>
  <div class="blok"><h2>Płatności i usługi</h2><ul class="lista-kr">{"".join(f"<li>{e(u)}</li>" for u in p["uslugi"])}</ul></div>
</div></section>
<section class="sek"><div class="wrap"><div class="sek-glowa"><h2>Inne placówki Jubilat</h2></div><ul class="inne">{inne}</ul>
<p class="sek-stopka"><a class="link-dalej" href="{Pp.a("sklepy/")}">Mapa wszystkich placówek</a></p></div></section>'''
    strona(path, body=body, ld=[placowka_ld(p, B + "/" + url_img(info, info["ws"][min(2, len(info["ws"]) - 1)])), okruszki_ld([("Sklepy", "sklepy/"), (p["krotka"], path)])],
           nav_akt="sklepy/", mob=("Wyznacz trasę", prowadz(p).replace("&amp;", "&"), p["tel"]), og_img=url_img(info, info["ws"][min(2, len(info["ws"]) - 1)]),
           preload_img=preload_hero(Pp, info))


def s_dh():
    Pp = P("dom-handlowy/")
    m = META["/dom-handlowy/"]
    info = foto_pl(DH)
    meta = f'<a class="btn btn-ciem" href="tel:+48126193300">Zadzwoń: 12 619 33 00</a><a class="btn btn-linia" href="{prowadz(DH)}" target="_blank" rel="noopener">Wyznacz trasę</a>'
    lead = "Siedem kondygnacji nad Wisłą, kilka kroków od Wawelu, a w nich zakupy na co dzień i na specjalne okazje. Parter spożywczy, I piętro HOME ze strefą Beauty, II i III piętro Salon Eleganza."
    tabs = "".join(tabela_godz(d["godz"], f'{d["poz"]}: {d["nazwa"]}') for d in DH["dzialy"])
    body = ph(Pp, [("Dom Handlowy", "dom-handlowy/")], e(m["h1"]), lead, meta, foto=info, foto_alt=FOTO_ALT["dh"], foto_cap="al. Zygmunta Krasińskiego 1, róg ul. Zwierzynieckiej", st_id="dh") + f'''
<section class="sek dh"><div class="wrap"><div class="sek-glowa"><h2>Działy i piętra</h2><p>Każde piętro ma swoje godziny. Stoisko spożywcze jest czynne najdłużej: od poniedziałku do soboty do 22:00.</p></div>{pietra_html(Pp)}</div></section>
<section class="sek produkty"><div class="wrap">
  <div class="sek-glowa sek-glowa-row"><div><h2>Produkty unikatowe na parterze</h2><p>Obok produktów znanych marek półki z wyrobami regionalnych mleczarni i małych manufaktur.</p></div>
  <div class="strzalki"><button type="button" data-kier="-1" aria-label="Przewiń produkty w lewo">‹</button><button type="button" data-kier="1" aria-label="Przewiń produkty w prawo">›</button></div></div>
  {polka_html(Pp, 10)}<p class="sek-stopka"><a class="link-dalej" href="{Pp.a("produkty-unikatowe/")}">Wszystkie produkty unikatowe</a></p></div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap dwie">
  <div class="blok"><h2>Godziny otwarcia</h2><div style="margin-top:22px">{tabs}</div><p class="godz-uw">W pozostałe niedziele i w święta ustawowo wolne od pracy Dom Handlowy jest nieczynny. Najemcy w budynku mogą mieć własne godziny.</p></div>
  <div class="blok"><h2>Płatności i bony</h2><p>Karta, gotówka, bony towarowe i podarunkowe Jubilata oraz bony i karty Pluxee. Na parterze opłacisz rachunki i wypłacisz gotówkę przy kasie (cashback).</p>
   <ul class="lista-kr"><li>Bony podarunkowe 50 zł realizujesz na stoiskach przemysłowych (I, II i III piętro), a kupisz na I i II piętrze.</li><li>Firmy zamawiają bony towarowe 10, 20 i 50 zł: <a class="link" href="mailto:marketing@jubilat.com.pl">marketing@jubilat.com.pl</a></li><li>3% rabatu dla posiadaczy krakowskich kart rodzinnych</li></ul>
   <h2 style="margin-top:52px">Dojazd</h2><p>Tramwajem do przystanku Jubilat, przy samym budynku. Spacerem z Rynku Głównego ulicą Zwierzyniecką, z Wawelu bulwarami.</p>
   <div class="mapa-mini" data-mapa="dh" role="region" aria-label="Mapa: Dom Handlowy Jubilat"><p class="mapa-zast">Mapa wczyta się po przewinięciu.</p></div></div>
</div></section>
<section class="sek"><div class="wrap skroty-w"><ul class="skroty">
  <li><a href="{Pp.a("eleganza/")}"><h3>Salon Eleganza</h3><p>Moda na II i III piętrze, kolekcja jesień-zima i marki w salonie.</p></a></li>
  <li><a href="{Pp.a("lokale-na-wynajem/")}"><h3>Sala konferencyjna</h3><p>Do 80 miejsc w budynku Domu Handlowego.</p></a></li>
  <li><a href="{Pp.a("gazetka/")}"><h3>Gazetka</h3><p>Aktualna oferta Domu Handlowego w PDF.</p></a></li></ul></div></section>'''
    strona("dom-handlowy/", body=body, ld=[placowka_ld(DH, B + "/" + url_img(info)), okruszki_ld([("Dom Handlowy", "dom-handlowy/")])], nav_akt="dom-handlowy/",
           mob=("Wyznacz trasę", prowadz(DH).replace("&amp;", "&"), "12 619 33 00"), preload_img=preload_hero(Pp, info))


def s_produkty():
    Pp = P("produkty-unikatowe/")
    m = META["/produkty-unikatowe/"]
    lead = "Na półkach Jubilata są rzeczy, których nie znajdziesz w dużych sieciach: nabiał z regionalnych mleczarni, ręcznie robione pierogi i łazanki, zioła i herbatki, miody i słodycze od małych producentów."
    out = ""
    for k, n, pr, wag, cena in D.PRODUKTY:
        info = przygotuj("p-" + k, WIZ / f"p-{k}.jpg", [220, 440])
        out += f'<li class="prod">{pic(Pp, info, n, sizes="(max-width: 760px) 45vw, 240px")}<div class="prod-in"><p class="cena">{cena} zł</p><h2 class="prod-h">{e(n)}</h2><p>{e(pr)}, {wag}</p></div></li>'
    body = ph(Pp, [("Dom Handlowy", "dom-handlowy/"), ("Produkty unikatowe", "produkty-unikatowe/")], e(m["h1"]), lead) + f'''
<section class="sek"><div class="wrap"><ul class="prod-siatka">{out}</ul>
<p class="przypis">Ceny z jubilat.com.pl, stan na {D.PRODUKTY_STAN}. Część produktów jest sezonowa. Ceny i dostępność sprawdzisz w konkretnym sklepie, a najszerszy wybór jest na stoisku spożywczym Domu Handlowego.</p></div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap dwie">
  <div class="blok"><h2>Skąd pochodzą</h2><p>Wśród dostawców są regionalne mleczarnie, takie jak OSM w Skale i Spółdzielnia Mleczarska w Łapach, małe kuchnie robiące pierogi ręcznie, zielarze i pasieki.</p></div>
  <div class="blok"><h2>Gdzie kupić</h2><p>Najszerszy wybór jest na parterze Domu Handlowego przy al. Krasińskiego 1, czynnym od poniedziałku do soboty do 22:00. Część produktów jest też w <a href="{Pp.a("sklepy/")}">sklepach osiedlowych</a>.</p></div>
</div></section>'''
    strona("produkty-unikatowe/", body=body, ld=[okruszki_ld([("Dom Handlowy", "dom-handlowy/"), ("Produkty unikatowe", "produkty-unikatowe/")])], nav_akt="dom-handlowy/")


def s_eleganza():
    Pp = P("eleganza/")
    m = META["/eleganza/"]
    f1 = przygotuj("lb-k56", WIZ / "eleganza" / "lb" / "k56.jpg", [360, 533])
    f2 = przygotuj("lb-k16", WIZ / "eleganza" / "lb" / "k16.jpg", [360, 533])
    f3 = przygotuj("lb-k53", WIZ / "eleganza" / "lb" / "k53.jpg", [360, 533])
    sch = przygotuj("lb-schody", WIZ / "eleganza" / "lb" / "schody.jpg", [960, 1440, 1920])
    lb = ""
    for i, (k, opis) in enumerate(D.LOOKBOOK):
        inf = przygotuj("lb-" + k, WIZ / "eleganza" / "lb" / f"{k}.jpg", [360, 533])
        lb += (f'<li class="lk-k{" lk-duzy" if i == 0 else ""}"><figure><button type="button" data-lbx="lk" data-duze="{Pp.a("assets/img/lb-" + k + "-533.webp")}" aria-label="Powiększ: {e(opis)}">'
               f'{pic(Pp, inf, opis, sizes="(max-width: 760px) 50vw, 25vw" if i else "(max-width: 760px) 100vw, 50vw")}</button><figcaption>{e(opis)}</figcaption></figure></li>')
    marki = ""
    for k, n, w, opis in D.MARKI:
        src = WIZ / "eleganza" / "marki" / f"{k}.webp"
        if src.exists() and w:
            iw, ih = Image.open(src).size
            marki += f'<li><img src="{Pp.a("assets/img/marki/" + k + ".webp")}" width="{iw}" height="{ih}" style="--w:{w}px" loading="lazy" alt="{e(n)}"><span class="marka-opis">{e(opis)}</span></li>'
        else:
            marki += f'<li><span class="marka-txt">{e(n)}</span><span class="marka-opis">{e(opis)}</span></li>'
    g = DH["dzialy"][2]["godz"]
    body = f'''<section class="elh">
  <div class="elh-in">
    <h1 class="elh-logo"><img src="{Pp.a("assets/img/eleganza-logo-bialy.webp")}" width="727" height="466" alt=""><span class="sr">{e(m["h1"])}</span></h1>
    <p class="elh-haslo">Prawdziwy luksus szyty w&nbsp;Polsce</p>
    <p class="elh-lead">Odzież damska, męska i dziecięca, obuwie i galanteria na II i III piętrze Domu Handlowego Jubilat. 95% kolekcji pochodzi od polskich producentów.</p>
    <div class="elh-cta"><a class="btn el-btn" href="#kolekcja">Zobacz kolekcję</a><a class="elh-link" href="#wizyta">Godziny i dojazd</a></div>
    <p class="elh-teraz st-el" data-st="dh:2" data-st-pre="Salon: "></p>
  </div>
  <div class="elh-foto">{pic(Pp, f1, "Kobieta w bordowym komplecie i krótkim płaszczu z kolekcji jesień-zima", sizes="(max-width: 760px) 100vw, 30vw", lazy=False, prio=True, img_cls="elh-f1")}{pic(Pp, f2, "Para w granatowym garniturze i czarnej sukience koktajlowej", sizes="30vw", img_cls="elh-f2", cls="elh-p2")}</div>
</section>
<section class="el-sek el-o"><div class="el-wrap el-o-uklad">
  <div class="el-o-tekst"><h2>Salon dla tych, którzy znają się na materiałach</h2>
    <p class="el-o-duzy">Eleganza to salon dla osób, które przy zakupach patrzą najpierw na tkaninę, krój i wykończenie. 95% asortymentu pochodzi od polskich producentów, więc kupując u nas, wspierasz polskie szwalnie i domy mody.</p>
    <p>Na dwóch piętrach Domu Handlowego znajdziesz garderobę na co dzień i na wyjątkowe okazje: płaszcze, garnitury, sukienki, dzianiny, buty, torebki i walizki, a także ubrania dla dzieci.</p></div>
  <figure class="el-o-foto">{pic(Pp, f3, "Kobieta w satynowej bluzce i czarnych spodniach na schodach kamienicy", sizes="(max-width: 760px) 100vw, 33vw")}</figure>
</div></section>
<section class="el-sek el-kol" id="kolekcja"><div class="el-wrap">
  <div class="el-glowa"><h2>Kolekcja jesień-zima 2026</h2><p>Wybrane stylizacje, które są teraz w salonie. Kolekcję uzupełniamy co kilka tygodni. Dotknij zdjęcia, żeby je powiększyć.</p></div>
  <ul class="lk">{lb}</ul>
</div></section>
<section class="el-sek el-marki" id="marki"><div class="el-wrap">
  <div class="el-glowa"><h2>Marki w salonie</h2><p>Polskie domy mody obok sprawdzonych marek z Europy. Od garnituru po walizkę na wyjazd.</p></div>
  <ul class="marki-pas">{marki}</ul>
</div></section>
<section class="el-wiz" id="wizyta">
  <figure class="el-wiz-foto">{pic(Pp, sch, "Para w swobodnych stylizacjach na kamiennych schodach kamienicy", sizes="100vw")}</figure>
  <div class="el-wrap el-wiz-uklad">
    <div><h2>Odwiedź salon</h2><p class="el-wiz-adr">Dom Handlowy Jubilat, II-III piętro<br>al. Zygmunta Krasińskiego 1, 31-111 Kraków</p>
      <ul class="el-pietra"><li>Odzież damska i męska</li><li>Moda dziecięca</li><li>Obuwie i galanteria skórzana</li><li>Walizki i torby podróżne</li><li>Tekstylia, zabawki i artykuły szkolno-biurowe</li></ul>
      <div class="el-wiz-akcje"><a class="btn el-btn-pel" href="tel:+48126193332">Zadzwoń: 12 619 33 32</a><a class="btn el-btn-linia" href="{prowadz(DH)}" target="_blank" rel="noopener">Wyznacz trasę</a></div></div>
    <div><h3>Godziny otwarcia</h3>
      <table class="el-godz" data-gt><tr data-r="pt"><td>Poniedziałek - piątek</td><td>{zakres(g["pt"])}</td></tr><tr data-r="sob"><td>Sobota</td><td>{zakres(g["sob"])}</td></tr><tr data-r="nh"><td>Niedziela handlowa</td><td>{zakres(g["nh"])}</td></tr></table>
      <p class="el-nh">Najbliższe niedziele handlowe: {nh_tekst(3)}. W pozostałe niedziele i święta salon jest nieczynny.</p>
      <h3>Dojazd</h3><p class="el-dojazd">Przystanek tramwajowy Jubilat jest tuż przy wejściu, przy moście Dębnickim. Wawel i Rynek Główny są w zasięgu krótkiego spaceru.</p>
      <p class="el-dojazd">Telefon do salonu: <a href="tel:+48126193332">12 619 33 32</a> lub <a href="tel:+48126193333">12 619 33 33</a>. W Salonie Eleganza zbierasz punkty w <a href="{Pp.a("okazje/")}">aplikacji Jubilat</a>.</p></div>
  </div>
</section>
{faq_html("eleganza", "Pytania o Salon Eleganza")}
{kontakt_sek(Pp, el=True)}
<dialog class="lbx" id="lbx" aria-label="Powiększone zdjęcie"><figure class="lbx-in"><img id="lbxImg" src="data:," alt=""><figcaption><span id="lbxOpis"></span><span class="lbx-nr" id="lbxNr"></span></figcaption></figure>
<button class="lbx-b lbx-z" id="lbxZ" type="button" aria-label="Zamknij">×</button><button class="lbx-b lbx-p" id="lbxP" type="button" aria-label="Poprzednie zdjęcie">‹</button><button class="lbx-b lbx-n" id="lbxN" type="button" aria-label="Następne zdjęcie">›</button></dialog>'''
    el_ld = {"@type": "ClothingStore", "@id": B + "/eleganza/#salon", "name": "Salon Eleganza w Domu Handlowym Jubilat", "url": B + "/eleganza/",
             "image": B + "/assets/img/lb-k56-533.webp", "telephone": "+48 12 619 33 32", "address": adres_ld(DH),
             "containedInPlace": {"@id": B + "/dom-handlowy/#placowka"}, "parentOrganization": {"@id": ORG_ID},
             "geo": {"@type": "GeoCoordinates", "latitude": DH["lat"], "longitude": DH["lng"]},
             "openingHoursSpecification": godz_ld(g), "specialOpeningHoursSpecification": specjalne_ld(g),
             "brand": [{"@type": "Brand", "name": n} for _, n, *_ in D.MARKI]}
    strona("eleganza/", body=body, body_cls="el", ld=[el_ld, okruszki_ld([("Salon Eleganza", "eleganza/")]), faq_ld("eleganza")], nav_akt="eleganza/", theme="#5f060f",
           mob=("Godziny i dojazd", "#wizyta", "12 619 33 32"), og_img="assets/img/og-eleganza.jpg", fonts_el=True,
           preload_img=preload_hero(Pp, f1, "(max-width: 760px) 100vw, 30vw"))


def s_bary():
    Pp = P("bary-mleczne/")
    m = META["/bary-mleczne/"]
    lead = "Dwa bary mleczne prowadzone przez spółdzielnię Jubilat. Zupy, pierogi, kotlety i surówki, gotowane na miejscu każdego dnia. Menu na bieżący tydzień publikujemy na stronie każdego baru."
    body = ph(Pp, [("Bary mleczne", "bary-mleczne/")], e(m["h1"]), lead) + f'''
<section class="sek bary"><div class="wrap"><div class="bary-uklad">{"".join(bar_karta(Pp, b, "h2") for b in BARY)}</div></div></section>
{faq_html("bary")}'''
    strona("bary-mleczne/", body=body, ld=[okruszki_ld([("Bary mleczne", "bary-mleczne/")]), faq_ld("bary")], nav_akt="bary-mleczne/", mob=("Menu tygodnia", "#tresc"))


def s_bar(p):
    path = path_pl(p)
    Pp = P(path)
    m = META["/" + path]
    info = foto_pl(p)
    opis = {"zaczek": "Żaczek stoi przy Czarnowiejskiej, w okolicy uczelni i akademików, więc w porze obiadu przy stolikach siedzą obok siebie studenci i stali bywalcy z sąsiedztwa.",
            "flisak": "Flisak jest naprzeciw Domu Handlowego Jubilat, na początku ul. Kościuszki, w drodze na Salwator. Dobre miejsce na obiad po zakupach albo po spacerze bulwarami."}[p["id"]]
    meta = f'<a class="btn btn-ciem" href="{tel_href(p["tel"])}">Zadzwoń: {p["tel"]}</a><a class="btn btn-linia" href="#menu">Menu tygodnia</a>'
    dow = ", ".join(f'<a class="link" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in p["dowoz"])
    inny = BARY[1] if p is BARY[0] else BARY[0]
    body = ph(Pp, [("Bary mleczne", "bary-mleczne/"), (p["krotka"], path)], e(m["h1"]), f"{e(p['adres'])}, {p['kod']} Kraków. {e(opis)}", meta, foto=info, foto_alt=alt_pl(p), st_id=p["id"]) + f'''
<section class="sek" id="menu"><div class="wrap">
  <div class="menu-glowa"><h2>Menu tygodnia</h2><p>{menu_zakres()}. Zestaw: zupa i drugie danie.</p></div>
  <ul class="menu-t" data-menu="{p["id"]}">{menu_lista(p["id"])}</ul>
  <p class="menu-info" data-menu-info>Dania mogą się skończyć przed zamknięciem, zwłaszcza w porze obiadowej. Nowe menu publikujemy na początku każdego tygodnia.</p>
</div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap dwie">
  <div class="blok"><h2>Godziny otwarcia</h2>{tabela_godz(p["godz"], nh_daty=False)}<p class="godz-uw">Zamówienia z dowozem: {dow}.</p></div>
  <div class="blok"><h2>Adres i dojazd</h2><dl class="dane"><div><dt>Adres</dt><dd>{e(p["adres"])}, {p["kod"]} Kraków</dd></div><div><dt>Telefon</dt><dd><a href="{tel_href(p["tel"])}">{p["tel"]}</a></dd></div></dl>
  <div class="mapa-mini" data-mapa="{p["id"]}" role="region" aria-label="Mapa: {e(p["nazwa"])}"><p class="mapa-zast">Mapa wczyta się po przewinięciu.</p></div></div>
</div></section>
<section class="sek"><div class="wrap"><ul class="inne"><li><a href="{Pp.a(path_pl(inny))}"><b>{e(inny["nazwa"])}, {e(inny["adres"])}</b><span class="st" data-st="{inny["id"]}"></span></a></li>
<li><a href="{Pp.a("dom-handlowy/")}"><b>Dom Handlowy Jubilat</b><span class="st" data-st="dh"></span></a></li></ul></div></section>'''
    menu_ld = {"@type": "Menu", "@id": B + "/" + path + "#menu", "name": f"Menu tygodnia {menu_zakres()}", "hasMenuItem": [
        {"@type": "MenuItem", "name": f"{z} + {d2}", "offers": {"@type": "Offer", "price": c.replace(",", "."), "priceCurrency": "PLN"}} for z, d2, c in D.MENU[p["id"]]]}
    strona(path, body=body, ld=[placowka_ld(p, B + "/" + url_img(info)), menu_ld, okruszki_ld([("Bary mleczne", "bary-mleczne/"), (p["krotka"], path)])],
           nav_akt="bary-mleczne/", mob=("Menu tygodnia", "#menu", p["tel"]), preload_img=preload_hero(Pp, info))


def s_gazetka():
    Pp = P("gazetka/")
    m = META["/gazetka/"]
    G = D.GAZETKA
    okl = przygotuj("gazetka-okladka", SRC / "_tmp_gaz" / "s1.png", [300, 600, 900])
    strony = ""
    for i in range(1, G["strony"] + 1):
        th = przygotuj(f"gaz-s{i}", SRC / "_tmp_gaz" / f"s{i}.png", [200, 1100])
        strony += (f'<li><button type="button" data-lbx="gz" data-duze="{Pp.a("assets/img/gaz-s" + str(i) + "-" + str(th["ws"][-1]) + ".webp")}" aria-label="Powiększ stronę {i}">'
                   f'{pic(Pp, th, f"Gazetka Jubilat, strona {i}", sizes="(max-width: 760px) 23vw, 110px")}</button><span>{i}</span></li>')
    pdf = Pp.a("assets/pdf/" + G["plik"])
    size_mb = (ROOT / "assets/pdf" / G["plik"]).stat().st_size / 1e6
    body = ph(Pp, [("Gazetka", "gazetka/")], e(m["h1"]), "Promocje z gazetki obowiązują w Domu Handlowym Jubilat, chyba że przy produkcie zaznaczono inaczej. Gazetkę przejrzysz na stronie albo pobierzesz w PDF.") + f'''
<section class="sek"><div class="wrap">
  <div class="gz">
    <a class="gz-okl" href="{pdf}" target="_blank" rel="noopener">{pic(Pp, okl, "Okładka gazetki Jubilat: " + G["tytul"], sizes="(max-width: 760px) 280px, 420px")}</a>
    <div><h2>{e(G["tytul"])}</h2><p class="gz-daty">Oferta ważna od {data_pl(G["od"], False)} do {data_pl(G["do"])}</p>
    <p class="st" data-gazetka data-gaz-od="{D.GAZETKA['od']}" data-gaz-do="{D.GAZETKA['do']}">{gaz_status()}</p>
    <p class="gz-opis">{e(G["miejsce"])}. {G["strony"]} stron. Okres ważności jest podany także na pierwszej stronie gazetki.</p>
    <div class="akcje"><a class="btn btn-ciem" href="{pdf}" target="_blank" rel="noopener">Otwórz gazetkę (PDF, {size_mb:.1f} MB)</a><a class="btn btn-linia" href="{pdf}" download>Pobierz</a></div>
    {test_uw("to ostatnia opublikowana gazetka (21.10-04.11.2026). Po jej terminie status sam zmienia się na „zakończona”. Nową gazetkę dodaje się w panelu: plik PDF + daty od-do.")}</div>
  </div>
  <div class="gz-strony"><h3>Strony gazetki</h3><ul class="galeria">{strony}</ul></div>
</div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap"><div class="sek-glowa"><h2>Okazje z aplikacji</h2><p>Ceny dla klientów z aplikacją Jubilat albo kartą lojalnościową. <a href="{Pp.a("okazje/")}">Okazje, rabaty i aplikacja</a></p></div>{okazje_html(Pp, "okazje-siatka")}</div></section>
<dialog class="lbx lbx-jasny" id="lbx" aria-label="Powiększona strona gazetki"><figure class="lbx-in"><img id="lbxImg" src="data:," alt=""><figcaption><span id="lbxOpis"></span><span class="lbx-nr" id="lbxNr"></span></figcaption></figure>
<button class="lbx-b lbx-z" id="lbxZ" type="button" aria-label="Zamknij">×</button><button class="lbx-b lbx-p" id="lbxP" type="button" aria-label="Poprzednia strona">‹</button><button class="lbx-b lbx-n" id="lbxN" type="button" aria-label="Następna strona">›</button></dialog>'''
    strona("gazetka/", body=body, ld=[okruszki_ld([("Gazetka", "gazetka/")])], nav_akt="gazetka/", mob=("Otwórz PDF", "assets/pdf/" + G["plik"]))


def s_okazje():
    Pp = P("okazje/")
    m = META["/okazje/"]
    plak = przygotuj("app-plakat", RAW / "Aplikacja_JUBILAT_nowy_plakat.webp", [400, 700])
    body = ph(Pp, [("Okazje i aplikacja", "okazje/")], e(m["h1"]), "Okazje z aplikacji, rabat dla krakowskich rodzin, bony towarowe i podarunkowe. Wszystko, co obniża rachunek w sklepach Jubilat.") + f'''
<section class="sek"><div class="wrap"><div class="sek-glowa"><h2>Okazje z aplikacji</h2><p>Ceny dla klientów z aplikacją Jubilat albo kartą lojalnościową Społem lub Jubilat. Każda okazja ma termin od-do i znika ze strony sama po jego zakończeniu.</p></div>
{okazje_html(Pp, "okazje-siatka")}
<p class="przypis">Najniższe ceny z 30 dni podano ze stoiska spożywczego DH Jubilat, al. Krasińskiego 1.</p>
{test_uw("produkty i ceny z okazji 20-26.10.2026, daty ustawione przykładowo (03-16.11). Jedna karta jest zaplanowana od 17.11 i do tego dnia jest ukryta.")}</div></section>
<section class="sek aplikacja" id="aplikacja"><div class="wrap app-uklad">
  <div class="app-tekst"><h2>Aplikacja Jubilat</h2>
    <ul class="app-lista"><li>Za każde wydane 10 zł dostajesz 1 punkt, a na start 100 punktów.</li><li>Punkty wymieniasz na e-bony o wartości 5, 20 i 40 zł.</li><li>Punkty zbierasz w sklepach Jubilat, w Salonie Eleganza, na stoisku HOME oraz w barach Flisak i Żaczek.</li><li>Masz dostęp do okazji i akcji specjalnych w całej sieci.</li><li>Korzystałeś z karty klienta Społem w 2025 r.? Pobierz aplikację i dokończ rejestrację. Możesz też otrzymać nową kartę klienta Jubilat.</li></ul>
    {app_przyciski()}
    <p class="app-pomoc">Pomoc w sprawie aplikacji: <a href="tel:+48780191172">780 191 172</a>, pn-pt 7:00-15:00. <a href="{Pp.a("assets/pdf/regulamin-aplikacji-jubilat.pdf")}" target="_blank" rel="noopener">Regulamin aplikacji (PDF)</a></p></div>
  <figure class="app-plakat">{pic(Pp, plak, "Plakat: nowy program lojalnościowy Jubilat, 100 punktów na start", sizes="(max-width: 1060px) 80vw, 420px")}</figure>
</div></section>
<section class="sek" id="rabaty"><div class="wrap dwie">
  <div class="blok"><h2>3% rabatu dla krakowskich rodzin</h2><p>Posiadacze kart Krakowskie Rodziny z Niepełnosprawnym Dzieckiem, Krakowska Duża Rodzina oraz Rodzina 3+ dostają 3% rabatu na zakupy we wszystkich naszych sklepach. Wystarczy pokazać kartę przy kasie.</p>
  <ul class="lista-kr"><li>Rabat od zakupów za min. 5 zł</li><li>Nie obejmuje alkoholu, wyrobów tytoniowych, prasy, doładowań telefonicznych ani toreb na zakupy</li></ul></div>
  <div class="blok"><h2>Bony towarowe i podarunkowe</h2><p>Bony Jubilata kupisz na I i II piętrze Domu Handlowego. Bony podarunkowe 50 zł realizujesz na stoiskach przemysłowych DH (I, II i III piętro). Za zakupy zapłacisz też bonami i kartami Pluxee.</p>
  <p>Firmy zamawiają bony towarowe w nominałach 10, 20 i 50 zł: <a href="mailto:marketing@jubilat.com.pl">marketing@jubilat.com.pl</a>. Płatność przelewem, rozliczenie notą księgową.</p></div>
</div></section>'''
    strona("okazje/", body=body, ld=[okruszki_ld([("Okazje i aplikacja", "okazje/")])], nav_akt="okazje/", mob=("Pobierz aplikację", "#aplikacja"))


def s_niedziele():
    Pp = P("niedziele-handlowe/")
    m = META["/niedziele-handlowe/"]
    def lista(rok):
        return "".join(f'<li data-data="{d}">{data_pl(d, False)} <span>({["poniedziałek","wtorek","środa","czwartek","piątek","sobota","niedziela"][datetime.date.fromisoformat(d).weekday()]})</span></li>' for d in D.NIEDZIELE_HANDLOWE if d.startswith(rok))
    sw = lambda rok: "".join(f'<li data-data="{d}">{data_pl(d, False)} - {e(n)}</li>' for d, n in D.SWIETA.items() if d.startswith(rok))
    body = ph(Pp, [("Sklepy", "sklepy/"), ("Niedziele handlowe", "niedziele-handlowe/")], e(m["h1"]),
              f"Najbliższe niedziele handlowe: <b>{nh_tekst(3)}</b>. W te dni otwieramy Dom Handlowy i sklepy osiedlowe, poza sklepem przy Placu Na Stawach.") + f'''
<section class="sek"><div class="wrap dwie">
  <div class="blok">{tabela_nh()}<p class="godz-uw">Handel w niedziele jest dozwolony tylko w wyznaczone dni (ustawa z 10 stycznia 2018 r. o ograniczeniu handlu w niedziele i święta oraz w niektóre inne dni). W Wielką Sobotę sklepy mogą być czynne najdłużej do 14:00.</p></div>
  <div class="blok"><h2>Niedziele handlowe 2026</h2><ul class="lista-kr daty">{lista("2026")}</ul>
  <h2 style="margin-top:44px">Niedziele handlowe 2027</h2><p>Wyliczone według ustawy.</p><ul class="lista-kr daty">{lista("2027")}</ul></div>
</div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap dwie">
  <div class="blok"><h2>Święta 2026 - sklepy nieczynne</h2><ul class="lista-kr daty">{sw("2026")}</ul></div>
  <div class="blok"><h2>Święta 2027 - sklepy nieczynne</h2><ul class="lista-kr daty">{sw("2027")}</ul></div>
</div></section>
{faq_html("sklepy")}'''
    strona("niedziele-handlowe/", body=body, ld=[okruszki_ld([("Sklepy", "sklepy/"), ("Niedziele handlowe", "niedziele-handlowe/")])], nav_akt="sklepy/")


def s_lokale():
    Pp = P("lokale-na-wynajem/")
    m = META["/lokale-na-wynajem/"]
    sala = przygotuj("sala", RAW / "IMG_1333-edited-scaled.webp", [600, 1000, 1600])
    sala2 = przygotuj("sala2", RAW / "IMG_1336-edited-scaled.webp", [600, 1000, 1600])
    meta = '<a class="btn btn-ciem" href="tel:+48126193398">Sala: 12 619 33 98</a><a class="btn btn-linia" href="tel:+48126193419">Lokale: 12 619 34 19</a>'
    body = ph(Pp, [("Lokale na wynajem", "lokale-na-wynajem/")], e(m["h1"]), "Spółdzielnia wynajmuje salę konferencyjną, biura, lokal użytkowy i magazyny. Sala i biura są w budynku Domu Handlowego przy al. Krasińskiego 1, przy samym przystanku tramwajowym.", meta, foto=sala, foto_alt="Sala konferencyjna w Domu Handlowym Jubilat, rzędy stołów przy oknach") + f'''
<section class="sek wynajem"><div class="wrap wyn-uklad">
  <div class="wyn-oferta">
    <h2>Sala konferencyjna na 80 osób</h2><p class="wyn-opis">Klimatyzowana i w pełni wyposażona sala na szkolenia, wykłady, prezentacje i spotkania firmowe.</p>
    <dl class="wyn-dl">
      <div><dt>Sala konferencyjna</dt><dd>do 80 miejsc, klimatyzacja, tablice, rzutnik, nagłośnienie, internet. Tel. <a href="tel:+48126193398">12 619 33 98</a></dd></div>
      <div><dt>Biura</dt><dd>15 m², 15,4 m², 21,8 m² i 23,5 m²</dd></div>
      <div><dt>Lokal użytkowy</dt><dd>ul. Machaya 1, 122 m²</dd></div>
      <div><dt>Magazyny</dt><dd>powierzchnię dobierzemy do potrzeb. Tel. <a href="tel:+48126193419">12 619 34 19</a></dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:administracja@jubilat.com.pl">administracja@jubilat.com.pl</a></dd></div>
    </dl>
    <figure class="wyn-foto" style="margin-top:28px">{pic(Pp, sala2, "Sala konferencyjna Jubilat, widok na stoły i okna", sizes="(max-width: 1060px) 100vw, 45vw")}</figure>
  </div>
  {wyn_form()}
</div></section>
{faq_html("wynajem", "Pytania o wynajem")}'''
    strona("lokale-na-wynajem/", body=body, ld=[okruszki_ld([("Lokale na wynajem", "lokale-na-wynajem/")]), faq_ld("wynajem")], nav_akt="lokale-na-wynajem/",
           mob=("Zapytaj o wynajem", "#wynForm", "12 619 34 19"), preload_img=preload_hero(Pp, sala))


def wyn_form():
    return '''<form class="wyn-form" id="wynForm" novalidate>
  <h2 class="form-h">Zapytaj o wynajem</h2>
  <fieldset><legend>Czego szukasz?</legend><div class="chipy" data-p="typ">
    <button type="button" data-v="sala" class="on" aria-pressed="true">Sala konferencyjna</button><button type="button" data-v="biuro" aria-pressed="false">Biuro</button><button type="button" data-v="lokal" aria-pressed="false">Lokal użytkowy</button><button type="button" data-v="magazyn" aria-pressed="false">Magazyn</button></div></fieldset>
  <div class="pola" data-dla="sala"><label>Data wydarzenia<input type="date" id="fData"></label><label>Liczba osób<input type="number" id="fOsoby" min="1" max="80" inputmode="numeric" placeholder="np. 40"></label></div>
  <div class="pola" data-dla="biuro" hidden><fieldset class="pelne"><legend>Powierzchnia biura</legend><div class="chipy" data-p="biuro">
    <button type="button" data-v="15 m²" aria-pressed="false">15 m²</button><button type="button" data-v="15,4 m²" aria-pressed="false">15,4 m²</button><button type="button" data-v="21,8 m²" aria-pressed="false">21,8 m²</button><button type="button" data-v="23,5 m²" aria-pressed="false">23,5 m²</button></div></fieldset></div>
  <div class="pola" data-dla="magazyn" hidden><label>Potrzebna powierzchnia (m²)<input type="number" id="fM2" min="1" inputmode="numeric" placeholder="np. 50"></label></div>
  <div class="pola" data-dla="biuro lokal magazyn" hidden><label>Od kiedy<select id="fOd"><option value="">Od zaraz</option><option>od grudnia 2026</option><option>od stycznia 2027</option><option>od lutego 2027</option><option>od marca 2027</option><option>później, termin do ustalenia</option></select></label></div>
  <div class="pola"><label>Imię i nazwisko<input type="text" id="fImie" autocomplete="name"></label><label>Telefon<input type="tel" id="fTel" autocomplete="tel"></label></div>
  <label class="pelne">Kilka słów o potrzebach<textarea id="fOpis" rows="3"></textarea></label>
  <div class="podglad"><p class="podglad-tyt">Twoja wiadomość do <b>administracja@jubilat.com.pl</b></p><pre id="podglad"></pre></div>
  <div class="form-akcje"><a class="btn btn-ciem" id="wynMail" href="mailto:administracja@jubilat.com.pl">Wyślij e-mail</a><button class="btn btn-linia" type="button" id="wynKopiuj">Kopiuj treść</button><a class="wyn-tel" id="wynTel" href="tel:+48126193398">lub zadzwoń: 12 619 33 98</a></div>
</form>'''


def s_praca():
    Pp = P("praca/")
    m = META["/praca/"]
    of = ""
    for o in D.PRACA:
        kol = ""
        for t, l in (("Zakres obowiązków", o["zadania"]), ("Czego oczekujemy", o["wymagania"]), ("Co oferujemy", o["oferta"])):
            if l:
                kol += f'<div><h3>{t}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in l)}</ul></div>'
        of += (f'<li><details class="oferta" id="{o["slug"]}"{" open" if o is D.PRACA[0] else ""} data-od="{o["od"]}"{(" data-do=" + chr(34) + o["do"] + chr(34)) if o["do"] else ""}><summary><div><h2>{e(o["tytul"])}</h2><span>Sklepy Jubilat w Krakowie</span></div></summary>'
               f'<div class="oferta-in">{kol}</div></details></li>')
    body = ph(Pp, [("Praca", "praca/")], e(m["h1"]), "Szukamy ludzi do sklepów, barów mlecznych i Domu Handlowego. Pracujesz w Krakowie, blisko domu, w spółdzielni z ponad półwieczną historią.",
              f'<a class="btn btn-ciem" href="{D.PRACA_LINK}" target="_blank" rel="noopener">Aplikuj online</a><a class="btn btn-linia" href="tel:+48780191147">Zadzwoń: 780 191 147</a>') + f'''
<section class="sek"><div class="wrap">
  <div class="sek-glowa"><h2>Aktualne oferty</h2><p>Kliknij stanowisko, żeby zobaczyć szczegóły.</p></div>
  <ul class="oferty">{of}</ul>
  <div class="aplikuj"><div><h2>Jak aplikować</h2><p>Zgłoszenie wyślesz przez bezpieczny formularz rekrutacyjny eRecruiter albo mailem. W treści wiadomości wpisz stanowisko, na które aplikujesz.</p>
    <div class="akcje"><a class="btn btn-ciem" href="{D.PRACA_LINK}" target="_blank" rel="noopener">Formularz rekrutacyjny</a></div></div>
    <dl class="dane"><div><dt>Telefon</dt><dd><a href="tel:+48780191147">780 191 147</a></dd></div><div><dt>E-mail</dt><dd><a href="mailto:rekrutacja@jubilat.com.pl">rekrutacja@jubilat.com.pl</a></dd></div><div><dt>Adres</dt><dd>al. Zygmunta Krasińskiego 1, 31-111 Kraków</dd></div></dl></div>
</div></section>
{faq_html("praca")}'''
    jobs = [{"@type": "JobPosting", "title": o["tytul"], "datePosted": o["od"], "employmentType": "FULL_TIME",
             "description": "<p>" + "</p><p>".join(o["zadania"] + o["oferta"]) + "</p>",
             "hiringOrganization": {"@id": ORG_ID, "@type": "Organization", "name": D.FIRMA["nazwa"]},
             "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Kraków", "addressCountry": "PL", "streetAddress": D.FIRMA["ulica"], "postalCode": D.FIRMA["kod"], "addressRegion": "małopolskie"}}} for o in D.PRACA]
    strona("praca/", body=body, ld=[okruszki_ld([("Praca", "praca/")]), faq_ld("praca")] + jobs, nav_akt=None, mob=("Aplikuj", D.PRACA_LINK, "780 191 147"))


def s_historia():
    Pp = P("historia/")
    m = META["/historia/"]
    info = foto_pl(DH)
    hist = "".join(f'<li><span class="rok">{r}</span><p>{e(t)}</p></li>' for r, t in D.HISTORIA)
    tekst = [
        "Historia Domu Handlowego Jubilat sięga 1958 roku, kiedy krakowska spółdzielczość spożywców obchodziła jubileusz pięćdziesięciolecia. Wtedy narodziła się koncepcja nowoczesnego centrum handlowego, symbolu rozwoju spółdzielczości i odpowiedzi na potrzeby mieszkańców Krakowa. Rok później powstała pierwsza koncepcja architektoniczna: największy obiekt handlowy w mieście, z kawiarnią na dachu i widokiem na Wisłę.",
        "Wstępny projekt przygotował Henryk Jerzy Marconi, ale inwestycja się opóźniła. Zmieniono zespół projektowy, a ostateczną wersję budynku opracowano pod kierunkiem Jadwigi Sanickiej, z zachowaniem głównych założeń pierwotnej koncepcji. Stabilizacja podmokłego gruntu przy brzegu Wisły sprawiła, że budowa trwała blisko dekadę. Jubilat otwarto w lipcu 1969 roku i stał się największym, najnowocześniejszym domem towarowym w Krakowie.",
        "Budynek to modernistyczna plomba w kwartale międzywojennych kamienic u zbiegu ul. Zwierzynieckiej i al. Krasińskiego, tuż przy moście Dębnickim. Dwie przeszklone kondygnacje parteru otwierają wnętrze na ulicę. Dwa piętra handlowe wysunięto przed lico budynku i ujęto w szklaną ścianę kurtynową. Wyższe kondygnacje biurowe mają spokojniejszy rytm elewacji z dekoracyjnym rastrem, a na najwyższym piętrze jest bar i taras z widokiem na Wisłę i Wawel, częściowo osłonięty ażurowym okapem. Wieczorami przeszklona fasada rozświetlała się rzędami świetlówek.",
        "Przez niemal trzy dekady Jubilat był największym domem handlowym w Krakowie. W 1991 roku spółdzielnia przyjęła nazwę Handlowa Spółdzielnia Jubilat. W 2014 roku wymieniono stolarkę i przeszklenia: szyby o delikatnie niebieskim odcieniu zastąpiły pierwotne, brązowe. Dziś Jubilat pozostaje jednym z najbardziej rozpoznawalnych modernistycznych budynków Krakowa i ważnym miejscem zakupów w centrum miasta.",
    ]
    body = ph(Pp, [("Historia", "historia/")], e(m["h1"]), "Od spółdzielczości spożywców działającej w Krakowie od 1908 roku do modernistycznego domu handlowego nad Wisłą.", foto=info, foto_alt=FOTO_ALT["dh"], foto_cap="Dom Handlowy Jubilat, al. Krasińskiego 1") + f'''
<section class="sek"><div class="wrap hist-uklad">
  <div class="hist-tekst">{"".join(f"<p>{e(t)}</p>" for t in tekst)}</div>
  <div><ol class="os">{hist}</ol>
  <figure class="znak"><img src="{Pp.a("assets/img/znak-96.png")}" width="72" height="72" alt="Znak firmowy Jubilat: skrzydełko z czapki Merkurego" loading="lazy"><figcaption>Znakiem spółdzielni jest stylizowane skrzydełko z czapki Merkurego, patrona kupców. Oznacza dobrą jakość towarów i fachową obsługę.</figcaption></figure></div>
</div></section>'''
    strona("historia/", body=body, ld=[okruszki_ld([("Historia", "historia/")])], nav_akt="historia/", preload_img=preload_hero(Pp, info))


def s_aktualnosci():
    Pp = P("aktualnosci/")
    m = META["/aktualnosci/"]
    body = ph(Pp, [("Aktualności", "aktualnosci/")], e(m["h1"]), "Nowe marki w Salonie Eleganza i w strefie Beauty, zmiany godzin przed świętami, okazje i wydarzenia w Domu Handlowym.") + \
        f'<section class="sek"><div class="wrap">{akt_lista(Pp, D.AKTUALNOSCI)}</div></section>'
    strona("aktualnosci/", body=body, ld=[okruszki_ld([("Aktualności", "aktualnosci/")])], mob=("Godziny otwarcia", "sklepy/"))
    for i, a in enumerate(D.AKTUALNOSCI):
        path = f"aktualnosci/{a['slug']}/"
        Pa = P(path)
        logo = f'<div class="art-logo"><img src="{Pa.a("assets/img/marki/" + a["img"] + ".webp")}" alt="Logo marki {e(a["tytul"].split(" w ")[0])}"></div>' if a.get("img") else ""
        inne = [x for x in D.AKTUALNOSCI if x is not a][:3]
        body = f'''<article class="art">{okruszki(Pa, [("Aktualności", "aktualnosci/"), (skroc(a["tytul"], 40), path)])}
<h1>{e(a["tytul"])}</h1><p class="art-meta"><time datetime="{a["data"]}">{data_pl(a["data"])}</time> · {e(a["kat"])}</p>{logo}
<div class="art-tresc">{"".join(f"<p>{e(t)}</p>" for t in a["tresc"])}</div>
<div class="art-stopka"><a class="link-dalej" href="{Pa.a("aktualnosci/")}">Wszystkie aktualności</a><a class="link" href="{Pa.a("eleganza/" if a["kat"] == "Salon Eleganza" else "dom-handlowy/")}">{"Salon Eleganza" if a["kat"] == "Salon Eleganza" else "Dom Handlowy Jubilat"}</a></div>
</article>
<section class="sek" style="background:var(--szar)"><div class="wrap"><div class="sek-glowa"><h2>Inne aktualności</h2></div>{akt_lista(Pa, inne, h="h3", skrot=True)}</div></section>'''
        tit = (a["tytul"] + " - Jubilat Kraków")
        if len(tit) > 60:
            tit = a["tytul"][:60]
        ld = {"@type": "NewsArticle", "headline": a["tytul"], "datePublished": a["data"], "dateModified": a["data"], "inLanguage": "pl-PL",
              "author": {"@id": ORG_ID, "@type": "Organization", "name": D.FIRMA["nazwa"]}, "publisher": {"@id": ORG_ID, "@type": "Organization", "name": D.FIRMA["nazwa"], "logo": {"@type": "ImageObject", "url": B + "/assets/img/logo-jubilat.png"}},
              "mainEntityOfPage": B + "/" + path, "image": B + ("/assets/img/marki/" + a["img"] + ".webp" if a.get("img") else "/assets/img/og-jubilat.jpg")}
        strona(path, title=tit, desc=skroc(a["tresc"][0], 155), body=body, ld=[ld, okruszki_ld([("Aktualności", "aktualnosci/"), (a["tytul"], path)])])


def s_kontakt():
    Pp = P("kontakt/")
    m = META["/kontakt/"]
    dz = "".join(f'<div><dt>{e(n)}</dt><dd>{(f"<a href={chr(34)}{tel_href(t)}{chr(34)}>{t}</a>") if t else ""}{"<br>" if t and em else ""}{(f"<a href={chr(34)}mailto:{em}{chr(34)}>{em}</a>") if em else ""}</dd></div>' for n, t, em in D.KONTAKTY)
    pl = "".join(f'<div><dt>{e(p["krotka"] if p["typ"] == "sklep" else p["nazwa"])}</dt><dd><a href="{tel_href(p["tel"])}">{p["tel"]}</a> <span>· <a href="{Pp.a(path_pl(p))}">godziny</a></span></dd></div>' for p in D.PLACOWKI)
    zarz = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in D.ZARZAD)
    body = ph(Pp, [("Kontakt", "kontakt/")], e(m["h1"]), f'{D.FIRMA["nazwa"]}, al. Zygmunta Krasińskiego 1, 31-111 Kraków. Sekretariat: <a href="{tel_href(D.FIRMA["tel"])}">{D.FIRMA["tel"]}</a>, <a href="mailto:{D.FIRMA["email"]}">{D.FIRMA["email"]}</a>.') + f'''
<section class="sek"><div class="wrap dwie">
  <div>
    <div class="blok"><h2>Dane spółdzielni</h2><dl class="dane">
      <div><dt>Nazwa</dt><dd>{D.FIRMA["nazwa"]}</dd></div><div><dt>Adres</dt><dd>al. Zygmunta Krasińskiego 1, 31-111 Kraków</dd></div>
      <div><dt>Telefon</dt><dd><a href="{tel_href(D.FIRMA["tel"])}">{D.FIRMA["tel"]}</a></dd></div><div><dt>Faks</dt><dd>{D.FIRMA["faks"]}</dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:{D.FIRMA["email"]}">{D.FIRMA["email"]}</a></dd></div>
      <div><dt>KRS</dt><dd>{D.FIRMA["krs"]}</dd></div><div><dt>NIP</dt><dd>{D.FIRMA["nip"]}</dd></div><div><dt>REGON</dt><dd>{D.FIRMA["regon"]}</dd></div></dl></div>
    <div class="blok"><h2>Działy</h2><dl class="dane">{dz}</dl></div>
  </div>
  <form class="form" id="kontaktForm" novalidate>
    <h2>Napisz do nas</h2>
    <div class="pola"><label>Imię i nazwisko<input type="text" name="imie" autocomplete="name" required></label><label>E-mail<input type="email" name="email" autocomplete="email" required></label></div>
    <div class="pola"><label>Telefon (opcjonalnie)<input type="tel" name="tel" autocomplete="tel"></label><label>Temat<select name="temat"><option>Pytanie ogólne</option><option>Salon Eleganza</option><option>Bony dla firm</option><option>Wynajem</option><option>Praca</option><option>Aplikacja Jubilat</option></select></label></div>
    <label>Wiadomość<textarea name="wiad" rows="6" required></textarea></label>
    <label class="zgoda"><input type="checkbox" name="zgoda" required><span>Zgadzam się na przetwarzanie moich danych w celu odpowiedzi na wiadomość. Szczegóły w <a href="{Pp.a("polityka-prywatnosci/")}">polityce prywatności</a>.</span></label>
    <button class="btn btn-ciem" type="submit">Wyślij wiadomość</button>
    <p class="form-wynik" id="formWynik" role="status" hidden></p>
    {test_uw("formularz jest makietą - po uruchomieniu na WordPressie wiadomości trafią na info@jubilat.com.pl.")}
  </form>
</div></section>
<section class="sek" style="background:var(--szar)"><div class="wrap dwie">
  <div class="blok"><h2>Telefony do placówek</h2><dl class="dane">{pl}</dl></div>
  <div class="blok"><h2>Zarząd i kierownictwo</h2><dl class="zarzad">{zarz}</dl>
  <div class="mapa-mini" data-mapa="dh" role="region" aria-label="Mapa: siedziba spółdzielni"><p class="mapa-zast">Mapa wczyta się po przewinięciu.</p></div></div>
</div></section>'''
    strona("kontakt/", body=body, ld=[org_ld(), okruszki_ld([("Kontakt", "kontakt/")])], mob=("Napisz", "#kontaktForm"))


def s_polityka():
    Pp = P("polityka-prywatnosci/")
    tresc = f'''<h2>Administrator danych</h2><p>Administratorem danych osobowych jest {D.FIRMA["nazwa"]} z siedzibą w Krakowie, al. Zygmunta Krasińskiego 1, 31-111 Kraków, KRS {D.FIRMA["krs"]}, NIP {D.FIRMA["nip"]}. Kontakt: <a href="mailto:{D.FIRMA["email"]}">{D.FIRMA["email"]}</a>, tel. {D.FIRMA["tel"]}.</p>
<h2>Jakie dane i po co</h2><ul><li>Formularz kontaktowy i wiadomości e-mail: imię i nazwisko, adres e-mail, telefon i treść wiadomości - wyłącznie w celu odpowiedzi (art. 6 ust. 1 lit. f RODO, prawnie uzasadniony interes administratora, lub lit. b, gdy wiadomość dotyczy zawarcia umowy, np. najmu).</li>
<li>Rekrutacja: dane z CV przekazywane przez formularz eRecruiter lub e-mailem - w celu przeprowadzenia rekrutacji (art. 22¹ Kodeksu pracy, a w zakresie szerszym na podstawie zgody).</li>
<li>Aplikacja Jubilat: zasady przetwarzania danych w programie lojalnościowym opisuje regulamin aplikacji.</li></ul>
<h2>Jak długo</h2><p>Dane z korespondencji przechowujemy przez czas potrzebny do udzielenia odpowiedzi i ewentualnego dochodzenia roszczeń. Dane z rekrutacji - do jej zakończenia, a za zgodą także na potrzeby przyszłych rekrutacji.</p>
<h2>Odbiorcy danych</h2><p>Dane mogą być przekazywane podmiotom, które obsługują dla nas stronę, pocztę i systemy informatyczne, na podstawie umów powierzenia przetwarzania. Nie przekazujemy danych poza Europejski Obszar Gospodarczy.</p>
<h2>Twoje prawa</h2><p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia, wniesienia sprzeciwu oraz cofnięcia zgody w dowolnym momencie. Przysługuje Ci skarga do Prezesa Urzędu Ochrony Danych Osobowych.</p>
<h2>Pliki cookies i usługi zewnętrzne</h2><p>Strona nie używa plików cookies reklamowych ani analitycznych. W pamięci przeglądarki mogą być zapisywane wyłącznie ustawienia potrzebne do działania strony. Mapy placówek korzystają z kafelków OpenStreetMap, które wczytują się dopiero po przewinięciu do mapy; przy ich pobieraniu serwery OpenStreetMap otrzymują adres IP przeglądarki. Przyciski „Prowadź” otwierają Mapy Google w nowej karcie.</p>
<h2>Zmiany</h2><p>Aktualna wersja polityki prywatności jest zawsze dostępna na tej stronie.</p>'''
    body = ph(Pp, [("Polityka prywatności", "polityka-prywatnosci/")], "Polityka prywatności", "Jak Handlowa Spółdzielnia Jubilat przetwarza dane osób, które korzystają ze strony i kontaktują się z nami.") + f'<div class="prawny">{tresc}{test_uw("treść do weryfikacji przez Spółdzielnię (m.in. czy wyznaczono inspektora ochrony danych).")}</div>'
    strona("polityka-prywatnosci/", title="Polityka prywatności - Jubilat Kraków", desc="Polityka prywatności Handlowej Spółdzielni Jubilat w Krakowie: administrator danych, cele przetwarzania, prawa osób i pliki cookies.", body=body,
           ld=[okruszki_ld([("Polityka prywatności", "polityka-prywatnosci/")])])


def s_404():
    # 404 musi działać z dowolnej ścieżki - na GitHub Pages linki względem katalogu głównego projektu
    body = f'''<section class="ph e404"><div class="ph-in"><h1>Nie ma takiej strony</h1><p class="ph-lead">Adres mógł się zmienić po przebudowie strony. Spróbuj jednej z tych:</p>
<ul class="lista-kr" style="max-width:520px"><li><a class="link" href="ROOT/sklepy/">Sklepy i godziny otwarcia</a></li><li><a class="link" href="ROOT/eleganza/">Salon Eleganza</a></li><li><a class="link" href="ROOT/bary-mleczne/">Bary mleczne i menu tygodnia</a></li><li><a class="link" href="ROOT/gazetka/">Gazetka</a></li><li><a class="link" href="ROOT/kontakt/">Kontakt</a></li></ul>
<div class="ph-meta"><a class="btn btn-ciem" href="ROOT/">Strona główna</a></div></div></section>'''
    strona("404.html", title="Nie ma takiej strony - Jubilat", desc="Strona nie istnieje. Przejdź do strony głównej Jubilat.", body=body, noindex_extra=True)
    f = ROOT / "404.html"
    t = f.read_text(encoding="utf-8")
    root = "/jubilat-koncepcja" if D.PREVIEW else ""
    t = t.replace('href="ROOT/', f'href="{root}/').replace('href="./', f'href="{root}/').replace('src="assets/', f'src="{root}/assets/').replace('href="assets/', f'href="{root}/assets/')
    t = re.sub(r'href="(?!https?:|tel:|mailto:|#|/)([^"]+)"', lambda mm: f'href="{root}/{mm.group(1)}"', t)
    t = t.replace('data-root="./"', f'data-root="{root}/"')
    f.write_text(t, encoding="utf-8")


def s_przekierowania():
    # stary adres podglądu Eleganzy (link z wizualizacji) -> nowa podstrona
    (ROOT / "eleganza.html").write_text('<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>Salon Eleganza</title><meta name="robots" content="noindex"><link rel="canonical" href="' + B + '/eleganza/"><meta http-equiv="refresh" content="0; url=eleganza/"></head><body><a href="eleganza/">Salon Eleganza</a></body></html>', encoding="utf-8")


def mapa_i_robots():
    urls = "".join(f"<url><loc>{B}/{p}</loc><lastmod>{DZIS}</lastmod></url>" for p in STRONY)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    prod = f"User-agent: *\nAllow: /\n\nSitemap: {B}/sitemap.xml\n"
    (SRC / "robots_produkcja.txt").write_text(prod, encoding="utf-8")
    (ROOT / "robots.txt").write_text("# Wersja testowa - nie indeksować\nUser-agent: *\nDisallow: /\n" if D.PREVIEW else prod, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    zasoby()
    s_home(); s_sklepy()
    for p in SKLEPY:
        s_sklep(p)
    s_dh(); s_produkty(); s_eleganza(); s_bary()
    for b in BARY:
        s_bar(b)
    s_gazetka(); s_okazje(); s_niedziele(); s_lokale(); s_praca(); s_historia(); s_aktualnosci(); s_kontakt(); s_polityka(); s_404()
    s_przekierowania(); mapa_i_robots()
    print("Strony:", len(STRONY))
    for s in STRONY:
        print(" ", s or "/")
