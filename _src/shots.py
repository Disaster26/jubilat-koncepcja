# -*- coding: utf-8 -*-
"""Zrzuty ekranu wszystkich stron: python _src/shots.py <runda> [filtr]
Wynik: _src/shots/<runda>/<strona>_<szer>x<wys>[_full].png + raport błędów konsoli, przewijania poziomego."""
import sys, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = sys.argv[3] if len(sys.argv) > 3 else "http://127.0.0.1:8793/"
runda = sys.argv[1] if len(sys.argv) > 1 else "r1"
filtr = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else ""
OUT = ROOT / "_src" / "shots" / runda
OUT.mkdir(parents=True, exist_ok=True)
VP = [(390, 844), (360, 640), (1440, 900), (1920, 1080)]
strony = [""] + [p.parent.relative_to(ROOT).as_posix() + "/" for p in sorted(ROOT.glob("**/index.html"))
                 if "wizualizacja" not in p.as_posix() and "_src" not in p.as_posix() and p.parent != ROOT] + ["404.html"]
strony = [s for s in strony if filtr in s] if filtr else strony
raport = []
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=str(Path.home() / "AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe"))
    for w, h in VP:
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=w < 768, has_touch=w < 768, locale="pl-PL", timezone_id="Europe/Warsaw")
        for s in strony:
            pg = ctx.new_page()
            bledy = []
            pg.on("console", lambda m: bledy.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda ex: bledy.append(str(ex)))
            pg.goto(BASE + s, wait_until="networkidle")
            pg.wait_for_timeout(300)
            nazwa = (s.strip("/").replace("/", "_") or "home").replace(".html", "")
            pg.screenshot(path=str(OUT / f"{nazwa}_{w}x{h}.png"))
            info = pg.evaluate("""() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
              wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'fixed' && r.width > 0 && !e.closest('.polka,.okazje-lista,.leaflet-container,dialog,.sr,.skip'); }).slice(0, 5).map(e => e.tagName + '.' + e.className),
              h1: document.querySelectorAll('h1').length})""")
            if w in (390, 1440):
                # przewiń całą stronę, żeby wczytać leniwe obrazy i mapy
                pg.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } await Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 3000); }))); window.scrollTo(0, 0); }")
                pg.wait_for_timeout(1200)
                pg.screenshot(path=str(OUT / f"{nazwa}_{w}x{h}_full.png"), full_page=True)
            if info["sw"] > info["cw"] or bledy or info["h1"] != 1:
                raport.append({"strona": s, "vp": f"{w}x{h}", "poziomo": info["sw"] - info["cw"], "elementy": info["wide"], "bledy": bledy[:5], "h1": info["h1"]})
            pg.close()
        ctx.close()
    br.close()
(OUT / "raport.json").write_text(json.dumps(raport, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(raport, ensure_ascii=False, indent=1)[:6000])
print("OK", len(strony), "stron")
