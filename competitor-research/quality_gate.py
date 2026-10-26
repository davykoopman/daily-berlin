"""Kwaliteitspoort voor open regels (Not listed) in launch_state.json. Afgekeurde regels gaan UIT de Launch File
(listers zien alleen goede producten) en naar listings/rejected.json, zodat ze nooit opnieuw worden voorgesteld:
  - bronlink niet (meer) bereikbaar (echte 404)
  - minder dan 3 verschillende foto's
  - merknaam/logo-woorden in de titel
Daarna aanvullen met select_products.py --update en opnieuw photo_upgrade.py + quality_gate.py.

Gebruik:  python3 quality_gate.py [--min-fotos 3]
"""
import argparse, concurrent.futures as cf, json, re, sys
from pathlib import Path

import datetime
import imagehash
import product_picker as pp
import photo_upgrade as pu

BASE = Path(__file__).parent
STATE = BASE / "listings/launch_state.json"
BRAND = re.compile(r"\b(nike|adidas|puma|ralph lauren|polo ralph|tommy hilfiger|lacoste|gucci|prada|chanel|dior|"
                   r"louis vuitton|burberry|north face|moncler|levi'?s|calvin klein|hugo boss|zara|ugg)\b", re.I)


REJ = BASE / "listings/rejected.json"


def reject(state):
    """Regels met _rej (of een oude auto-check Issues-markering) uit de file halen en vastleggen in rejected.json."""
    rej = json.loads(REJ.read_text()) if REJ.exists() else []
    today = datetime.date.today().isoformat()
    for s in state:
        keep = []
        for x in state[s]:
            why = x.pop("_rej", None)
            c = x.get("comment") or ""
            if not why and x["status"] in ("Issues", "Duplicate") and ("(auto-check)" in c or "(photo upgrade)" in c):
                why = c   # automatisch afgekeurd (niet door een lister): hoort niet in de file
            if why:
                rej.append(dict(store=s, url=x["url"], title=x["title"], reason=why, date=today))
            else:
                keep.append(x)
        state[s] = keep
    REJ.write_text(json.dumps(rej, ensure_ascii=False, indent=0))


def dedupe(state, rows, gals, hashes):
    """Les uit de file van 26-10 (121 x 'Already in store'): na de foto-upgrade opnieuw controleren
    (1) tegen de ACTUELE store-catalogus (eerste 8 foto's vs eerste 8 van elk eigen product, ≤12) en
    (2) open regels binnen dezelfde store tegen elkaar (zelfde product via twee links): ≥2 foto's ≤8 of hoofdfoto ≤6.
    Bij (2) blijft de bovenste regel (prioriteit/lijstvolgorde) staan."""
    import numpy as np
    cfg = json.loads((BASE / "config/stores.json").read_text())
    dom = {x["naam"]: x["domein"] for x in cfg["stores"]}
    gal_of = {id(x): g for x, g in zip(rows, gals)}
    n_own = n_dup = 0
    for store, srows in state.items():
        prods = pp.fetch_products(dom[store], strict=True)
        og = [im["src"] + ("&" if "?" in im["src"] else "?") + "width=240" for p in prods for im in (p.get("images") or [])[:8]]
        oh = pp.hash_images(og)
        OH = np.array([int(h, 16) for h in oh.values() if h], dtype=np.uint64)
        seen = []          # (main, [hashes]) van eerdere open regels
        for x in srows:
            if x["status"] != "Not listed" or x.get("_rej"):
                continue
            g = gal_of.get(id(x))
            if not g or not g["imgs"]:
                continue
            hh = [int(hashes[pu.W(u)], 16) for u, _, _ in g["imgs"][:8] if hashes.get(pu.W(u))]
            if not hh:
                continue
            # generieke foto's (maattabel e.d.) die bij veel eigen producten terugkomen tellen niet mee
            def hit(h):
                n = int(np.count_nonzero(np.bitwise_count(OH ^ np.uint64(h)) <= 12))
                return 0 < n < 15
            if len(OH) and any(hit(h) for h in hh):
                x["_rej"] = "Already in store (auto-check)"; n_own += 1
                continue
            dup = False
            for main, prev in seen:
                same = sum(1 for h in hh if any(bin(h ^ q).count("1") <= 8 for q in prev))
                if same >= 2 or bin(hh[0] ^ main).count("1") <= 6:
                    dup = True
                    break
            if dup:
                x["_rej"] = "Same product twice in list (auto-check)"; n_dup += 1
                continue
            seen.append((hh[0], hh))
    print(f"  dedupe: {n_own} al in store, {n_dup} dubbel in lijst", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-fotos", type=int, default=3)
    a = ap.parse_args()
    state = json.loads(STATE.read_text())
    rows = [x for v in state.values() for x in v if x["status"] == "Not listed"]
    key = lambda x: (x["url"].split("/")[2], x["url"].split("/")[4].split("?")[0])
    with cf.ThreadPoolExecutor(6) as ex:
        gals = list(ex.map(lambda x: pu.gallery(*key(x)), rows))
    hashes = pp.hash_images([pu.W(u) for g in gals if g for u, _, _ in g["imgs"][:12]])
    n = {"dead": 0, "few": 0, "brand": 0}
    for x, g in zip(rows, gals):
        # 'Chanel - …' bij Look de Paris is een productnaam, geen merk: alleen als het merk ná het eerste woord staat tellen we het
        title_rest = x["title"].split(" ", 1)[1] if " " in x["title"] else ""
        if not g:
            continue          # tijdelijk onbereikbaar (rate limit): niet afkeuren, volgende ronde opnieuw
        if g.get("dead") or not g["imgs"]:
            x["_rej"] = "Source link inactive"; n["dead"] += 1
            continue
        hs = [imagehash.hex_to_hash(h) for u, _, _ in g["imgs"][:12] if (h := hashes.get(pu.W(u)))]
        distinct = []
        for h in hs:
            if all(h - d > 4 for d in distinct):
                distinct.append(h)
        if not pu.enough_photos(g, len(distinct), a.min_fotos):
            x["_rej"] = f"Too few photos: {len(distinct)}"; n["few"] += 1
        elif BRAND.search(title_rest):
            x["_rej"] = "Brand name in title"; n["brand"] += 1
    dedupe(state, rows, gals, hashes)
    reject(state)
    STATE.write_text(json.dumps(state, ensure_ascii=False))
    print(f"{len(rows)} open regels gecontroleerd: {n}", file=sys.stderr)
    for s, v in state.items():
        print(f"  {s}: open {sum(1 for x in v if x['status'] == 'Not listed')}", file=sys.stderr)


if __name__ == "__main__":
    main()
