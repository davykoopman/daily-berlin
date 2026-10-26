"""Welke uitschieters (data/google/standouts.json) ontbreken in welke eigen store?
Aanwezig = ≥2 verschillende foto's van de bestseller komen voor bij één product van die store (≤10)."""
import json, sys
from pathlib import Path
import numpy as np
import product_picker as pp, photo_upgrade as pu

BASE = Path(__file__).parent


def main(out):
    bs = json.loads((BASE / "data/google/standouts.json").read_text())
    cfg = json.loads((BASE / "config/stores.json").read_text())
    own = {}
    for s in cfg["stores"]:
        if s.get("_noot"):
            continue
        prods = pp.fetch_products(s["domein"], strict=True)
        gal = [(p["handle"], im["src"] + ("&" if "?" in im["src"] else "?") + "width=240") for p in prods for im in (p.get("images") or [])[:6]]
        hs = pp.hash_images([u for _, u in gal])
        own[s["naam"]] = [(hd, int(hs[u], 16)) for hd, u in gal if hs.get(u)]
    res, gaps = [], 0
    for dom, lst in bs.items():
        for b in lst:
            g = pu.gallery(dom, b["handle"])
            if not g:
                continue
            imgs = [u for u, _, _ in g["imgs"][:6]]
            hs = pp.hash_images([pu.W(u) for u in imgs])
            hh = [int(hs[pu.W(u)], 16) for u in imgs if hs.get(pu.W(u))]
            pres = {}
            for n, l2 in own.items():
                H = np.array([h for _, h in l2], dtype=np.uint64); hd = [x for x, _ in l2]; cnt = {}
                for h in hh:
                    for j in np.nonzero(np.bitwise_count(H ^ np.uint64(h)) <= 10)[0]:
                        cnt.setdefault(hd[j], set()).add(h)
                best = max(cnt.items(), key=lambda x: len(x[1]), default=(None, set()))
                pres[n] = best[0] if len(best[1]) >= 2 or (len(hh) <= 2 and best[1]) else None
            b["presence"], b["imgs"] = pres, imgs
            res.append(b); gaps += sum(v is None for v in pres.values())
            print(dom[:6], b["shop_title"][:45], " ".join(f"{k[:4]}:{'JA' if v else '--'}" for k, v in pres.items()))
    Path(out).write_text(json.dumps(res, ensure_ascii=False))
    print("gaten", gaps, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
