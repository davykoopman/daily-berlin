"""Kwaliteitspoort voor open regels (Not listed) in launch_state.json:
  - bronlink niet (meer) bereikbaar        → Issues 'Source link inactive (auto-check)'
  - minder dan 3 verschillende foto's        → Issues 'Too few photos (auto-check)'
  - merknaam/logo-woorden in de titel        → Issues 'Brand name in title (auto-check)'
Daarna aanvullen met select_products.py --update en opnieuw photo_upgrade.py + quality_gate.py.

Gebruik:  python3 quality_gate.py [--min-fotos 3]
"""
import argparse, concurrent.futures as cf, json, re, sys
from pathlib import Path

import imagehash
import product_picker as pp
import photo_upgrade as pu

BASE = Path(__file__).parent
STATE = BASE / "listings/launch_state.json"
BRAND = re.compile(r"\b(nike|adidas|puma|ralph lauren|polo ralph|tommy hilfiger|lacoste|gucci|prada|chanel|dior|"
                   r"louis vuitton|burberry|north face|moncler|levi'?s|calvin klein|hugo boss|zara|ugg)\b", re.I)


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
            x.update(status="Issues", comment="Source link inactive (auto-check)", lister=""); n["dead"] += 1
            continue
        hs = [imagehash.hex_to_hash(h) for u, _, _ in g["imgs"][:12] if (h := hashes.get(pu.W(u)))]
        distinct = []
        for h in hs:
            if all(h - d > 4 for d in distinct):
                distinct.append(h)
        if len(distinct) < a.min_fotos:
            x.update(status="Issues", comment=f"Too few photos: {len(distinct)} (auto-check)", lister=""); n["few"] += 1
        elif BRAND.search(title_rest):
            x.update(status="Issues", comment="Brand name in title (auto-check)", lister=""); n["brand"] += 1
    STATE.write_text(json.dumps(state, ensure_ascii=False))
    print(f"{len(rows)} open regels gecontroleerd: {n}", file=sys.stderr)
    for s, v in state.items():
        print(f"  {s}: open {sum(1 for x in v if x['status'] == 'Not listed')}", file=sys.stderr)


if __name__ == "__main__":
    main()
