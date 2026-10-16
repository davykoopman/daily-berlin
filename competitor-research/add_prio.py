"""Zet bestseller-regels (P) bovenaan de nieuwe regels van elke store in launch_state.json.

Invoer: JSON-lijst met items {url, title, cat, gender, base_eur, why, stores: [...]} (stores = waar het moet komen).
Per store gecontroleerd: link actief, ≥3 verschillende foto's, ≥50% maten leverbaar, niet al in de store (≤12 op de
eerste 6 foto's), niet al in de Launch File. Prijs = base_eur (prijsniveau van de eigen bestseller) omgerekend,
nooit onder de bronprijs.

Gebruik:  python3 add_prio.py <items.json> [--dry-run]
"""
import argparse, datetime as dt, json, sys
from pathlib import Path
import imagehash
import numpy as np
import product_picker as pp
import photo_upgrade as pu
import select_products as sp

BASE = Path(__file__).parent
STATE = BASE / "listings/launch_state.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    items = json.loads(Path(a.items).read_text())
    cfg = json.loads((BASE / "config/stores.json").read_text())
    stores = {s["naam"]: s for s in cfg["stores"] if not s.get("_noot")}
    fx = cfg["fx_naar_eur"]
    state = json.loads(STATE.read_text())
    today = dt.date.today().isoformat()
    pool = json.loads((BASE / ".cache/pool.json").read_text())
    market_of = {s["domain"]: s["market"] for s in pool["stores"]}
    own = {}
    for n, s in stores.items():
        prods = pp.fetch_products(s["domein"])
        gal = [im["src"] + ("&" if "?" in im["src"] else "?") + "width=240" for p in prods for im in (p.get("images") or [])[:6]]
        own[n] = np.array([int(h, 16) for h in pp.hash_images(gal).values() if h], dtype=np.uint64)
    added = {n: [] for n in stores}
    for it in items:
        st_, hd = it["url"].split("/")[2], it["url"].split("/")[4].split("?")[0]
        g = pu.gallery(st_, hd)
        if not g or not g["imgs"] or not g["avail"]:
            print("  x niet actief/leverbaar:", it["url"], file=sys.stderr); continue
        hs = pp.hash_images([pu.W(u) for u, _, _ in g["imgs"][:12]])
        hh = [imagehash.hex_to_hash(hs[pu.W(u)]) for u, _, _ in g["imgs"][:12] if hs.get(pu.W(u))]
        distinct = []
        for h in hh:
            if all(h - d > 4 for d in distinct):
                distinct.append(h)
        own_link = st_ in {x["domein"] for x in stores.values()}
        if not own_link and not pu.enough_photos(g, len(distinct)):
            print("  x <3 foto's:", it["url"], file=sys.stderr); continue
        first6 = [int(str(h), 16) for h in hh[:6]]
        try:
            src_price = json.loads(pp.get(f"https://{st_}/products/{hd}.js"))["price"] / 100
        except Exception:
            src_price = 0
        src_cur = it.get("src_cur", "EUR")
        for n in it["stores"]:
            s = stores[n]
            if any(x["url"].split("?")[0] == it["url"] for x in state.get(n, [])):
                continue
            if not it.get("presence_checked") and len(own[n]) and any(int(np.min(np.bitwise_count(own[n] ^ np.uint64(h)))) <= 12 for h in first6[:4]):
                continue
            floor = src_price * fx.get(src_cur, 1.0)
            eur = max(it["base_eur"], floor)
            price = sp.round_price(eur, s["valuta"], fx)
            in_m = market_of.get(st_) in s["markten"]
            row = dict(key=f"prio/{st_}/{hd}", url=it["url"], title=g.get("title") or it["title"], cat=sp.CAT_EN.get(it["cat"], it["cat"]),
                       gender=it["gender"], week="1", strat=it.get("strat", "P"), score=999 if it.get("strat", "P") == "P" else 500, why=it["why"], price=price, band="",
                       price_note=("take over the source link price" if it.get("strat") == "A" else
                                   "price level of your own bestseller" + (f" (source sells at {src_price:.2f} {src_cur})" if src_price else "")),
                       source=it.get("source_label") or st_, market=market_of.get(st_, ""), own_market=in_m,
                       img_score=round(100 * pu.quality(g, hs)[0]), img_txt=f"{len(g['imgs'])} photos, 1st {g['imgs'][0][1]}×{g['imgs'][0][2]}",
                       photo_note=("Proven bestseller bag – list early" if it.get("strat") == "A" else "Proven type in your own stores – list first"), alts=[], img=pu.W(g["imgs"][0][0]), added=today,
                       lister="", status="Not listed", comment="", name="", prio=True)
            added[n].append(row)
    for n, rows in added.items():
        if not rows:
            continue
        cur = state.get(n, [])
        # na de bestaande regels, vóór de andere nieuwe regels van vandaag
        old = [x for x in cur if x.get("added") != today or x.get("prio")]
        new = [x for x in cur if x.get("added") == today and not x.get("prio")]
        state[n] = old + rows + new
        print(f"  {n}: +{len(rows)} bestseller-regels", file=sys.stderr)
    if not a.dry_run:
        STATE.write_text(json.dumps(state, ensure_ascii=False))


if __name__ == "__main__":
    main()
