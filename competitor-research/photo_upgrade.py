"""Vervangt voor alle open regels (Not listed) in launch_state.json de importlink door de beste versie van
HETZELFDE product bij een andere competitor. Er komen geen kolommen bij; alleen link, foto-info, bron en
foto-advies worden bijgewerkt. De adviesprijs blijft gebaseerd op de bewijsbron (≥75K bestseller).

Score per versie (afgesproken met Davy, 9-10):
  conversie (55%) = bestseller-positie in die store × grootte van de store
  kwaliteit (45%) = resolutie (tot 2000 px), aantal verschillende foto's, staande foto's
  − grote aftrek als die store in het land van jouw store adverteert
Kleuren tellen niet mee (leverancier-beschikbaarheid onbekend).
Wisselen alleen als de nieuwe versie duidelijk beter scoort (+0,05).

Gebruik:  python3 photo_upgrade.py [--store Niaali ...] [--dry-run]
"""
import argparse, concurrent.futures as cf, csv, json, math, sys
from pathlib import Path

import imagehash
import product_picker as pp

BASE = Path(__file__).parent
STATE = BASE / "listings/launch_state.json"
W = lambda u: u + ("&" if "?" in u else "?") + "width=240"
fix = lambda u: ("https:" + u) if str(u).startswith("//") else u


def gallery(store, handle, tries=3):
    """None = tijdelijk niet op te halen (429/5xx/timeout); dead=True alleen bij een echte 404."""
    import time, urllib.error
    for i in range(tries):
        try:
            d = json.loads(pp.get(f"https://{store}/products/{handle}.js", timeout=25))
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return dict(imgs=[], avail=False, dead=True)
        except Exception:
            pass
        time.sleep(3 * (i + 1))
    else:
        return None
    med = [m for m in d.get("media", []) if m.get("media_type") == "image"]
    v = d.get("variants") or []
    return dict(imgs=[(fix(m["src"]), m.get("width") or 0, m.get("height") or 0) for m in med],
                avail=bool(v) and sum(1 for x in v if x.get("available")) >= max(1, 0.5 * len(v)))


def quality(g, hashes):
    imgs = g["imgs"]
    if not imgs:
        return 0.0, 0
    res = sorted(min(w, h) for _, w, h in imgs)
    med = res[len(res) // 2]
    # aantal VERSCHILLENDE foto's (bijna-identieke tellen één keer)
    hs = [imagehash.hex_to_hash(h) for u, _, _ in imgs[:12] if (h := hashes.get(W(u)))]
    distinct = []
    for h in hs:
        if all(h - d > 4 for d in distinct):
            distinct.append(h)
    w, h = imgs[0][1], imgs[0][2]
    portrait = 1.0 if w and 1.15 <= h / w <= 1.55 else 0.6 if w and 0.95 <= h / w < 1.15 else 0.3
    q = 0.5 * min(med, 2000) / 2000 + 0.3 * min(len(distinct), 10) / 10 + 0.2 * portrait
    return q, len(distinct)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = json.loads((BASE / "config/stores.json").read_text())
    mk = {s["naam"]: s["markten"] for s in cfg["stores"]}
    comp = {r["Domein"]: r for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8"))}
    visits = lambda d: int(comp.get(d, {}).get("Bezoekers per maand") or 0)
    names = {d: r["Store"] for d, r in comp.items()}
    pool = json.loads((BASE / ".cache/pool.json").read_text())
    market_of = {s["domain"]: s["market"] for s in pool["stores"]}
    prods = [r for r in pool["products"] if r.get("phash")]
    P = {(r["store"], r["handle"]): r for r in pool["products"]}
    import numpy as np
    H = np.array([int(r["phash"], 16) for r in prods], dtype=np.uint64)

    def dists(h):
        x = H ^ np.uint64(int(str(h), 16))
        return np.bitwise_count(x) if hasattr(np, "bitwise_count") else np.array([bin(int(v)).count("1") for v in x])
    state = json.loads(STATE.read_text())
    stores = [s for s in state if not a.store or s in a.store]

    rows = [(s, x) for s in stores for x in state[s] if x["status"] == "Not listed"]
    print(f"{len(rows)} open regels", file=sys.stderr)
    cur_key = lambda x: (x["url"].split("/")[2], x["url"].split("/")[4].split("?")[0])

    # Fase 1: galerij van de huidige bron
    with cf.ThreadPoolExecutor(16) as ex:
        cur = dict(zip([cur_key(x) for _, x in rows], ex.map(lambda t: gallery(*cur_key(t[1])), rows)))
    hashes = pp.hash_images([W(u) for g in cur.values() if g for u, _, _ in g["imgs"][:4]])
    # Fase 2: kandidaten = pool-producten waarvan de hoofdfoto overeenkomt met één van onze eerste 4 foto's
    cand = {}
    for s, x in rows:
        g = cur.get(cur_key(x))
        if not g:
            continue
        ref = [imagehash.hex_to_hash(h) for u, _, _ in g["imgs"][:4] if (h := hashes.get(W(u)))]
        found = []
        if ref:
            dm = np.min(np.stack([dists(r) for r in ref]), axis=0)
            for i in np.nonzero(dm <= 5)[0]:
                found.append((int(dm[i]), -visits(prods[i]["store"]), (prods[i]["store"], prods[i]["handle"])))
        found = [k for _, _, k in sorted(found) if k != cur_key(x)]
        cand[(s, x["url"])] = list(dict.fromkeys(found))[:8]
    need = sorted({k for v in cand.values() for k in v})
    print(f"{len(need)} alternatieve versies ophalen ...", file=sys.stderr)
    with cf.ThreadPoolExecutor(16) as ex:
        gal = dict(zip(need, ex.map(lambda k: gallery(*k), need)))
    gal.update(cur)
    hashes = pp.hash_images([W(u) for g in gal.values() if g for u, _, _ in g["imgs"][:12]])

    def first_hashes(g, n=4):
        return [imagehash.hex_to_hash(h) for u, _, _ in g["imgs"][:n] if (h := hashes.get(W(u)))]

    def medres(g):
        r = sorted(min(w, h) for _, w, h in g["imgs"]) or [0]
        return r[len(r) // 2]

    def score(k, g, markets):
        r = P.get(k)
        pct = r["pct"] if r else 0.3
        v = visits(k[0]) or 20000
        conv = 0.6 * pct + 0.4 * min(math.log10(v) / math.log10(1_700_000), 1.0)
        q, nd = quality(g, hashes)
        dom = market_of.get(k[0]) in markets
        first = min(g["imgs"][0][1], g["imgs"][0][2]) if g["imgs"] else 0
        return dict(total=0.55 * conv + 0.45 * q - (0.5 if dom else 0), conv=conv, q=q, nd=nd, dom=dom, res=medres(g),
                    n=len(g["imgs"]), first=first)

    def acceptable(new, old, same_main):
        """Alleen wisselen bij echte winst (regel Davy 9-10): nooit minder foto's, nooit een minder scherpe
        eerste foto, nooit naar >20% lagere mediaan-resolutie."""
        if new["dom"] and not old["dom"]:
            return False
        if new["res"] < 0.8 * old["res"] or new["n"] < old["n"] or new["first"] < old["first"]:
            return False
        better_photos = new["q"] >= old["q"] + 0.05
        better_main = (not same_main) and new["conv"] >= old["conv"] + 0.10 and new["q"] >= old["q"] - 0.03
        return better_photos or better_main

    changed, report = 0, []
    for s, x in rows:
        k0 = cur_key(x)
        g0 = gal.get(k0)
        if not g0 or not g0["imgs"]:
            continue
        markets = mk[s]
        best_k, best = k0, score(k0, g0, markets)
        base = best
        ref = first_hashes(g0)
        for k in cand.get((s, x["url"]), []):
            g = gal.get(k)
            if not g or not g["imgs"] or not g["avail"]:
                continue
            # hetzelfde product? minstens 2 overeenkomende foto's tussen de eerste 4 van beide galerijen
            mine = first_hashes(g)
            if sum(1 for h in mine if any(h - r <= 5 for r in ref)) < 2:
                continue
            sc = score(k, g, markets)
            same_main = bool(mine) and bool(ref) and (mine[0] - ref[0] <= 5)
            if acceptable(sc, base, same_main) and sc["total"] > best["total"]:
                best_k, best = k, sc
        # foto-advies: hoofdfoto gelijk aan die van een concurrent in jouw markt?
        gb = gal[best_k]
        rivals_main = [imagehash.hex_to_hash(P[k]["phash"]) for k in cand.get((s, x["url"]), [])
                       if k in P and P[k].get("phash") and market_of.get(k[0]) in markets]
        fh = first_hashes(gb, 12)
        note = "Main photo free to use (no competitor in your market uses it)"
        if fh and any(fh[0] - r <= 5 for r in rivals_main):
            alt = next((i for i, h in enumerate(fh) if i and all(h - r > 5 for r in rivals_main)), None)
            note = (f"Same main photo as a competitor in your market → use photo {alt + 1} as main" if alt is not None
                    else "Same main photo as a competitor in your market → use a supplier/model photo as main")
        if best_k != k0:
            changed += 1
            q0 = quality(g0, hashes)
            report.append((s, x["title"][:50], f"{k0[0]} → {best_k[0]}", f"{base['res']}px/{q0[1]} → "
                           f"{best['res']}px/{best['nd']} foto's"))
            x["url"] = f"https://{best_k[0]}/products/{best_k[1]}"
            x["img"] = gb["imgs"][0][0] + ("&" if "?" in gb["imgs"][0][0] else "?") + "width=240"
            x["source"] = f"{names.get(best_k[0], best_k[0])} ({visits(best_k[0]) / 1000:.0f}K)" if visits(best_k[0]) else names.get(best_k[0], best_k[0])
            x["market"] = market_of.get(best_k[0], x["market"])
            x["own_market"] = best["dom"]
            x["price_note"] = (x.get("price_note") or "") + "; photos from best-converting version, price from proven bestseller"
        x["img_txt"] = f"{len(gb['imgs'])} photos, 1st {gb['imgs'][0][1]}×{gb['imgs'][0][2]}"
        x["img_score"] = round(100 * quality(gb, hashes)[0])
        x["photo_note"] = note
    # geen dubbele links binnen één store
    for s in stores:
        seen = set()
        for x in state[s]:
            if x["status"] == "Not listed" and x["url"] in seen:
                x["status"], x["comment"] = "Duplicate", "Same product twice in list (photo upgrade)"
            seen.add(x["url"])
    print(f"{changed} van {len(rows)} links vervangen", file=sys.stderr)
    for r in report[:40]:
        print("  ", " | ".join(r), file=sys.stderr)
    by = {}
    for r in report:
        by[r[0]] = by.get(r[0], 0) + 1
    print("per store:", by, file=sys.stderr)
    if not a.dry_run:
        STATE.write_text(json.dumps(state, ensure_ascii=False))


if __name__ == "__main__":
    main()
