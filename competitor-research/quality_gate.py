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
        if len(distinct) < a.min_fotos:
            x["_rej"] = f"Too few photos: {len(distinct)}"; n["few"] += 1
        elif BRAND.search(title_rest):
            x["_rej"] = "Brand name in title"; n["brand"] += 1
    reject(state)
    STATE.write_text(json.dumps(state, ensure_ascii=False))
    print(f"{len(rows)} open regels gecontroleerd: {n}", file=sys.stderr)
    for s, v in state.items():
        print(f"  {s}: open {sum(1 for x in v if x['status'] == 'Not listed')}", file=sys.stderr)


if __name__ == "__main__":
    main()
