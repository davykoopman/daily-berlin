"""Eigen bestsellers die in een andere eigen store ontbreken → items voor add_prio.py.

  python3 transfers.py <presence.json> <out.json> --stores Niaali Migesi "Vinci Fashion"

Per gat: beste versie van HETZELFDE product bij een competitor (≥2 van de eerste 4 foto's gelijk, leverbaar,
liefst niet uit de markt van die store, beste foto-score), anders de eigen-store-link. Herenstores (gender M)
krijgen alleen herenproducten (of unisex)."""
import argparse, concurrent.futures as cf, json, re
from pathlib import Path
import numpy as np
import imagehash
import product_picker as pp, photo_upgrade as pu, bestsellers_google as bg

BASE = Path(__file__).parent
MEN = re.compile(r"uomo|herren|męsk|mesk|\bmen'?s?\b|homme|hombre|unisex", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("presence"); ap.add_argument("out"); ap.add_argument("--stores", nargs="*")
    a = ap.parse_args()
    bs = json.loads(Path(a.presence).read_text())
    cfg = json.loads((BASE / "config/stores.json").read_text())
    fx = cfg["fx_naar_eur"]; st = {s["naam"]: s for s in cfg["stores"]}
    pool = json.loads((BASE / ".cache/pool.json").read_text()); P = [r for r in pool["products"] if r.get("phash")]
    mo = {s["domain"]: s["market"] for s in pool["stores"]}; cur = {s["domain"]: s["currency"] for s in pool["stores"]}
    cur.update({x["domein"]: x["valuta"] for x in cfg["stores"]})
    H = np.array([int(r["phash"], 16) for r in P], dtype=np.uint64)
    pat = pp.compile_keywords(json.loads((BASE / "config/seasons.json").read_text()))
    items = []
    for b in bs:
        need = [n for n, v in b["presence"].items() if v is None and (not a.stores or n in a.stores)]
        need = [n for n in need if st[n].get("gender") != "M" or MEN.search(b["shop_title"])]
        if not need:
            continue
        hs = pp.hash_images([pu.W(u) for u in b["imgs"]]); hh = [int(hs[pu.W(u)], 16) for u in b["imgs"] if hs.get(pu.W(u))]
        vers = set()
        for h in hh[:6]:
            for j in np.nonzero(np.bitwise_count(H ^ np.uint64(h)) <= 5)[0]: vers.add((P[j]["store"], P[j]["handle"]))
        with cf.ThreadPoolExecutor(5) as ex: G = dict(zip(vers, ex.map(lambda k: pu.gallery(*k), vers)))
        gh = pp.hash_images([pu.W(u) for g in G.values() if g for u, _, _ in g["imgs"][:12]])
        ref = [imagehash.hex_to_hash(f"{h:016x}") for h in hh[:6]]
        good = []
        for k, g in G.items():
            if not g or not g["imgs"] or not g["avail"]: continue
            mine = [imagehash.hex_to_hash(gh[pu.W(u)]) for u, _, _ in g["imgs"][:4] if gh.get(pu.W(u))]
            if sum(1 for h in mine if any(h - r <= 5 for r in ref)) < 2: continue
            good.append(dict(k=k, q=pu.quality(g, gh)[0], n=len(g["imgs"]), market=mo.get(k[0])))
        base = float(b["price"]) * fx[cur.get(b["store"], "EUR")] if not isinstance(b["price"], str) or b["price"].replace(".", "").isdigit() else bg.num(b["price"]) * fx[cur.get(b["store"], "EUR")]
        cat = pp.categorize({"title": b["shop_title"]}, pat)
        g_ = "M" if MEN.search(b["shop_title"]) else "W"
        own = {x["domein"]: x["naam"] for x in cfg["stores"]}.get(b["store"], b["store"])
        for n in need:
            cand = [v for v in good if v["market"] not in st[n]["markten"]] or good
            cand.sort(key=lambda v: (-v["q"], -v["n"]))
            if cand:
                url = f"https://{cand[0]['k'][0]}/products/{cand[0]['k'][1]}"; src = cand[0]["k"][0]
            else:
                url = f"https://{b['store']}/products/{b['handle']}"; src = f"{own} (own store)"
            items.append(dict(url=url, title=b["shop_title"], cat=cat, gender=g_, base_eur=round(base, 2), src_cur=cur.get(url.split("/")[2], "EUR"),
                              why=f"Bestseller in {own}: €{b['value']:.0f} revenue, {b.get('conv', 0)} orders (Shopify, last 21 days) – missing in this store",
                              stores=[n], presence_checked=True, davento_price=(n == "Niaali"), source_label=f"{src} · bestseller {own}"))
            print(n, b["shop_title"][:45], url)
    Path(a.out).write_text(json.dumps(items, ensure_ascii=False, indent=1)); print(len(items))


if __name__ == "__main__":
    main()
