"""Leest Google Ads-productrapporten (export uit Merchant/Ads, UTF-16 TSV) en geeft de bestsellers per store
(omzet = conv.waarde, opgeteld over varianten) met hun productlink.

Gebruik:  python3 bestsellers_google.py data/google/davento_….csv:davento.it data/google/niaali_….csv:niaali.com [--top 10]
"""
import argparse, csv, json, re, sys
from pathlib import Path
import product_picker as pp

BASE = Path(__file__).parent


def num(x):
    x = re.sub(r"[^\d,.-]", "", x or "").replace(".", "").replace(",", ".")
    try:
        return float(x)
    except ValueError:
        return 0.0


def read(path):
    t = open(path, encoding="utf-16").read().splitlines()
    rows = list(csv.reader(t[2:], delimiter="\t"))
    return [dict(zip(rows[0], r)) for r in rows[1:] if len(r) > 5]


def bestsellers(path, domain, top=10):
    prods = {p["id"]: p for p in pp.fetch_products(domain)}
    agg = {}
    for r in read(path):
        m = re.match(r"shopify_\w+?_(\d+)_(\d+)", r["Item-ID"])
        if not m:
            continue
        a = agg.setdefault(int(m.group(1)), dict(cost=0, conv=0, value=0, clicks=0, title=r["Titel"].rsplit(",", 1)[0], price=r["Prijs"]))
        a["cost"] += num(r["Kosten"]); a["conv"] += num(r["Conversies"]); a["value"] += num(r["Conv.waarde"])
        a["clicks"] += num(r["Klikken op product"])
    out = []
    for pid, a in sorted(agg.items(), key=lambda x: -x[1]["value"])[:top]:
        p = prods.get(pid)
        out.append(dict(a, id=pid, store=domain, handle=p["handle"] if p else None,
                        url=f"https://{domain}/products/{p['handle']}" if p else None,
                        shop_title=p["title"] if p else None, roas=round(a["value"] / max(a["cost"], 0.01), 2)))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("rapporten", nargs="+")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    res = {}
    for arg in a.rapporten:
        path, dom = arg.rsplit(":", 1)
        res[dom] = bestsellers(path, dom, a.top)
        for b in res[dom]:
            print(f"{dom:12} omzet {b['value']:7.0f} spend {b['cost']:6.0f} ROAS {b['roas']:4.1f} | {b['shop_title']} | {b['url']}")
    (BASE / "data/google/bestsellers.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
