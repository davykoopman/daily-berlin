"""Look-alikes van eigen bestsellers zoeken in de pool (.cache/pool.json).

  python3 lookalikes.py sheet <familie> <M|W|any> [n]   → contactsheet + json in --out (visueel kiezen)
  python3 lookalikes.py check <picks.json> <out.json>     → China-bewijs, ≥3 foto's (kleurvarianten tellen), leverbaar, geen merk

picks.json: [{"family": "...", "sheet": "<familie>_<g>", "idx": [..], "gender": "M", "base_eur": 99.9, "cat": "Tussenjas"}]
Kandidaten worden gesorteerd op bestseller-positie (pct) bij de competitor: liefst look-alikes die zelf ook bestseller zijn.
"""
import argparse, collections, concurrent.futures as cf, io, json, re, sys
from pathlib import Path
import numpy as np
import imagehash
import product_picker as pp
import photo_upgrade as pu

BASE = Path(__file__).parent
R = lambda s: re.compile(s, re.I)
W = R(r"damen|donna|damsk|women|femme|mujer|dames|ladies|frauen|kobiet")
M = R(r"herren|uomo|męsk|mesk|\bmen'?s?\b|homme|hombre|heren|\bman\b")
LONG = R(r"lang|long|lungo|lunga|maxi|midi|dług|knielang|wadenlang")
PUFF = r"puffer|stepp|quilt|doudoune|piumin|puchow|pikow|padded|wattiert|daunen|imbottit|trapunt|matelass"
HOOD = r"kapuz|hood|cappucc|capuch|kaptur|capucha"
SPEC = {
    "glossy_puffer":   dict(cats=["Winterjas", "Tussenjas"], inc=R(r"glän|glanz|gloss|shiny|lucid|brillant|lakier|błyszcz|wet look|metall"), extra=R(PUFF), long=False),
    "short_puffer_hood": dict(cats=["Winterjas", "Tussenjas"], inc=R(PUFF), extra=R(HOOD), long=False),
    "long_puffer":     dict(cats=["Winterjas", "Tussenjas"], inc=LONG, extra=R(PUFF + "|down"), long=True),
    "light_quilt":     dict(cats=["Tussenjas", "Winterjas"], inc=R(r"stepp|quilt|trapunt|matelass|pikowan|acolch|leicht|light|stehkragen|stand.?collar|collo alto"), extra=R(PUFF), long=False, nohood=True),
    "suede_sherpa":    dict(cats=["Tussenjas", "Winterjas"], inc=R(r"wildleder|suede|scamosciat|daim|zamsz|ante\b|velours|lammfell|shearling|aviator|pilot|flieger"), extra=R(r"sherpa|teddy|fell|fur|pelz|futro|shearling|lammfell|foder|lined|gefüttert|doubl"), long=False),
    "suede_zip":       dict(cats=["Tussenjas"], inc=R(r"wildleder|suede|scamosciat|daim|zamsz|ante\b|velours"), extra=None, long=False),
    "snow_jacket":     dict(cats=["Winterjas", "Tussenjas", "Set"], inc=R(r"ski|snow|schnee|neve|neige|nieve|narciar|softshell|outdoor|montagn|berg|wasserdicht|waterproof|imperme"), extra=None, long=None),
    "knit_dress":      dict(cats=["Jurk", "Trui / hoodie"], inc=R(r"strickkleid|pulloverkleid|knit dress|sweater dress|abito maglion|abito in maglia|robe pull|robe en maille|vestido de punto|sukienka.*(dzian|swetr)|jumper dress"), extra=None, long=None),
    "long_coat_w":     dict(cats=["Winterjas", "Tussenjas", "Blazer"], inc=R(r"mantel|coat|cappott|manteau|płaszcz|abrigo"), extra=LONG, long=None),
    "parka":           dict(cats=["Winterjas", "Tussenjas"], inc=R(r"parka"), extra=None, long=None),
    "trench":          dict(cats=["Winterjas", "Tussenjas"], inc=R(r"trench"), extra=None, long=None),
    "oversize_cardigan": dict(cats=["Vest / cardigan", "Trui / hoodie"], inc=R(r"cardigan|strickjacke|gilet|kardigan|rebeca"), extra=R(r"oversize|grob|chunky|button|knöpf|bottoni|bouton|guzik"), long=None),
    "tracksuit":       dict(cats=["Set"], inc=R(r"jogging|tracksuit|trainings|dres|tuta|survêt|chándal|sport|hoodie|kapuz|hood|felpa|sweat"), extra=None, long=None),
    "hooded_winter_m": dict(cats=["Winterjas", "Tussenjas"], inc=R(HOOD), extra=R(r"winter|kalt|cold|fredd|hiver|invierno|zim|warm|foder|lined|gefüttert|imbott|padded"), long=False),
    "wide_jeans":      dict(cats=["Broek"], inc=R(r"jeans|denim"), extra=R(r"weit|wide|baggy|relaxed|loose|ampi|large|ancho|szerok|straight|gerade"), long=None),
    "bomber":          dict(cats=["Tussenjas", "Winterjas"], inc=R(r"bomber|blouson"), extra=None, long=False),
    "corduroy":        dict(cats=["Broek", "Blazer", "Tussenjas"], inc=R(r"cord\b|kord|corduroy|velluto|velours côtel|pana\b|sztruks"), extra=None, long=None),
    "cargo":           dict(cats=["Broek"], inc=R(r"cargo|utility"), extra=None, long=None),
    "wool_coat_m":     dict(cats=["Winterjas", "Tussenjas"], inc=R(r"wollmantel|wool coat|cappotto|manteau|płaszcz|abrigo|mantel|overcoat|peacoat|caban"), extra=None, long=None),
    "knit_vest_m":     dict(cats=["Vest / cardigan", "Trui / hoodie", "Blazer"], inc=R(r"weste|vest\b|gilet|kamizel|chaleco|pullunder|slipover"), extra=R(r"strick|knit|maglia|tricot|punto|dzian|v-?neck|v-ausschnitt|scollo a v|col v"), long=None),
    "field_jacket":    dict(cats=["Tussenjas", "Winterjas"], inc=R(r"field|feld|m-?65|cargo|utility|safari|militar|military|polow|worker|work jacket|multi.?pocket"), extra=None, long=None),
    "suit_m":          dict(cats=["Set", "Blazer"], inc=R(r"anzug|suit|completo|costume|traje|garnitur|zweiteil|2-?piece|two.?piece|set\b|komplet|conjunto|ensemble"), extra=R(r"anzug|suit|blazer|sakko|giacca|veste|chaqueta|marynark|smart|elegant|formal|casual"), long=None),
    "boots_m":         dict(cats=["Laarzen", "Schoenen"], inc=R(r"stiefel|boot|stivale|botte|bota|kozak|trzewik|scarpa alta|high.?top|chelsea"), extra=None, long=None),
}


def gender_of(t):
    return "M" if M.search(t) and not W.search(t) else "W" if W.search(t) and not M.search(t) else "?"


def sheet(fam, gender, n, out):
    sp = SPEC[fam]
    pool = json.loads((BASE / ".cache/pool.json").read_text())
    P = pool["products"]
    cl = collections.Counter(r["cluster"] for r in P if r.get("cluster"))
    res, seen = [], set()
    for r in sorted(P, key=lambda r: -float(r.get("pct") or 0)):
        t = r["title"]
        if r["cat"] not in sp["cats"] or not r.get("img"):
            continue
        g = gender_of(t)
        if gender != "any" and g not in (gender, "?" if gender == "W" else "x"):   # heren: alleen aantoonbaar heren
            continue
        if not sp["inc"].search(t) or (sp["extra"] and not sp["extra"].search(t)):
            continue
        if sp["long"] is True and not LONG.search(t): continue
        if sp["long"] is False and LONG.search(t): continue
        if sp.get("nohood") and re.search(HOOD, t, re.I): continue
        k = r.get("cluster") or r.get("phash")
        if k in seen: continue
        seen.add(k)
        r["g"] = g; r["nst"] = cl[r["cluster"]] if r.get("cluster") else 1
        r["china"] = bool("O1CN" in (r["img"] or "") or any(re.search("1688|ali", x, re.I) for x in (r.get("tags") or [])) or r["nst"] >= 2)
        res.append(r)
    res = res[:n]
    tag = f"{fam}_{gender}"
    Path(out).mkdir(parents=True, exist_ok=True)
    (Path(out) / f"{tag}.json").write_text(json.dumps(res))
    from PIL import Image, ImageDraw
    def load(u):
        try: return Image.open(io.BytesIO(pp.get(u + ("&" if "?" in u else "?") + "width=200", binary=True))).convert("RGB").resize((140, 170))
        except Exception: return Image.new("RGB", (140, 170), "grey")
    with cf.ThreadPoolExecutor(10) as ex: ims = list(ex.map(lambda r: load(r["img"]), res))
    sh = Image.new("RGB", (10 * 145, max(1, (len(res) + 9) // 10) * 190), "white"); d = ImageDraw.Draw(sh)
    for j, (r, im) in enumerate(zip(res, ims)):
        x, y = (j % 10) * 145, (j // 10) * 190
        sh.paste(im, (x, y + 16)); d.text((x + 2, y + 2), f"{j} {'C' if r['china'] else ''}{r['g']} {float(r.get('pct') or 0):.2f} {r['store'][:10]}", fill="red" if r["china"] else "black")
    sh.save(Path(out) / f"{tag}.png"); print(tag, len(res))


def check(picks_path, out_path):
    import select_products as sp_
    sp_.load_eligible()
    picks = json.loads(Path(picks_path).read_text())
    folder = Path(picks_path).parent
    pool = json.loads((BASE / ".cache/pool.json").read_text()); P = [r for r in pool["products"] if r.get("phash")]
    H = np.array([int(r["phash"], 16) for r in P], dtype=np.uint64)
    cur = {s["domain"]: s["currency"] for s in pool["stores"]}
    BRAND = R(r"fila|adidas|nike|puma|moncler|canada goose|north face|ralph|tommy|lacoste|gucci|prada|burberry|stone island|ugg|celine|chanel|dior|louis|zara|levi")
    cands = []
    for pk in picks:
        js = json.loads((folder / f"{pk['sheet']}.json").read_text())
        for i in pk["idx"]:
            r = js[i]
            cands.append(dict(url=f"https://{r['store']}/products/{r['handle']}", store=r["store"], handle=r["handle"], title=r["title"],
                              gender=pk["gender"], fam=pk["family"], base=pk["base_eur"], cat=pk["cat"], pct=float(r.get("pct") or 0)))
    seen = set(); cands = [c for c in cands if not (c["url"] in seen or seen.add(c["url"]))]
    with cf.ThreadPoolExecutor(5) as ex: G = list(ex.map(lambda c: pu.gallery(c["store"], c["handle"]), cands))
    gh = pp.hash_images([pu.W(u) for g in G if g for u, _, _ in g["imgs"][:12]])
    ok, drop = [], collections.Counter()
    for c, g in zip(cands, G):
        if not g or not g["imgs"] or not g["avail"]: drop["niet actief/leverbaar"] += 1; continue
        hh = [imagehash.hex_to_hash(gh[pu.W(u)]) for u, _, _ in g["imgs"][:12] if gh.get(pu.W(u))]
        distinct = []
        for h in hh:
            if all(h - d > 4 for d in distinct): distinct.append(h)
        others = set()
        for h in hh[:6]:
            for j in np.nonzero(np.bitwise_count(H ^ np.uint64(int(str(h), 16))) <= 5)[0]: others.add(P[j]["store"])
        others.discard(c["store"])
        ali = any(re.search(r"O1CN|alicdn", u) for u, _, _ in g["imgs"])
        if not pu.enough_photos(g, len(distinct)): drop["<3 foto's"] += 1; continue
        if not (others or ali): drop["geen China-bewijs"] += 1; continue
        if BRAND.search(c["title"]): drop["merk"] += 1; continue
        c.update(others=sorted(others), ali=ali, q=pu.quality(g, gh)[0], src_cur=cur.get(c["store"], "EUR"), visits=sp_.VISITS.get(c["store"], 0))
        ok.append(c)
    print(f"kandidaten {len(cands)} → door checks {len(ok)} {dict(drop)}", file=sys.stderr)
    Path(out_path).write_text(json.dumps(ok, ensure_ascii=False, indent=1))


def auto(spec_path, out):
    """spec: [{"family","gender","n","base_eur","cat","label"}] → per familie de n beste kandidaten met China-vlag en
    bestseller-positie ≥ 0.5 (look-alikes die zelf ook verkopen), daarna check() en één review-sheet."""
    spec = json.loads(Path(spec_path).read_text())
    picks = []
    for f in spec:
        sheet(f["family"], f["gender"], 200, out)
        js = json.loads((Path(out) / f"{f['family']}_{f['gender']}.json").read_text())
        idx = [i for i, r in enumerate(js) if r["china"] and float(r.get("pct") or 0) >= 0.5][: f["n"]]
        picks.append(dict(family=f["label"], sheet=f"{f['family']}_{f['gender']}", idx=idx, gender=f["gender"], base_eur=f["base_eur"], cat=f["cat"]))
    (Path(out) / "picks.json").write_text(json.dumps(picks, indent=1))
    check(str(Path(out) / "picks.json"), str(Path(out) / "ok.json"))
    ok = json.loads((Path(out) / "ok.json").read_text())
    from PIL import Image, ImageDraw
    def load(u):
        try: return Image.open(io.BytesIO(pp.get(u + ("&" if "?" in u else "?") + "width=200", binary=True))).convert("RGB").resize((120, 150))
        except Exception: return Image.new("RGB", (120, 150), "grey")
    P = {(r["store"], r["handle"]): r for f in spec for r in json.loads((Path(out) / f"{f['family']}_{f['gender']}.json").read_text())}
    with cf.ThreadPoolExecutor(10) as ex: ims = list(ex.map(lambda c: load(P[(c["store"], c["handle"])]["img"]), ok))
    sh = Image.new("RGB", (12 * 125, max(1, (len(ok) + 11) // 12) * 175), "white"); d = ImageDraw.Draw(sh)
    for j, (c, im) in enumerate(zip(ok, ims)):
        x, y = (j % 12) * 125, (j // 12) * 175
        sh.paste(im, (x, y + 22)); d.text((x + 2, y + 2), f"{j} {c['fam'][:16]}", fill="black"); d.text((x + 2, y + 12), c["store"][:18], fill="grey")
    sh.save(Path(out) / "review.png"); print("review", len(ok))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd"); ap.add_argument("args", nargs="*")
    ap.add_argument("--out", default=str(BASE / ".cache/lookalikes"))
    a = ap.parse_args()
    if a.cmd == "sheet":
        sheet(a.args[0], a.args[1], int(a.args[2]) if len(a.args) > 2 else 60, a.out)
    elif a.cmd == "auto":
        auto(a.args[0], a.out)
    elif a.cmd == "check":
        check(a.args[0], a.args[1])
