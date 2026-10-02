"""Herberekent alleen de productgroepen in .cache/pool.json (zonder opnieuw te downloaden)."""
import json, collections
from pathlib import Path
import pool
P = Path(__file__).parent / ".cache/pool.json"
d = json.loads(P.read_text())
cl = pool.cluster([r for r in d["products"] if r.get("phash")])
for r in d["products"]:
    r["cluster"] = cl.get(f'{r["store"]}/{r["handle"]}')
P.write_text(json.dumps(d, ensure_ascii=False))
g = collections.defaultdict(set)
for r in d["products"]:
    if r["cluster"]:
        g[r["cluster"]].add(r["store"])
print("groepen:", len(g), "verdeling stores/groep:", sorted(collections.Counter(min(len(v), 10) for v in g.values()).items()))
