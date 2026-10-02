"""Productpool: haalt de catalogus + bestseller-ranking van alle sterke competitors op,
herkent hetzelfde product over stores en landen heen (fotovergelijking) en slaat alles op
in .cache/pool.json voor select.py.

Gebruik:  python3 pool.py                (alle competitors met ≥25K bezoekers en match ≥3)
          python3 pool.py --extra a.com:US b.com:CA
"""
import argparse, concurrent.futures as cf, csv, datetime as dt, json, re, sys, time
from pathlib import Path

import product_picker as pp

BASE = Path(__file__).parent
CACHE = BASE / ".cache"
POOL_DIR = CACHE / "stores"
COUNTRY_CODES = {"DE", "FR", "UK", "IT", "ES", "PL", "US", "CA", "NL", "AT", "CH", "BE", "PT", "IE", "SE", "DK"}


def competitors(min_visits=25000, min_score=3):
    out = []
    for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8")):
        v = int(r["Bezoekers per maand"] or 0)
        s = int(r["Match-score"] or 0)
        if v < min_visits or s < min_score:
            continue
        # Markt = land met het meeste verkeer volgens SimilarWeb, anders het land van de research-ronde.
        m = re.match(r"([A-Z]{2})\s", r["Top landen"] or "")
        market = m.group(1) if m and m.group(1) in COUNTRY_CODES else r["Land"]
        out.append(dict(domain=r["Domein"], market=market, visits=v, name=r["Store"], score=s))
    return out


def currency(domain):
    try:
        h = pp.get(f"https://{domain}/")
        m = re.search(r'Shopify\.currency\s*=\s*\{"active":"([A-Z]{3})', h)
        return m.group(1) if m else None
    except Exception:
        return None


def fetch_store(c, max_age_h=20):
    POOL_DIR.mkdir(parents=True, exist_ok=True)
    f = POOL_DIR / f'{c["domain"]}.json'
    if f.exists() and time.time() - f.stat().st_mtime < max_age_h * 3600:
        return json.loads(f.read_text())
    try:
        prods = pp.fetch_products(c["domain"])
        rank = pp.fetch_bestseller_rank(c["domain"], len(prods))
        tiers = pp.sales_tiers(prods, rank)
        cur = currency(c["domain"]) or "EUR"
    except Exception as e:
        print(f'  ! {c["domain"]}: {e}', file=sys.stderr)
        return None
    slim = []
    for p in prods:
        if not p.get("variants"):
            continue
        slim.append(dict(handle=p["handle"], title=p["title"], type=p.get("product_type") or "", tags=p.get("tags") or [],
                         created=p["created_at"], published=p.get("published_at") or p["created_at"],
                         price=float(p["variants"][0]["price"]), compare=float(p["variants"][0].get("compare_at_price") or 0),
                         avail=sum(1 for v in p["variants"] if v.get("available")), nvar=len(p["variants"]),
                         img=pp.img_url(p), rank=rank.get(p["handle"]), tier=tiers.get(p["handle"])))
    data = dict(store=c, currency=cur, fetched=dt.datetime.now().isoformat(timespec="minutes"), n_ranked=len(rank), products=slim)
    f.write_text(json.dumps(data, ensure_ascii=False))
    return data


def cluster(recs, max_dist=5):
    """Groepeert hetzelfde product over stores. Streng, zonder kettingvorming:
    een product hoort alleen bij een groep als zijn foto ≤ max_dist afwijkt van de EERSTE foto
    van die groep, de categorie gelijk is en de prijs (EUR) binnen factor 1,8 ligt.
    Kandidaten via multi-index: 64 bit in 8 blokken; ≤ 7 verschillen ⇒ minstens één blok gelijk."""
    import imagehash
    items = [r for r in recs if r.get("phash")]
    items.sort(key=lambda r: (-(r["pct"] or 0)))           # beste verkoper wordt 'seed'
    hv = [imagehash.hex_to_hash(r["phash"]) for r in items]
    buckets = {}
    for i, r in enumerate(items):
        for b in range(8):
            buckets.setdefault((b, r["phash"][2 * b:2 * b + 2]), []).append(i)
    seed_of = [None] * len(items)
    for i, r in enumerate(items):
        if seed_of[i] is not None:
            continue
        seed_of[i] = i
        cand = set()
        for b in range(8):
            lst = buckets[(b, r["phash"][2 * b:2 * b + 2])]
            if len(lst) <= 300:                              # generieke foto's overslaan
                cand.update(lst)
        stores_in = {r["store"]}
        for j in sorted(cand):
            if j == i or seed_of[j] is not None:
                continue
            q = items[j]
            if (q["cat"] == r["cat"] and hv[i] - hv[j] <= max_dist and q["store"] not in stores_in
                    and 1 / 1.8 <= q["price_eur"] / max(r["price_eur"], 1) <= 1.8):
                seed_of[j] = i
                stores_in.add(q["store"])
    key = lambda r: f'{r["store"]}/{r["handle"]}'
    size = {}
    for sd in seed_of:
        size[sd] = size.get(sd, 0) + 1
    return {key(r): key(items[seed_of[i]]) for i, r in enumerate(items) if size[seed_of[i]] >= 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra", nargs="*", default=[], help="domein:MARKT, bijv. harperwells-boston.com:US")
    ap.add_argument("--markten", nargs="*", default=["ES", "IT", "DE", "PL", "UK", "US"], help="markten van jouw stores")
    a = ap.parse_args()
    comps = competitors()
    known = {c["domain"] for c in comps}
    for e in a.extra:
        d, m = e.split(":")
        if d not in known:
            comps.append(dict(domain=d, market=m, visits=0, name=d, score=4))
    print(f"{len(comps)} competitors ophalen ...", file=sys.stderr)
    with cf.ThreadPoolExecutor(6) as ex:
        stores = [s for s in ex.map(fetch_store, comps) if s]

    cfg = json.loads((BASE / "config/seasons.json").read_text())
    pats = pp.compile_keywords(cfg)
    fx = json.loads((BASE / "config/stores.json").read_text())["fx_naar_eur"]
    now = dt.datetime.now(dt.timezone.utc)
    recs = []
    for s in stores:
        n = max(s["n_ranked"], 1)
        rate = fx.get(s["currency"], 1.0)
        for p in s["products"]:
            live = max(dt.datetime.fromisoformat(p["published"]), dt.datetime.fromisoformat(p["created"]))
            pct = 1 - (p["rank"] - 1) / n if p["rank"] else 0.0
            cat = pp.categorize({"title": p["title"], "product_type": p["type"], "tags": p["tags"]}, pats)
            sw = {}
            for m in a.markten:
                season = cfg["season_by_month"].get(m, cfg["season_by_month"]["DE"])[str(now.month)]
                sw[m] = pp.season_weight(p, cat, cfg, m, season)[0]
            recs.append(dict(store=s["store"]["domain"], market=s["store"]["market"], visits=s["store"]["visits"],
                             handle=p["handle"], title=p["title"], cat=cat, price_eur=round(p["price"] * rate, 2),
                             price=p["price"], cur=s["currency"], compare=p["compare"], avail=p["avail"], nvar=p["nvar"],
                             age=(now - live).days, live=live.date().isoformat(), rank=p["rank"], pct=round(pct, 3),
                             tier0=(p["tier"] == 0), season=sw, img=p["img"], tags=p["tags"]))
    # Alleen kandidaten hashen: in seizoen ergens én (nieuw of verkopend).
    cand = [r for r in recs if r["img"] and max(r["season"].values()) >= 0.5 and (r["age"] <= 75 or r["pct"] >= 0.5)]
    print(f"{len(recs)} producten, {len(cand)} kandidaten; foto's vergelijken ...", file=sys.stderr)
    hashes = pp.hash_images([r["img"] for r in cand])
    key = lambda r: f'{r["store"]}/{r["handle"]}'
    for r in recs:
        r["phash"] = hashes.get(r["img"]) if r["img"] else None
    cl = cluster([r for r in recs if r.get("phash")])
    for r in recs:
        r["cluster"] = cl.get(key(r))
    out = dict(built=now.isoformat(timespec="minutes"), stores=[dict(**s["store"], currency=s["currency"], n=len(s["products"])) for s in stores],
               products=recs)
    (CACHE / "pool.json").write_text(json.dumps(out, ensure_ascii=False))
    multi = {}
    for r in recs:
        if r["cluster"]:
            multi.setdefault(r["cluster"], set()).add(r["store"])
    print(f"Klaar: {len(stores)} stores, {len(recs)} producten, "
          f"{sum(1 for v in multi.values() if len(v) >= 2)} producten bij ≥2 competitors.", file=sys.stderr)


if __name__ == "__main__":
    main()
