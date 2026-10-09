"""Zoekt voor een gelist product welke competitors hetzelfde product verkopen en wie de beste foto's heeft.

Gebruik:  python3 photo_compare.py <productlink van eigen store> [--sheet pad.png]

Werkwijze: foto's van jouw product → fotovergelijking met de hoofdfoto's in .cache/pool.json
(generieke foto's zoals maattabellen worden overgeslagen) → per treffer de volledige galerij ophalen
(aantal foto's, resolutie) → gesorteerd op resolutie, dan aantal foto's, dan grootte van de store.
"""
import argparse, concurrent.futures as cf, csv, io, json, re
from pathlib import Path

import imagehash
import product_picker as pp

BASE = Path(__file__).parent
W = lambda u: u + ("&" if "?" in u else "?") + "width=240"
fix = lambda u: ("https:" + u) if u.startswith("//") else u


def gallery(store, handle):
    try:
        d = json.loads(pp.get(f"https://{store}/products/{handle}.js", timeout=25))
    except Exception:
        return None
    med = [m for m in d.get("media", []) if m.get("media_type") == "image"]
    return dict(title=d["title"], price=d["price"] / 100,
                imgs=[(fix(m["src"]), m.get("width") or 0, m.get("height") or 0) for m in med])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--sheet")
    a = ap.parse_args()
    m = re.match(r"https?://([^/]+)/products/([^/?#]+)", a.url)
    own_store, own_handle = m.group(1).replace("www.", ""), m.group(2)
    own = gallery(own_store, own_handle)
    print(f"Jouw product: {own['title']} | {len(own['imgs'])} foto's | 1e {own['imgs'][0][1]}×{own['imgs'][0][2]}")
    pool = json.loads((BASE / ".cache/pool.json").read_text())
    prods = [r for r in pool["products"] if r.get("phash")]
    allh = [imagehash.hex_to_hash(r["phash"]) for r in prods]
    rh = pp.hash_images([W(u) for u, _, _ in own["imgs"][:10]])
    refs = []
    for u, _, _ in own["imgs"][:10]:
        h = rh.get(W(u))
        if not h:
            continue
        h = imagehash.hex_to_hash(h)
        hits = [i for i, x in enumerate(allh) if h - x <= 5]
        if 0 < len(hits) <= 40:           # >40 treffers = generieke foto (maattabel e.d.)
            refs.append((h, hits))
    idx = sorted({i for _, hits in refs for i in hits})
    cands = {(prods[i]["store"], prods[i]["handle"]) for i in idx}
    vis = {r["Domein"]: (int(r["Bezoekers per maand"] or 0), r["Paid search"]) for r in
           csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8"))}
    import select_products as sp
    sp.load_eligible()
    with cf.ThreadPoolExecutor(10) as ex:
        res = list(ex.map(lambda c: (c, gallery(*c)), sorted(cands)))
    rows = []
    for (st, hd), g in res:
        if not g or not g["imgs"]:
            continue
        res_ = sorted(min(w, h) for _, w, h in g["imgs"])
        rows.append(dict(store=st, url=f"https://{st}/products/{hd}", title=g["title"], n=len(g["imgs"]),
                         first=f"{g['imgs'][0][1]}×{g['imgs'][0][2]}", res=res_[len(res_) // 2],
                         visits=vis.get(st, (0, ""))[0], source=st in sp.ELIGIBLE, imgs=g["imgs"]))
    rows.sort(key=lambda r: (-r["res"], -r["n"], -r["visits"]))
    print(f"{len(rows)} competitors met hetzelfde product:")
    for r in rows:
        print(f"  {'✅' if r['source'] else '  '} {r['store']:28} {r['visits']/1000:6.0f}K | {r['n']:2} foto's | 1e {r['first']:10} | "
              f"mediaan {r['res']}px | {r['url']}")
    if a.sheet and rows:
        from PIL import Image, ImageDraw
        def load(u):
            try:
                return Image.open(io.BytesIO(pp.get(W(u), binary=True))).convert("RGB").resize((150, 150))
            except Exception:
                return Image.new("RGB", (150, 150), "grey")
        show = [dict(store="JOUW PRODUCT", n=len(own["imgs"]), res=min(own["imgs"][0][1:]), visits=0, imgs=own["imgs"])] + rows[:14]
        sheet = Image.new("RGB", (150 * 9, 170 * len(show)), "white")
        dr = ImageDraw.Draw(sheet)
        for i, r in enumerate(show):
            dr.text((3, i * 170 + 3), r["store"][:20], fill="black")
            dr.text((3, i * 170 + 20), f"{r['n']} foto's, {r['res']}px", fill="black")
            dr.text((3, i * 170 + 37), f"{r['visits'] // 1000}K", fill="black")
            with cf.ThreadPoolExecutor(8) as ex:
                ims = list(ex.map(load, [u for u, _, _ in r["imgs"][:8]]))
            for j, im in enumerate(ims):
                sheet.paste(im, (150 * (j + 1), i * 170 + 10))
        sheet.save(a.sheet)


if __name__ == "__main__":
    main()
