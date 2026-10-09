"""Selecteert per eigen store de beste producten om te listen, op basis van de productpool
(pool.py) over alle competitors en landen heen.

Strategieën (in volgorde van voorkeur):
  A  Bewezen elders, vrij in jouw markt  - bestseller bij competitor(s) in een ánder land, in jouw markt
                                           nog door geen enkele competitor verkocht. Geen prijsdruk.
  B  Breed bewezen                        - bij ≥3 competitors te koop en ergens een bestseller.
  C  Nieuw & opkomend                     - ≤21 dagen live bij een sterke competitor en al verkopend.
  D  Bewezen in jouw markt                - bestseller bij een competitor in jouw land: alleen met
                                           scherpere prijs; ≥3 competitors in jouw land = verzadigd (overslaan).
  E  Nieuw bij topcompetitor              - net toegevoegd (≤14 dagen) door een store met ≥150K bezoekers.

Gebruik:  python3 select_products.py            (alle stores uit config/stores.json)
          python3 select_products.py --store Stellamea --aantal 300
"""
import argparse, concurrent.futures as cf, datetime as dt, io, json, math, re, statistics as st, sys
from pathlib import Path

import product_picker as pp

BASE = Path(__file__).parent
CACHE = BASE / ".cache"
OUT = BASE / "listings"
COLD = {"DE", "PL", "UK", "US", "CA", "NL", "AT", "CH"}
SKIP_TITLE = re.compile(r"(geschenk|gift ?card|carte cadeau|tarjeta regalo|versandschutz|shipping protection|protection de l|"
                        r"expédition|insurance|versicherung|bundle|mystery|\bbox\b|sample)", re.I)
W_RE = re.compile(r"(damen|women|woman|ladies|donna|mujer|femme|damsk|dames|\bwomens?\b)", re.I)
M_RE = re.compile(r"(herren|\bmen\b|\bmens\b|\bmen's|uomo|hombre|homme|męsk|mesk|heren)", re.I)
MARKET_NAME = {"DE": "Germany", "FR": "France", "UK": "United Kingdom", "IT": "Italy", "ES": "Spain", "PL": "Poland",
               "US": "United States", "CA": "Canada", "NL": "Netherlands", "AT": "Austria", "CH": "Switzerland"}
CAT_EN = {"Winterjas": "Winter coat", "Tussenjas": "Transition jacket", "Trui / hoodie": "Sweater / hoodie",
          "Vest / cardigan": "Cardigan", "Blazer": "Blazer", "Laarzen": "Boots", "Broek": "Trousers", "Jurk": "Dress",
          "Blouse / shirt": "Blouse / shirt", "Set": "Set", "Schoenen": "Shoes", "T-shirt / top": "T-shirt / top",
          "Shorts": "Shorts", "Sandalen": "Sandals", "Badmode": "Swimwear", "Overig": "Other"}


# Alleen deze competitors mogen bronlink zijn: geverifieerd ≥75K bezoekers/mnd (SimilarWeb-hoofdcijfer),
# match-score ≥4 (zelfde dropship-model, geen eigen label) en geen onbevestigde/geschatte cijfers.
MIN_SOURCE_VISITS = 75000
MIN_SOURCE_PAID = 0.58   # ≥60% paid search; Leon Boutique (59%) op verzoek binnen, Karlson (30%) eruit
ELIGIBLE, VISITS, TREND = set(), {}, {}


def load_eligible():
    import csv
    for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8")):
        v = int(r["Bezoekers per maand"] or 0)
        n = r["Notities"].lower()
        VISITS[r["Domein"]] = v
        TREND[r["Domein"]] = float(r["Trend vorige maand"]) if r["Trend vorige maand"] not in ("", None) else 0.0
        paid = float(r["Paid search"]) if r["Paid search"] not in ("", None) else 0.0
        if (v >= MIN_SOURCE_VISITS and paid >= MIN_SOURCE_PAID and int(r["Match-score"] or 0) >= 4 and "referentie" not in n
                and "onbevestigd" not in n and "schatting" not in n):
            ELIGIBLE.add(r["Domein"])


def gender(title, typ=""):
    t = f"{title} {typ}"
    w, m = bool(W_RE.search(t)), bool(M_RE.search(t))
    return "W" if w and not m else "M" if m and not w else "?"


def round_price(eur, cur, fx):
    v = eur / fx.get(cur, 1.0)
    if cur == "PLN":
        return max(round(v / 10) * 10 - 0.05, 9.95)
    return max(math.floor(v) + 0.95 if v - math.floor(v) >= 0.45 else math.floor(v) - 0.05, 9.95)


def own_catalog(domain):
    prods = pp.fetch_products(domain)
    imgs = [pp.img_url(p) for p in prods if p.get("images")]
    gal = [im["src"] + ("&" if "?" in im["src"] else "?") + "width=240" for p in prods for im in (p.get("images") or [])[:6]]
    hashes = pp.hash_images(imgs)
    all_hashes = [h for h in pp.hash_images(gal).values() if h]
    g = [gender(p["title"], p.get("product_type") or "") for p in prods]
    share_w = g.count("W") / max(g.count("W") + g.count("M"), 1)
    prices = sorted(float(p["variants"][0]["price"]) for p in prods if p.get("variants"))
    return dict(n=len(prods), hashes=[h for h in hashes.values() if h], all_hashes=all_hashes, share_w=share_w,
                median=prices[len(prices) // 2] if prices else None,
                handles={p["handle"] for p in prods}, titles=[p["title"] for p in prods])


def build_groups(pool):
    groups = {}
    for r in pool["products"]:
        if SKIP_TITLE.search(r["title"]) or r["cat"] == "Overig" or r["price_eur"] < 12:
            continue
        k = r["cluster"] or f'{r["store"]}/{r["handle"]}'
        groups.setdefault(k, []).append(r)
    return groups


def evaluate(members, markets, store_visits_rank):
    # Verzadiging en bevestiging: alle competitors. Bewijs en bron: alleen grote (ELIGIBLE) competitors.
    in_m = [m for m in members if m["market"] in markets]
    out_m = [m for m in members if m["market"] not in markets]
    stores_all = {m["store"] for m in members}
    stores_in = {m["store"] for m in in_m}
    big = [m for m in members if m["store"] in ELIGIBLE]
    if not big:
        return None
    best = max(big, key=lambda m: (m["pct"], -m["age"]))
    best_in = max((m["pct"] for m in big if m["market"] in markets), default=0)
    best_out = max((m["pct"] for m in big if m["market"] not in markets), default=0)
    newest = min(m["age"] for m in big)
    season = st.mean(max((mm["season"].get(k, 0) for mm in members), default=0) for k in markets)
    all_tier0 = all(m["tier0"] for m in big)
    big_new = [m for m in big if m["age"] <= 14 and m["visits"] >= 150000]
    selling_new = [m for m in big if m["age"] <= 21 and m["pct"] >= 0.6 and not m["tier0"]]

    strat = None
    if len(stores_in) >= 3:
        strat = "X"  # verzadigd in jouw markt
    elif not stores_in and best_out >= 0.75:
        strat = "A"
    elif len(stores_all) >= 3 and best["pct"] >= 0.6:
        strat = "B"
    elif selling_new and len(stores_in) <= 1:
        strat = "C"
    elif stores_in and best_in >= 0.8:
        strat = "D"
    elif big_new and len(stores_in) <= 1:
        strat = "E"
    if strat in (None, "X"):
        return None

    newness = max(0.0, 1 - newest / 45)
    reach = math.log10(max(best["visits"], 10000)) / math.log10(1_500_000)
    bonus = {"A": 1.0, "B": 0.9, "C": 0.8, "D": 0.4, "E": 0.6}[strat]
    score = season * (35 * best["pct"] + 15 * min(len(stores_all) - 1, 3) / 3 + 20 * newness + 15 * bonus + 15 * reach)
    # Trend van de bron: dalers tellen gewoon mee (blijven grote stores), alleen een kleine correctie (±5%).
    score *= 1 + 0.075 * max(-0.7, min(TREND.get(best["store"], 0.0), 0.7))
    if len(stores_in) == 2:
        score -= 15
    if strat == "D":
        score -= 8   # we gaan niet onder de prijs zitten, dus bewezen-in-eigen-markt weegt minder
    if all_tier0 and newest > 10:
        score -= 20
    return dict(strat=strat, score=round(score, 1), best=best, members=members, big=big, in_m=in_m, out_m=out_m,
                stores_all=stores_all, stores_in=stores_in, season=round(season, 2), newest=newest, newness=newness)


def price_bands(pool, markets):
    """Sweet spot per categorie: P25/P50/P75 van de bestsellers (top 25%) in de markt(en);
    te weinig data in de markt → alle markten."""
    def q(v, x):
        v = sorted(v); return v[min(int(x * len(v)), len(v) - 1)]
    allv, mk = {}, {}
    for r in pool["products"]:
        if r["pct"] >= 0.75 and r["price_eur"] >= 12:
            allv.setdefault(r["cat"], []).append(r["price_eur"])
            if r["market"] in markets:
                mk.setdefault(r["cat"], []).append(r["price_eur"])
    out = {}
    for c, v in allv.items():
        src = mk.get(c) if len(mk.get(c, [])) >= 25 else v
        out[c] = (q(src, 0.25), q(src, 0.5), q(src, 0.75))
    return out


def fetch_media(members):
    """Foto-informatie van de bronproducten (aantal, afmeting 1e foto), met cache."""
    f = CACHE / "media.json"
    cache = json.loads(f.read_text()) if f.exists() else {}
    todo = [m for m in members if f'{m["store"]}/{m["handle"]}' not in cache]

    def one(m):
        k = f'{m["store"]}/{m["handle"]}'
        try:
            d = json.loads(pp.get(f'https://{m["store"]}/products/{m["handle"]}.js', timeout=20))
            imgs = [x for x in d.get("media", []) if x.get("media_type") == "image"] or \
                   [{"src": u, "width": None, "height": None} for u in d.get("images", [])]
            return k, [dict(src=("https:" + x["src"]) if str(x.get("src", "")).startswith("//") else x.get("src"),
                            w=x.get("width"), h=x.get("height")) for x in imgs][:12]
        except Exception:
            return k, None
    with cf.ThreadPoolExecutor(16) as ex:
        for k, v in ex.map(one, todo):
            cache[k] = v
    f.write_text(json.dumps(cache))
    return cache


def image_score(media):
    """0-100: aantal foto's (≥6 ideaal), resolutie 1e foto (≥1200 px), staande verhouding (3:4 – 4:5)."""
    if not media:
        return 0, "no photo info"
    n = len(media)
    w, h = media[0].get("w") or 0, media[0].get("h") or 0
    s_n = min(n, 6) / 6 * 35
    s_res = (min(min(w, h), 1200) / 1200 * 40) if w and h else 15
    r = (h / w) if w else 1
    s_ar = 25 if 1.15 <= r <= 1.55 else 18 if 0.95 <= r < 1.15 else 8
    txt = f"{n} photos, 1st {w}×{h}" if w else f"{n} photos"
    return round(s_n + s_res + s_ar), txt


def choose_source(ev, store_cur, markets, media):
    """Bronlink: (1) liefst NIET bij een concurrent in jouw eigen markt – zelfde foto en prijs is
    directe concurrentie; (2) waar het product goed verkoopt (≤0,15 onder de beste ranking);
    (3) de beste foto's; (4) dezelfde valuta en de hoogste prijs."""
    top = max(m["pct"] for m in ev["big"])
    near = [m for m in ev["big"] if m["pct"] >= top - 0.15] or ev["big"]
    for m in near:
        m["img_score"], m["img_txt"] = image_score(media.get(f'{m["store"]}/{m["handle"]}'))
    return max(near, key=lambda m: (m["market"] not in markets, round(m["img_score"] / 15),
                                    m["cur"] == store_cur, m["price_eur"], m["pct"]))


def photo_advice(ev, src, markets, media):
    """Does a competitor in your market use the same main photo? Then use another photo first."""
    rivals = [m for m in ev["in_m"] if m is not src]
    if src["market"] in markets:
        rivals.append(src)
    if not rivals:
        return "Main photo free to use (no competitor in your market)"
    gal = media.get(f'{src["store"]}/{src["handle"]}') or []
    if len(gal) >= 2:
        return f"Same main photo as {len({r['store'] for r in rivals})} competitor(s) in your market → use photo 2 (or a model photo) as main image"
    return "Same main photo as a competitor in your market → use a different (supplier) photo as main image"


def price_advice(ev, store_cur, fx, bands):
    src = ev["best"]
    if src["market"] in ev.get("markets", ()):
        # Bron adverteert in jouw land: iets onder zijn prijs, maar nooit meer dan €5 / 5% (marge beschermen).
        base = src["price"] if src["cur"] == store_cur else src["price_eur"] / fx.get(store_cur, 1.0)
        drop = min(5.0 / fx.get(store_cur, 1.0) if store_cur != "EUR" else 5.0, 0.05 * base)
        adv = round_price((base - drop) * fx.get(store_cur, 1.0), store_cur, fx)
        if adv < base - drop - 0.01:          # afronding mag nooit verder omlaag dan de grens
            adv = round_price((base - drop + 1) * fx.get(store_cur, 1.0), store_cur, fx)
        band = ""
        p25, p50, p75 = bands.get(src["cat"], (None, None, None))
        if p25:
            band = f"{round_price(p25, store_cur, fx):.0f}–{round_price(p75, store_cur, fx):.0f}"
        return adv, band, f"source advertises in your market: slightly below its price ({base:.2f}), max €5 / 5% lower", None
    p25, p50, p75 = bands.get(src["cat"], (None, None, None))
    if src["cur"] == store_cur:
        advies = src["price"]
        why = "take over the source link price"
    else:
        advies = round_price(src["price_eur"], store_cur, fx)
        why = f"source link price ({src['price']:.2f} {src['cur']}) converted"
    hoger = None
    if p50 and src["price_eur"] < p25:
        hoger = round_price(p50, store_cur, fx)
        why += f"; below the category sweet spot, can go higher: {hoger:.2f}"
    ins = [m for m in ev["in_m"] if m["pct"] >= 0.75]
    if ins:
        why += f"; note: already a bestseller at {len({m['store'] for m in ins})} competitor(s) in your market"
    band = (f"{round_price(p25, store_cur, fx):.0f}–{round_price(p75, store_cur, fx):.0f}" if p25 else "")
    return advies, band, why, hoger


def explain(ev, markets, names):
    b = ev["best"]
    nm = lambda d: names.get(d, d)
    parts = []
    top = f"top {max(1, round((1 - b['pct']) * 100))}%"
    parts.append(f"{top} bestseller at {nm(b['store'])} ({b['market']}, {b['visits']/1000:.0f}K visits/mo)" if b["visits"]
                 else f"{top} bestseller at {nm(b['store'])} ({b['market']})")
    others = sorted({(nm(m["store"]), m["market"], m["store"] in ELIGIBLE) for m in ev["members"] if m["store"] != b["store"]},
                    key=lambda t: (not t[2], t[0]))
    if others:
        parts.append("also at " + ", ".join(f"{s} ({mk}{'' if big else ', small'})" for s, mk, big in others[:4])
                     + (f" +{len(others) - 4}" if len(others) > 4 else ""))
    if not ev["stores_in"]:
        parts.append(f"no competitor sells it in {'/'.join(markets)} yet → open space")
    else:
        parts.append(f"{len(ev['stores_in'])} competitor(s) in {'/'.join(markets)}")
    if ev["newest"] <= 21:
        parts.append(f"added {ev['newest']} days ago")
    parts.append(f"season fit {ev['season']:.1f}")
    return " · ".join(parts)


XMAS = re.compile(r"(weihnacht|christmas|xmas|navidad|natale|noël|noel|święt|swiat|ugly sweater|rentier|reindeer|santa)", re.I)


def listweek(ev, markets):
    """Week 1-2: herfstlagen; week 3: zwaardere winterartikelen in koude markten; week 4: kerst."""
    b = ev["best"]
    if XMAS.search(b["title"]):
        return 4
    if not (set(markets) & COLD):
        return 1 if b["cat"] in ("Blazer", "Vest / cardigan", "Tussenjas", "Trui / hoodie", "Blouse / shirt") else 2
    if b["cat"] in ("Winterjas", "Laarzen"):
        return 3
    return 1 if b["cat"] in ("Tussenjas", "Blazer", "Vest / cardigan", "Blouse / shirt", "Jurk", "Set") else 2


def final_checks(picked, own, existing, media, n_target):
    """Strengere dubbelcheck + bron-check (lessen uit de eerste ronde):
    - eerste 3 foto's van de bron vs ALLE foto's van je eigen producten (listers kiezen soms een andere hoofdfoto);
    - eerste 3 foto's vs alle regels die al in de Launch File staan en vs elkaar (kleurvarianten = zelfde product);
    - bronlink moet nog actief zijn en ≥50% van de maten leverbaar."""
    import imagehash
    own_h = [imagehash.hex_to_hash(h) for h in own["all_hashes"]]
    gal = lambda m: [x["src"] + ("&" if "?" in (x["src"] or "") else "?") + "width=240" for x in (m or [])[:3] if x.get("src")]
    ex_imgs = []
    for x in existing:
        k = "/".join(x["url"].split("/")[2:5:2])
        ex_imgs += gal(media.get(k)) or ([x["img"]] if x.get("img") else [])
    cand_imgs = [u for e in picked for u in gal(media.get(f'{e["best"]["store"]}/{e["best"]["handle"]}'))]
    hs = pp.hash_images(ex_imgs + cand_imgs)
    seen = [imagehash.hex_to_hash(h) for u in ex_imgs if (h := hs.get(u))]

    def avail(e):
        b = e["best"]
        try:
            d = json.loads(pp.get(f'https://{b["store"]}/products/{b["handle"]}.js', timeout=20))
            v = d.get("variants") or []
            return bool(v) and sum(1 for x in v if x.get("available")) >= max(1, 0.5 * len(v))
        except Exception:
            return False
    with cf.ThreadPoolExecutor(12) as ex:
        ok = list(ex.map(avail, picked))
    out, drop = [], {"al in store": 0, "dubbel in lijst": 0, "bron niet leverbaar": 0}
    for e, a in zip(picked, ok):
        if not a:
            drop["bron niet leverbaar"] += 1; continue
        hh = [imagehash.hex_to_hash(h) for u in gal(media.get(f'{e["best"]["store"]}/{e["best"]["handle"]}')) if (h := hs.get(u))]
        if any(h - o <= 8 for h in hh for o in own_h):
            drop["al in store"] += 1; continue
        if any(h - o <= 6 for h in hh for o in seen):
            drop["dubbel in lijst"] += 1; continue
        seen += hh
        out.append(e)
        if len(out) >= n_target:
            break
    print(f"   final checks: {drop} → {len(out)}", file=sys.stderr)
    return out


def select_for_store(store, pool, groups, fx, names, taken, n_target, existing=()):
    markets = store["markten"]
    print(f"\n== {store['naam']} ({'/'.join(markets)}) ...", file=sys.stderr)
    own = own_catalog(store["domein"])
    import imagehash
    own_h = [imagehash.hex_to_hash(h) for h in own["hashes"]]
    cands = []
    for k, mem in groups.items():
        ev = evaluate(mem, markets, None)
        if not ev or ev["season"] < 0.6:
            continue
        ph = ev["best"].get("phash")
        if ph:
            h = imagehash.hex_to_hash(ph)
            if any(h - o <= 8 for o in own_h):
                continue  # heb je al
        g = gender(ev["best"]["title"])
        # Laat de mix aansluiten bij je store: dames/heren-verhouding als lichte weging.
        if g == "W":
            ev["score"] *= 0.75 + 0.5 * own["share_w"]
        elif g == "M":
            ev["score"] *= 0.75 + 0.5 * (1 - own["share_w"])
        ev["gender"], ev["key"] = g, k
        ev["score"] = round(ev["score"], 1)
        cands.append(ev)
    cands.sort(key=lambda e: -e["score"])
    # Categoriespreiding: max ~30% per categorie, zodat je niet 300 truien krijgt.
    cap = max(int(n_target * 0.3), 20)
    per_cat, picked = {}, []
    for e in cands:
        if any(e["key"] in taken.get(m, set()) for m in markets):
            continue  # al toegewezen aan een andere eigen store in dezelfde markt
        c = e["best"]["cat"]
        if per_cat.get(c, 0) >= cap:
            continue
        per_cat[c] = per_cat.get(c, 0) + 1
        picked.append(e)
        if len(picked) >= int(n_target * (2.4 if len(markets) > 1 else 1.8)) + 15:
            break
    bands = price_bands(pool, markets)
    media = fetch_media([m for e in picked for m in e["members"]])
    for e in picked:
        e["best"] = choose_source(e, store["valuta"], markets, media)
        # Foto's wegen mee: 1e foto bepaalt de klikratio. ±8 punten rond een gemiddelde score van 70.
        e["score"] = round(e["score"] + (e["best"]["img_score"] - 70) / 3.75, 1)
    picked = [e for e in picked if e["best"]["img_score"] >= 45] or picked
    # Bron in eigen markt alleen bij sterke trend + volledige match (top 15% bestseller, strategie B of C, goede foto's).
    picked = [e for e in picked if e["best"]["market"] not in markets
              or (e["strat"] in ("B", "C") and e["best"]["pct"] >= 0.85 and e["best"]["img_score"] >= 70)]
    picked.sort(key=lambda e: -e["score"])
    picked = final_checks(picked, own, existing, media, n_target)
    for m in markets:
        taken.setdefault(m, set()).update(e["key"] for e in picked)
    for e in picked:
        e["markets"] = markets
        e["foto_advies"] = photo_advice(e, e["best"], markets, media)
        e["bron_in_markt"] = e["best"]["market"] in markets
        e["advies"], e["band"], e["prijs_why"], e["hoger"] = price_advice(e, store["valuta"], fx, bands)
        e["uitleg"] = explain(e, markets, names)
        e["week"] = listweek(e, markets)
    picked.sort(key=lambda e: (e["week"], -e["score"]))
    print(f"   {len(cands)} kandidaten → {len(picked)} gekozen; eigen catalogus {own['n']} producten, "
          f"{own['share_w']:.0%} dames", file=sys.stderr)
    return picked, own


STRAT_TXT = {
    "A": ("A · Proven elsewhere, open in your market", "Bestseller at big competitor(s) in another country, while no competitor sells it in your market yet. Best chance: proven product without price competition."),
    "B": ("B · Broadly proven", "Sold by 3+ competitors and a bestseller at a big one. Several strong stores bet on it: low risk."),
    "C": ("C · New & rising", "Live ≤21 days at a big competitor and already in the top 40% of its ranking. Get in early before it is everywhere."),
    "D": ("D · Proven in your market", "Bestseller at one competitor in your country (3+ competitors there = skipped). Demand is proven; you compete on ads and photos, not on price."),
    "E": ("E · New at a top competitor", "Just added (≤14 days) by a store with 150K+ visits. Not yet proven, but these stores test deliberately."),
}


LISTERS = ["Dhafnie", "Fatima", "Davy"]
STATUSES = ["Not listed", "Draft", "Live", "Issues", "Duplicate"]
FILE_NAME = "Launch File Davy Koopman.xlsx"
STATE = OUT / "launch_state.json"


def to_row(e, store, names):
    """Plat record per pick (wordt bewaard in launch_state.json zodat statussen bij een update blijven)."""
    b = e["best"]
    return dict(key=e["key"], url=f'https://{b["store"]}/products/{b["handle"]}', title=b["title"],
                cat=CAT_EN.get(b["cat"], b["cat"]), gender=e["gender"], week=e["week"], strat=e["strat"],
                score=e["score"], why=e["uitleg"], price=e["advies"], band=e["band"], price_note=e["prijs_why"],
                source=f"{names.get(b['store'], b['store'])} ({VISITS.get(b['store'], 0)/1000:.0f}K)",
                market=b["market"], own_market=e["bron_in_markt"], img_score=b.get("img_score"), img_txt=b.get("img_txt"),
                photo_note=e["foto_advies"], alts=[f'https://{m["store"]}/products/{m["handle"]}' for m in e["big"] if m is not b][:3],
                img=b["img"], added=dt.date.today().isoformat(), lister="", status="Not listed", comment="", name="")


def read_statuses(path):
    """Leest Lister/Status/Comment per (Links-tab, link) uit een teruggestuurde Launch File."""
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    out = {}
    for ws in wb.worksheets:
        if not ws.title.endswith("– Links"):
            continue
        hdr = [c.value for c in ws[3]]
        try:
            ci = {k: hdr.index(k) for k in ("Link", "Lister", "Status", "Comment")}
        except ValueError:
            continue
        for row in ws.iter_rows(min_row=4, values_only=True):
            if row[ci["Link"]]:
                out[(ws.title, row[ci["Link"]])] = dict(lister=row[ci["Lister"]] or "", status=row[ci["Status"]] or "Not listed",
                                            comment=row[ci["Comment"]] or "")
    return out


def write_workbook(results, pool, names, path):
    """One file: 'Strategy & explanation' + per store a 'to list' tab and a '– Links' tab with lister/status."""
    from collections import Counter
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as XLImage
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from PIL import Image

    F, navy = "Arial", "1F2A44"
    f = lambda **k: Font(name=F, size=k.pop("size", 10), **k)
    thin = Border(bottom=Side(style="thin", color="D9DDE3"))
    hdr_fill = PatternFill("solid", fgColor=navy)
    sfill = {"A": "C6EFCE", "B": "DDEBF7", "C": "FCE4D6", "D": "FFF2CC", "E": "EDE7F6"}
    st_col = {"Not listed": ("F2F2F2", "595959"), "Draft": ("FFF2CC", "7F6000"), "Live": ("C6EFCE", "006100"),
              "Issues": ("FFC7CE", "9C0006"), "Duplicate": ("D9D9D9", "404040")}
    wb = Workbook()

    def thumb(u):
        try:
            im = Image.open(io.BytesIO(pp.get(u, binary=True, timeout=20))).convert("RGB")
            im.thumbnail((84, 84)); b = io.BytesIO(); im.save(b, "JPEG", quality=78); b.seek(0)
            return b
        except Exception:
            return None

    # ---------- Strategy & explanation ----------
    sg = wb.active
    sg.title = "Strategy & explanation"
    sg.column_dimensions["A"].width = 30
    sg.column_dimensions["B"].width = 120
    sg["A1"], sg["A1"].font = "Launch File – Davy Koopman", f(size=15, bold=True, color=navy)
    sg["A2"] = (f"Updated {dt.date.today():%d-%m-%Y} · per store a product tab and a '– Links' tab · list ±15-25 per store per day · "
                "listers fill in Lister / Status / Comment on the Links tab")
    sg["A2"].font = f(italic=True, color="666666")
    big = sorted(ELIGIBLE, key=lambda d: -VISITS.get(d, 0))
    rules = [
        ("How to use (listers)", "1) Open the '– Links' tab of your store. 2) Pick your name under Lister. 3) List the product from the link "
         "at the advised price. 4) Set Status: Live (published), Draft (prepared, not yet live), Duplicate (already in store) or Issues + a Comment. Work from top to bottom (list order). Always reach your daily target: skip duplicates and list the next one."),
        ("Sources (import links)", f"Only {len(big)} competitors with a verified SimilarWeb figure of ≥75K visits/month, the same dropshipping "
         "model and no own label. Smaller or unverified stores only count as confirmation ('also at …, small') and for saturation, never as source."),
        ("Source choice per product", "Preferably a competitor in a different country than your market (same photo + price at a domestic "
         "competitor = direct competition). Then: selling well, best photos, same currency, highest price. "
         "'⚠ own market' = only a domestic big source exists: follow the photo advice."),
        ("Price", "Advised price = price of the source link (take it over; other currency → converted, ending in .95). Never underprice. "
         "Below the category sweet spot (P25–P75 of bestsellers) → 'can go higher'."),
        ("Photos", "Photo score 0-100 (≥6 photos, 1st photo ≥1200 px, portrait 3:4/4:5). Counts in the order; weak photos are removed."),
        ("Season & order", "Week 1-2 autumn layers, week 3 winter coats/boots (cold markets), week 4 Christmas."),
        ("Duplicate check", "Products already in your store are removed (photo match). Stores sharing a market (UK) never get the same product."),
        ("", "")]
    for s_ in "ABCDE":
        rules.append(STRAT_TXT[s_])
    rules += [("", ""), ("Note", "Bestseller rank = position in the store's own 'best selling' sort, not a sales count. "
               "Preferably use supplier photos or your own texts rather than copying everything 1:1 from the competitor.")]
    r0 = 4
    for i, (k, v) in enumerate(rules):
        sg.cell(row=r0 + i, column=1, value=k).font = f(bold=True)
        c = sg.cell(row=r0 + i, column=2, value=v); c.font = f(); c.alignment = Alignment(wrap_text=True, vertical="top")
    r = r0 + len(rules) + 1
    sg.cell(row=r, column=1, value="Per store").font = f(size=12, bold=True, color=navy)
    r += 1
    for store, rows, own in results:
        cnt, cats, wk = Counter(x["strat"] for x in rows), Counter(x["cat"] for x in rows), Counter(x["week"] for x in rows)
        stc = Counter(x["status"] or "Not listed" for x in rows)
        src = Counter(x["source"] for x in rows)
        txt = (f"Market: {', '.join(MARKET_NAME.get(m, m) for m in store['markten'])} · {store['valuta']} · catalogue {own['n']} products "
               f"({own['share_w']:.0%} women) · {len(rows)} products · status: " + ", ".join(f"{k} {stc.get(k, 0)}" for k in STATUSES) + "\n"
               "Strategy: " + ", ".join(f"{k} {cnt[k]}" for k in "ABCDE" if cnt.get(k)) + "\n"
               "Categories: " + ", ".join(f"{k} {v}" for k, v in cats.most_common()) + "\n"
               "List weeks: " + ", ".join(f"week {k}: {v}" for k, v in sorted(wk.items())) + "\n"
               "Sources: " + ", ".join(f"{k} {n}×" for k, n in src.most_common()))
        sg.cell(row=r, column=1, value=store["naam"]).font = f(bold=True)
        c = sg.cell(row=r, column=2, value=txt); c.font = f(); c.alignment = Alignment(wrap_text=True, vertical="top")
        sg.row_dimensions[r].height = 92
        r += 1
    r += 1
    sg.cell(row=r, column=1, value="Allowed sources").font = f(size=12, bold=True, color=navy)
    r += 1
    mk = {s["domain"]: s["market"] for s in pool["stores"]}
    for d in big:
        sg.cell(row=r, column=1, value=names.get(d, d)).font = f()
        sg.cell(row=r, column=2, value=f"{mk.get(d, '')} · {VISITS.get(d, 0):,} visits/month").font = f()
        r += 1

    # ---------- per store ----------
    heads = ["#", "Photo", "List week", "Strategy", "Score", "Product (source title)", "Category", "W/M", "Why this product",
             "Advised price", "Category sweet spot", "Price note", "Cost price – fill in", "Margin %",
             "Source (import link)", "Source", "Source country", "Photo score", "Photos", "Photo advice", "Other (big) sources",
             "Status (from Links)", "Added on"]
    widths = [5, 13, 9, 26, 7, 42, 15, 5, 70, 11, 12, 34, 12, 9, 12, 20, 11, 9, 18, 38, 40, 13, 11]
    for store, rows, own in results:
        cur = store["valuta"]
        lt = f"{store['naam'][:22]} – Links"
        ws = wb.create_sheet(store["naam"][:31])
        ws.sheet_properties.tabColor = "F4B183"
        ws["A1"] = f"{store['naam']} – {len(rows)} products to list ({'/'.join(MARKET_NAME.get(m, m) for m in store['markten'])}, {cur})"
        ws["A1"].font = f(size=15, bold=True, color=navy)
        ws["A2"] = "Sorted by list order · sources only big competitors (≥75K visits/month, verified) · status is set on the Links tab"
        ws["A2"].font = f(italic=True, color="666666")
        H = 4
        for i, (h, w) in enumerate(zip(heads, widths), 1):
            hv = f"{h} ({cur})" if h in ("Advised price", "Category sweet spot", "Cost price – fill in") else h
            c = ws.cell(row=H, column=i, value=hv)
            c.font, c.fill = f(bold=True, color="FFFFFF"), hdr_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[H].height = 32
        with cf.ThreadPoolExecutor(16) as ex:
            thumbs = list(ex.map(lambda x: thumb(x["img"]) if x["img"] else None, rows))
        for i, (x, tb) in enumerate(zip(rows, thumbs)):
            r = H + 1 + i
            vals = [i + 1, "", f"Week {x['week']}", STRAT_TXT[x["strat"]][0], x["score"], x["title"], x["cat"], x["gender"],
                    x["why"], x["price"], x["band"], x["price_note"], None, None, "Open", x["source"],
                    x["market"] + (" ⚠ own market" if x["own_market"] else ""), x["img_score"], x["img_txt"],
                    x["photo_note"], "\n".join(x["alts"]), f"='{lt}'!H{r}", x["added"]]
            for j, v in enumerate(vals, 1):
                c = ws.cell(row=r, column=j, value=v)
                c.font, c.border = f(), thin
                c.alignment = Alignment(vertical="center", wrap_text=j in (4, 6, 9, 12, 16, 20, 21))
            ws.row_dimensions[r].height = 66
            ws.cell(row=r, column=4).fill = PatternFill("solid", fgColor=sfill[x["strat"]])
            for col in (10, 13):
                ws.cell(row=r, column=col).number_format = "0.00"
            inp = ws.cell(row=r, column=13)
            inp.fill, inp.font = PatternFill("solid", fgColor="FFF2CC"), f(color="0000FF")
            m = ws.cell(row=r, column=14, value=f'=IF(M{r}="","",(J{r}-M{r})/J{r})')
            m.number_format = "0%"
            lk = ws.cell(row=r, column=15)
            lk.hyperlink, lk.font = x["url"], f(color="1F5FBF", underline="single")
            if x["own_market"]:
                ws.cell(row=r, column=17).fill = PatternFill("solid", fgColor="FCE4D6")
            if tb:
                im = XLImage(tb); im.anchor = f"B{r}"; ws.add_image(im)
        last = H + max(len(rows), 1)
        for name, (bg, fg) in st_col.items():
            ws.conditional_formatting.add(f"V{H+1}:V{last}", FormulaRule(formula=[f'$V{H+1}="{name}"'],
                                          fill=PatternFill("solid", fgColor=bg), font=Font(name=F, bold=True, color=fg)))
        ws.freeze_panes = "C5"
        ws.auto_filter.ref = f"A{H}:W{last}"

        # Links tab (Links rows are aligned with the product tab: product row r ↔ Links row r)
        ls = wb.create_sheet(lt)
        ls.sheet_properties.tabColor = "A9D08E"
        ls["A1"] = f"{store['naam']}: import links in list order – list 15-25 per day, then set Lister and Status"
        ls["A1"].font = f(bold=True)
        lh = ["#", "List week", "Product Name", "Link", f"Advised price ({cur})", "Source", "Lister", "Status", "Comment", "Added on"]
        for c, (h, w) in enumerate(zip(lh, (5, 10, 40, 80, 14, 22, 12, 13, 45, 11)), 1):
            x_ = ls.cell(row=3, column=c, value=h); x_.font, x_.fill = f(bold=True, color="FFFFFF"), hdr_fill
            ls.column_dimensions[x_.column_letter].width = w
        # Links row = product row + 0 (both start at row 5 for item 1? product tab starts at 5, links at 4) → keep aligned:
        dv_l = DataValidation(type="list", formula1='"' + ",".join(LISTERS) + '"', allow_blank=True)
        dv_s = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=False)
        ls.add_data_validation(dv_l); ls.add_data_validation(dv_s)
        for i, x in enumerate(rows):
            r = H + 1 + i   # zelfde rij als op het producttabblad
            for c, v in enumerate([i + 1, f"Week {x['week']}", x.get("name") or None, x["url"], x["price"], x["source"], x["lister"] or None,
                                   x["status"] or "Not listed", x["comment"] or None, x["added"]], 1):
                ls.cell(row=r, column=c, value=v).font = f()
            ls.cell(row=r, column=4).hyperlink = x["url"]
            ls.cell(row=r, column=4).font = f(color="1F5FBF", underline="single")
            ls.cell(row=r, column=5).number_format = "0.00"
            for c in (3, 7, 8, 9):
                ls.cell(row=r, column=c).fill = PatternFill("solid", fgColor="FFF2CC")
            dv_l.add(ls.cell(row=r, column=7)); dv_s.add(ls.cell(row=r, column=8))
        lastl = H + max(len(rows), 1)
        for name, (bg, fg) in st_col.items():
            ls.conditional_formatting.add(f"H{H+1}:H{lastl}", FormulaRule(formula=[f'$H{H+1}="{name}"'],
                                          fill=PatternFill("solid", fgColor=bg), font=Font(name=F, bold=True, color=fg)))
        ls.row_dimensions[4].height = 6   # lege rij zodat rijnummers gelijk lopen met het producttabblad
        ls.freeze_panes = "E5"
        ls.auto_filter.ref = f"A3:J{lastl}"
    wb.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", nargs="*")
    ap.add_argument("--aantal", type=int, default=200, help="max aantal OPEN (Not listed) producten per store")
    ap.add_argument("--merge", help="teruggestuurde Launch File: statussen behouden en lijst aanvullen")
    ap.add_argument("--update", action="store_true", help="aanvullen vanuit launch_state.json (al opgeschoond)")
    a = ap.parse_args()
    cfg = json.loads((BASE / "config/stores.json").read_text())
    fx = cfg["fx_naar_eur"]
    pool = json.loads((CACHE / "pool.json").read_text())
    import csv
    load_eligible()
    names = {r["Domein"]: r["Store"] for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8"))}
    names.update({s["domain"]: s["name"] for s in pool["stores"] if s["name"] != s["domain"]})
    for s_ in pool["stores"]:
        s_["visits"] = VISITS.get(s_["domain"], 0)
    for r_ in pool["products"]:
        r_["visits"] = VISITS.get(r_["store"], 0)
    in_pool = {s_["domain"] for s_ in pool["stores"]}
    print(f"Toegestane bronnen: {len(ELIGIBLE & in_pool)} (niet in pool: {sorted(ELIGIBLE - in_pool)})", file=sys.stderr)
    groups = build_groups(pool)
    OUT.mkdir(exist_ok=True)
    stores = [s for s in cfg["stores"] if not s.get("_noot")]
    if a.store:
        stores = [s for s in stores if s["naam"] in a.store]

    old = {}
    if a.update and STATE.exists():
        old = json.loads(STATE.read_text())
        for rows in old.values():
            for x in rows:
                x["status"] = x.get("status") or "Not listed"
        print(f"Update: {sum(len(v) for v in old.values())} bestaande regels uit launch_state.json", file=sys.stderr)
    if a.merge:
        state = json.loads(STATE.read_text()) if STATE.exists() else {}
        import clean_returned as cr
        stat = {(f"{k[:22]} – Links", u): cr.clean(v) for k, rows in cr.read_file(a.merge).items() for u, v in rows.items()}
        for sn, rows in state.items():
            lt = f"{sn[:22]} – Links"
            for x in rows:
                x.update(stat.get((lt, x["url"]), {}))
            old[sn] = rows
        print(f"Merge: {sum(len(v) for v in old.values())} bestaande regels, {len(stat)} statussen uit {a.merge}", file=sys.stderr)
    taken = {}
    for s in stores:
        for x in old.get(s["naam"], []):
            for m in s["markten"]:
                taken.setdefault(m, set()).add(x["key"])
    order = {s["naam"]: i for i, s in enumerate(stores)}
    results = []
    for s in sorted(stores, key=lambda s: len(s["markten"])):
        prev = old.get(s["naam"], [])
        open_prev = sum(1 for x in prev if (x.get("status") or "Not listed") == "Not listed")
        need = max(a.aantal - open_prev, 0)
        picks, own = (select_for_store(s, pool, groups, fx, names, taken, need, existing=prev) if need
                      else ([], own_catalog(s["domein"])))
        rows = prev + [to_row(e, s, names) for e in picks]
        print(f"   {s['naam']}: {len(prev)} bestaand ({open_prev} open) + {len(picks)} nieuw", file=sys.stderr)
        results.append((s, rows, own))
    # Niet-geselecteerde stores (bij --store) blijven ongewijzigd in het bestand staan.
    prev_state = json.loads(STATE.read_text()) if STATE.exists() else {}
    done = {s["naam"] for s, _, _ in results}
    for s in cfg["stores"]:
        if s.get("_noot") or s["naam"] in done or s["naam"] not in prev_state:
            continue
        rows = old.get(s["naam"]) or prev_state[s["naam"]]
        results.append((s, rows, own_catalog(s["domein"])))
        order.setdefault(s["naam"], len(order))
    allnames = [s["naam"] for s in cfg["stores"] if not s.get("_noot")]
    results.sort(key=lambda t: allnames.index(t[0]["naam"]))
    state = {s["naam"]: rows for s, rows, _ in results}
    STATE.write_text(json.dumps(state, ensure_ascii=False))
    path = OUT / FILE_NAME
    write_workbook(results, pool, names, path)
    print(f"→ {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
