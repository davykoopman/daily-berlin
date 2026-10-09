"""Seizoensbeeld per markt, gemeten aan wat grote competitors NU doen (uit .cache/pool.json):
  - aandeel per categorie van de producten die ze de afgelopen N dagen live zetten (waar zetten ze op in);
  - aandeel per categorie van die nieuwe producten die al in hun top 25% bestsellers staan (wat verkoopt nu).

Gebruik:  python3 season_report.py [--dagen 14] [--min-bezoekers 75000]
"""
import argparse, collections, csv, json
from pathlib import Path

BASE = Path(__file__).parent
CAT_EN = {"Winterjas": "Winter coat", "Tussenjas": "Transition jacket", "Trui / hoodie": "Sweater/hoodie",
          "Vest / cardigan": "Cardigan", "Blazer": "Blazer", "Laarzen": "Boots", "Broek": "Trousers", "Jurk": "Dress",
          "Blouse / shirt": "Blouse/shirt", "Set": "Set", "Schoenen": "Shoes", "T-shirt / top": "T-shirt/top",
          "Shorts": "Shorts", "Sandalen": "Sandals", "Badmode": "Swimwear", "Overig": "Other"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dagen", type=int, default=14)
    ap.add_argument("--min-bezoekers", type=int, default=75000)
    a = ap.parse_args()
    vis = {r["Domein"]: int(r["Bezoekers per maand"] or 0) for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8"))}
    pool = json.loads((BASE / ".cache/pool.json").read_text())
    new, hot, stores = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter), collections.defaultdict(set)
    for r in pool["products"]:
        if vis.get(r["store"], 0) < a.min_bezoekers or r["age"] > a.dagen:
            continue
        m = r["market"]
        stores[m].add(r["store"])
        new[m][r["cat"]] += 1
        if r["pct"] >= 0.75:
            hot[m][r["cat"]] += 1
    out = {}
    for m in sorted(new, key=lambda k: -sum(new[k].values())):
        tot, th = sum(new[m].values()), sum(hot[m].values())
        print(f"\n== {m}: {len(stores[m])} grote stores, {tot} nieuwe producten in {a.dagen} dagen, {th} daarvan al top-25%")
        rows = []
        for c, n in new[m].most_common(10):
            h = hot[m][c]
            rows.append((CAT_EN.get(c, c), round(100 * n / tot), round(100 * h / th) if th else 0))
            print(f"   {CAT_EN.get(c, c):18} toegevoegd {100 * n / tot:4.0f}%   | verkoopt (top-25%) {100 * h / th if th else 0:4.0f}%")
        out[m] = dict(stores=sorted(stores[m]), n_new=tot, n_hot=th, rows=rows)
    (BASE / ".cache/season_report.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
