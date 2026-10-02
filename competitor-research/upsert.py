"""Voegt competitors toe aan data/competitors.csv of werkt ze bij (sleutel = domein).
Gebruik vanuit Python: upsert([dict(Land=..., Store=..., Domein=..., ...), ...])"""
import csv, datetime as dt
from pathlib import Path
P = Path(__file__).parent / "data/competitors.csv"
KEEP = ("Eerst gevonden", "Producten gekopieerd")

def upsert(rows):
    cur = list(csv.DictReader(open(P, encoding="utf-8")))
    F = list(cur[0].keys())
    idx = {r["Domein"]: r for r in cur}
    today = dt.date.today().isoformat()
    for n in rows:
        old = idx.get(n["Domein"])
        if old:
            for k, v in n.items():
                if k not in KEEP and v not in (None, ""):
                    old[k] = str(v)
            old["Laatst gecheckt"] = today
        else:
            r = {k: "" for k in F}
            r.update({k: str(v) for k, v in n.items() if v is not None})
            r.setdefault("Eerst gevonden", today); r["Eerst gevonden"] = r["Eerst gevonden"] or today
            r["Laatst gecheckt"] = today
            r["Producten gekopieerd"] = r["Producten gekopieerd"] or "nee"
            cur.append(r); idx[r["Domein"]] = r
    w = csv.DictWriter(open(P, "w", newline="", encoding="utf-8"), F); w.writeheader(); w.writerows(cur)
    return len(cur)
