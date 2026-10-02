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
MARKET_NAME = {"DE": "Duitsland", "FR": "Frankrijk", "UK": "VK", "IT": "Italië", "ES": "Spanje", "PL": "Polen",
               "US": "VS", "CA": "Canada", "NL": "Nederland", "AT": "Oostenrijk", "CH": "Zwitserland"}


# Alleen deze competitors mogen bronlink zijn: geverifieerd ≥75K bezoekers/mnd (SimilarWeb-hoofdcijfer),
# match-score ≥4 (zelfde dropship-model, geen eigen label) en geen onbevestigde/geschatte cijfers.
MIN_SOURCE_VISITS = 75000
ELIGIBLE, VISITS = set(), {}


def load_eligible():
    import csv
    for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8")):
        v = int(r["Bezoekers per maand"] or 0)
        n = r["Notities"].lower()
        VISITS[r["Domein"]] = v
        if (v >= MIN_SOURCE_VISITS and int(r["Match-score"] or 0) >= 4 and "referentie" not in n
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
    hashes = pp.hash_images(imgs)
    g = [gender(p["title"], p.get("product_type") or "") for p in prods]
    share_w = g.count("W") / max(g.count("W") + g.count("M"), 1)
    prices = sorted(float(p["variants"][0]["price"]) for p in prods if p.get("variants"))
    return dict(n=len(prods), hashes=[h for h in hashes.values() if h], share_w=share_w,
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
        return 0, "geen foto-info"
    n = len(media)
    w, h = media[0].get("w") or 0, media[0].get("h") or 0
    s_n = min(n, 6) / 6 * 35
    s_res = (min(min(w, h), 1200) / 1200 * 40) if w and h else 15
    r = (h / w) if w else 1
    s_ar = 25 if 1.15 <= r <= 1.55 else 18 if 0.95 <= r < 1.15 else 8
    txt = f"{n} foto's, 1e {w}×{h}" if w else f"{n} foto's"
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
    """Gebruikt een concurrent in jouw markt dezelfde hoofdfoto? Dan een andere foto als eerste."""
    rivals = [m for m in ev["in_m"] if m is not src]
    if src["market"] in markets:
        rivals.append(src)  # bron zelf is concurrent in jouw markt
    if not rivals:
        return "Hoofdfoto vrij te gebruiken (geen concurrent in jouw markt)"
    gal = media.get(f'{src["store"]}/{src["handle"]}') or []
    if len(gal) >= 2:
        return f"Zelfde hoofdfoto als {len({r['store'] for r in rivals})} concurrent(en) in jouw markt → zet foto 2 (of een modelfoto) als eerste"
    return "Zelfde hoofdfoto als concurrent in jouw markt → gebruik een andere foto (leverancier) als eerste"


def price_advice(ev, store_cur, fx, bands):
    src = ev["best"]
    p25, p50, p75 = bands.get(src["cat"], (None, None, None))
    if src["cur"] == store_cur:
        advies = src["price"]
        why = "prijs van de bronlink overnemen"
    else:
        advies = round_price(src["price_eur"], store_cur, fx)
        why = f"prijs van de bronlink ({src['price']:.2f} {src['cur']}) omgerekend"
    hoger = None
    if p50 and src["price_eur"] < p25:
        hoger = round_price(p50, store_cur, fx)
        why += f"; ligt onder de sweet spot, kan hoger: {hoger:.2f}"
    ins = [m for m in ev["in_m"] if m["pct"] >= 0.75]
    if ins:
        why += f"; let op: al bestseller bij {len({m['store'] for m in ins})} competitor(s) in jouw markt"
    band = (f"{round_price(p25, store_cur, fx):.0f}–{round_price(p75, store_cur, fx):.0f}" if p25 else "")
    return advies, band, why, hoger


def explain(ev, markets, names):
    b = ev["best"]
    nm = lambda d: names.get(d, d)
    parts = []
    top = f"top {max(1, round((1 - b['pct']) * 100))}%"
    parts.append(f"{top} bestseller bij {nm(b['store'])} ({b['market']}, {b['visits']/1000:.0f}K bez./mnd)" if b["visits"]
                 else f"{top} bestseller bij {nm(b['store'])} ({b['market']})")
    others = sorted({(nm(m["store"]), m["market"], m["store"] in ELIGIBLE) for m in ev["members"] if m["store"] != b["store"]},
                    key=lambda t: (not t[2], t[0]))
    if others:
        parts.append("ook bij " + ", ".join(f"{s} ({mk}{'' if big else ', klein'})" for s, mk, big in others[:4])
                     + (f" +{len(others) - 4}" if len(others) > 4 else ""))
    if not ev["stores_in"]:
        parts.append(f"nog bij géén competitor in {'/'.join(markets)} → vrije ruimte")
    else:
        parts.append(f"{len(ev['stores_in'])} competitor(s) in {'/'.join(markets)}")
    if ev["newest"] <= 21:
        parts.append(f"{ev['newest']} dagen geleden toegevoegd")
    parts.append(f"seizoensfit {ev['season']:.1f}")
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


def select_for_store(store, pool, groups, fx, names, taken, n_target):
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
        if len(picked) >= int(n_target * 1.2):
            break
    bands = price_bands(pool, markets)
    media = fetch_media([m for e in picked for m in e["members"]])
    for e in picked:
        e["best"] = choose_source(e, store["valuta"], markets, media)
        # Foto's wegen mee: 1e foto bepaalt de klikratio. ±8 punten rond een gemiddelde score van 70.
        e["score"] = round(e["score"] + (e["best"]["img_score"] - 70) / 3.75, 1)
    picked = [e for e in picked if e["best"]["img_score"] >= 45] or picked
    picked.sort(key=lambda e: -e["score"])
    picked = picked[:n_target]
    for m in markets:
        taken.setdefault(m, set()).update(e["key"] for e in picked)
    for e in picked:
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
    "A": ("A · Bewezen elders, vrij in jouw markt", "Bestseller bij competitor(s) in een ander land, terwijl nog geen enkele competitor in jouw markt hem verkoopt. Beste kans: bewezen product zonder prijsconcurrentie."),
    "B": ("B · Breed bewezen", "Bij 3+ competitors te koop en minstens ergens een bestseller. Meerdere sterke stores zetten erop in: lage gok."),
    "C": ("C · Nieuw & opkomend", "≤21 dagen live bij een sterke competitor en nu al in de top 40% van zijn ranking. Vroeg instappen voor hij overal staat."),
    "D": ("D · Bewezen in jouw markt", "Bestseller bij één competitor in jouw land (bij 3+ laten we hem weg). Vraag is bewezen; je concurreert op advertentie en foto's, niet op prijs."),
    "E": ("E · Nieuw bij topcompetitor", "Net toegevoegd (≤14 dagen) door een store met 150K+ bezoekers. Nog niet bewezen, maar die stores testen gericht."),
}


def write_workbook(results, pool, names, path):
    """Eén bestand: 'Strategie & uitleg' + per store een tab 'Te listen' en een tab 'Links'."""
    from collections import Counter
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as XLImage
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from PIL import Image

    F, navy = "Arial", "1F2A44"
    f = lambda **k: Font(name=F, size=k.pop("size", 10), **k)
    thin = Border(bottom=Side(style="thin", color="D9DDE3"))
    hdr_fill = PatternFill("solid", fgColor=navy)
    sfill = {"A": "C6EFCE", "B": "DDEBF7", "C": "FCE4D6", "D": "FFF2CC", "E": "EDE7F6"}
    wb = Workbook()

    def thumb(u):
        try:
            im = Image.open(io.BytesIO(pp.get(u, binary=True, timeout=20))).convert("RGB")
            im.thumbnail((84, 84)); b = io.BytesIO(); im.save(b, "JPEG", quality=78); b.seek(0)
            return b
        except Exception:
            return None

    # ---------- Strategie & uitleg ----------
    sg = wb.active
    sg.title = "Strategie & uitleg"
    sg.column_dimensions["A"].width = 30
    sg.column_dimensions["B"].width = 120
    sg["A1"], sg["A1"].font = "Listingplan – alle stores", f(size=15, bold=True, color=navy)
    sg["A2"] = f"Gemaakt {dt.date.today():%d-%m-%Y} · per store een tab 'Te listen' en een tab 'Links' · ±15-25 per dag"
    sg["A2"].font = f(italic=True, color="666666")
    big = sorted((d for d in ELIGIBLE), key=lambda d: -VISITS.get(d, 0))
    rules = [
        ("Bronnen (importlinks)", f"Uitsluitend {len(big)} competitors met een geverifieerd SimilarWeb-cijfer van ≥75K bezoekers/mnd, "
         "hetzelfde dropship-model (match ≥4) en geen eigen label. Kleinere of onbevestigde stores tellen alleen mee als "
         "bevestiging ('ook bij …, klein') en voor verzadiging, nooit als bron."),
        ("Bronkeuze per product", "Liefst een competitor in een ánder land dan jouw markt (zelfde foto + prijs bij een binnenlandse "
         "concurrent = directe concurrentie). Daarbinnen: goed verkopend, beste foto's, dezelfde valuta, hoogste prijs. "
         "'⚠ eigen markt' = alleen een binnenlandse grote bron: volg het foto-advies."),
        ("Prijs", "Adviesprijs = prijs van de bronlink (overnemen; andere valuta → omgerekend, ,95). Nooit onderprijzen. "
         "Onder de sweet spot van de categorie (P25–P75 van bestsellers) → 'kan hoger'."),
        ("Foto's", "Foto-score 0-100 (≥6 foto's, 1e foto ≥1200 px, staand 3:4/4:5). Telt mee in de volgorde; zwakke foto's eruit."),
        ("Seizoen & volgorde", "Week 1-2 herfstlagen, week 3 winterjassen/laarzen (koude markten), week 4 kerst."),
        ("Dubbelcheck", "Wat al in je store staat is eruit (fotovergelijking). Stores met dezelfde markt (UK) krijgen nooit hetzelfde product."),
        ("", "")]
    for s_ in "ABCDE":
        rules.append((STRAT_TXT[s_][0], STRAT_TXT[s_][1]))
    rules += [("", ""), ("Let op", "Bestseller-rank = positie in 'best verkocht' van de store zelf, geen verkoopaantal. "
               "Gebruik bij voorkeur leveranciersfoto's of eigen teksten, niet alles 1-op-1 van de competitor.")]
    r0 = 4
    for i, (k, v) in enumerate(rules):
        sg.cell(row=r0 + i, column=1, value=k).font = f(bold=True)
        c = sg.cell(row=r0 + i, column=2, value=v); c.font = f(); c.alignment = Alignment(wrap_text=True, vertical="top")
    r = r0 + len(rules) + 1
    sg.cell(row=r, column=1, value="Per store").font = f(size=12, bold=True, color=navy)
    r += 1
    for store, picks, own in results:
        cnt, cats, wk = Counter(e["strat"] for e in picks), Counter(e["best"]["cat"] for e in picks), Counter(e["week"] for e in picks)
        src = Counter(e["best"]["store"] for e in picks)
        txt = (f"Markt: {', '.join(MARKET_NAME.get(m, m) for m in store['markten'])} · {store['valuta']} · catalogus {own['n']} producten "
               f"({own['share_w']:.0%} dames) · {len(picks)} picks\n"
               f"Strategie: " + ", ".join(f"{k} {cnt[k]}" for k in "ABCDE" if cnt.get(k)) + "\n"
               f"Categorieën: " + ", ".join(f"{k} {v}" for k, v in cats.most_common()) + "\n"
               f"Listweken: " + ", ".join(f"week {k}: {v}" for k, v in sorted(wk.items())) + "\n"
               f"Bronnen: " + ", ".join(f"{names.get(d, d)} ({VISITS.get(d, 0)/1000:.0f}K) {n}×" for d, n in src.most_common()))
        sg.cell(row=r, column=1, value=store["naam"]).font = f(bold=True)
        c = sg.cell(row=r, column=2, value=txt); c.font = f(); c.alignment = Alignment(wrap_text=True, vertical="top")
        sg.row_dimensions[r].height = 92
        r += 1
    r += 1
    sg.cell(row=r, column=1, value="Toegestane bronnen").font = f(size=12, bold=True, color=navy)
    r += 1
    mk = {s["domain"]: s["market"] for s in pool["stores"]}
    for d in big:
        sg.cell(row=r, column=1, value=names.get(d, d)).font = f()
        sg.cell(row=r, column=2, value=f"{mk.get(d, '')} · {VISITS.get(d, 0):,} bezoekers/mnd".replace(",", ".")).font = f()
        r += 1

    # ---------- per store ----------
    heads = ["#", "Foto", "Listweek", "Strategie", "Score", "Product (bron-titel)", "Categorie", "D/H", "Waarom dit product",
             "Adviesprijs", "Sweet spot categorie", "Prijsadvies", "Inkoop – zelf invullen", "Marge %",
             "Bron (importlink)", "Bron", "Bron-land", "Foto-score", "Foto's", "Foto-advies", "Andere (grote) bronnen", "Gelist?"]
    widths = [5, 13, 9, 26, 7, 42, 15, 5, 70, 11, 12, 34, 12, 9, 12, 20, 10, 9, 18, 38, 40, 9]
    for store, picks, own in results:
        cur = store["valuta"]
        ws = wb.create_sheet(store["naam"][:31])
        ws.sheet_properties.tabColor = "F4B183"
        ws["A1"] = f"{store['naam']} – {len(picks)} producten om te listen ({'/'.join(MARKET_NAME.get(m, m) for m in store['markten'])}, {cur})"
        ws["A1"].font = f(size=15, bold=True, color=navy)
        ws["A2"] = "Gesorteerd op listweek en score · bronnen alleen grote competitors (≥75K bezoekers/mnd, geverifieerd)"
        ws["A2"].font = f(italic=True, color="666666")
        H = 4
        for i, (h, w) in enumerate(zip(heads, widths), 1):
            hv = f"{h} ({cur})" if h in ("Adviesprijs", "Sweet spot categorie", "Inkoop – zelf invullen") else h
            c = ws.cell(row=H, column=i, value=hv)
            c.font, c.fill = f(bold=True, color="FFFFFF"), hdr_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[H].height = 32
        dv = DataValidation(type="list", formula1='"ja,nee"', allow_blank=True)
        ws.add_data_validation(dv)
        with cf.ThreadPoolExecutor(16) as ex:
            thumbs = list(ex.map(lambda e: thumb(e["best"]["img"]) if e["best"]["img"] else None, picks))
        for i, (e, tb) in enumerate(zip(picks, thumbs)):
            r = H + 1 + i
            b = e["best"]
            alts = [f'https://{m["store"]}/products/{m["handle"]}' for m in e["big"] if m is not b][:3]
            vals = [i + 1, "", f"Week {e['week']}", STRAT_TXT[e["strat"]][0], e["score"], b["title"], b["cat"], e["gender"],
                    e["uitleg"], e["advies"], e["band"], e["prijs_why"], None, None, "Open",
                    f"{names.get(b['store'], b['store'])} ({VISITS.get(b['store'], 0)/1000:.0f}K)",
                    b["market"] + (" ⚠ eigen markt" if e["bron_in_markt"] else ""), b.get("img_score"), b.get("img_txt"),
                    e["foto_advies"], "\n".join(alts), "nee"]
            for j, v in enumerate(vals, 1):
                c = ws.cell(row=r, column=j, value=v)
                c.font, c.border = f(), thin
                c.alignment = Alignment(vertical="center", wrap_text=j in (4, 6, 9, 12, 16, 20, 21))
            ws.row_dimensions[r].height = 66
            ws.cell(row=r, column=4).fill = PatternFill("solid", fgColor=sfill[e["strat"]])
            for col in (10, 13):
                ws.cell(row=r, column=col).number_format = "0.00"
            inp = ws.cell(row=r, column=13)
            inp.fill, inp.font = PatternFill("solid", fgColor="FFF2CC"), f(color="0000FF")
            m = ws.cell(row=r, column=14, value=f'=IF(M{r}="","",(J{r}-M{r})/J{r})')
            m.number_format = "0%"
            lk = ws.cell(row=r, column=15)
            lk.hyperlink, lk.font = f'https://{b["store"]}/products/{b["handle"]}', f(color="1F5FBF", underline="single")
            if e["bron_in_markt"]:
                ws.cell(row=r, column=17).fill = PatternFill("solid", fgColor="FCE4D6")
            g = ws.cell(row=r, column=22)
            g.fill, g.font = PatternFill("solid", fgColor="FFF2CC"), f(color="0000FF")
            dv.add(g)
            if tb:
                im = XLImage(tb); im.anchor = f"B{r}"; ws.add_image(im)
        ws.freeze_panes = "C5"
        ws.auto_filter.ref = f"A{H}:V{H + len(picks)}"

        ls = wb.create_sheet(f"{store['naam'][:22]} – Links")
        ls.sheet_properties.tabColor = "A9D08E"
        ls["A1"], ls["A1"].font = f"{store['naam']}: importlinks in listvolgorde – kopieer per dag 15-25 regels", f(bold=True)
        for c, h in enumerate(["#", "Listweek", "Link", f"Adviesprijs ({cur})", "Bron"], 1):
            x = ls.cell(row=3, column=c, value=h); x.font, x.fill = f(bold=True, color="FFFFFF"), hdr_fill
        for i, e in enumerate(picks):
            b = e["best"]
            for c, v in enumerate([i + 1, f"Week {e['week']}", f'https://{b["store"]}/products/{b["handle"]}', e["advies"],
                                   names.get(b["store"], b["store"])], 1):
                ls.cell(row=4 + i, column=c, value=v).font = f()
        ls.column_dimensions["C"].width = 95
        ls.column_dimensions["B"].width = 10
        ls.column_dimensions["D"].width = 14
        ls.column_dimensions["E"].width = 22
    wb.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", nargs="*")
    ap.add_argument("--aantal", type=int, default=300)
    a = ap.parse_args()
    cfg = json.loads((BASE / "config/stores.json").read_text())
    fx = cfg["fx_naar_eur"]
    pool = json.loads((CACHE / "pool.json").read_text())
    import csv
    load_eligible()
    names = {r["Domein"]: r["Store"] for r in csv.DictReader(open(BASE / "data/competitors.csv", encoding="utf-8"))}
    names.update({s["domain"]: s["name"] for s in pool["stores"] if s["name"] != s["domain"]})
    # Bezoekers altijd uit het masterbestand (ook voor handmatig toegevoegde stores).
    for s_ in pool["stores"]:
        s_["visits"] = VISITS.get(s_["domain"], 0)
    for r_ in pool["products"]:
        r_["visits"] = VISITS.get(r_["store"], 0)
    in_pool = {s_["domain"] for s_ in pool["stores"]}
    print(f"Toegestane bronnen: {len(ELIGIBLE & in_pool)} (niet in pool: {sorted(ELIGIBLE - in_pool)})", file=sys.stderr)
    groups = build_groups(pool)
    print(f"Pool: {len(pool['products'])} producten in {len(groups)} unieke producten", file=sys.stderr)
    OUT.mkdir(exist_ok=True)
    taken = {}
    stores = [s for s in cfg["stores"] if not s.get("_noot")]
    if a.store:
        stores = [s for s in stores if s["naam"] in a.store]
    # Stores met één markt eerst kiezen; zo krijgen Fashionnovo en Alovefashion (alleen UK) eerst de UK-ruimte
    # en krijgt Niaali (PL + UK) daarna wat overblijft. Binnen één markt krijgt geen enkel product twee stores.
    order = {s["naam"]: i for i, s in enumerate(stores)}
    results = []
    for s in sorted(stores, key=lambda s: len(s["markten"])):
        picks, own = select_for_store(s, pool, groups, fx, names, taken, a.aantal)
        results.append((s, picks, own))
    results.sort(key=lambda t: order[t[0]["naam"]])
    path = OUT / f"Listings_alle_stores_{dt.date.today():%Y-%m-%d}.xlsx"
    write_workbook(results, pool, names, path)
    print(f"→ {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
