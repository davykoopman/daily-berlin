# Chargebacks & refunds report (Daily Berlin, Davento, Niaali)

Scripts die de exports van Shopify Payments en PayPal omzetten naar het rapport en de checklist voor productkwaliteit.
Geen klantgegevens of exports in deze map. Exports staan in `exports/` (lokaal, niet committen).

## Wat je per update aanlevert
Per store: orders-export, Shopify Payments transactions-export, payouts-export.
Voor alle stores samen: PayPal-transacties (CSV) en het PayPal geschillenrapport (CSV).
Niet nodig: facturatie (`charges_export`).

## Update draaien
1. Zet de nieuwe bestanden in `exports/` (of zet `EXPORTS_DIR`).
2. Pas bovenin `scripts/store_build.py` aan: `CUT` (laatste dag), `AS_OF`, de bestandsnamen in `STORES` en de PayPal-bestanden (`pdx`, `dis0`).
3. `python3 -I scripts/store_build.py` bouwt per store `data_<store>/` (CSV). Controleer of "unexplained" bij de payouts 0,00 is.
4. `python3 -I scripts/combine.py` voegt de stores samen in `data_all/`.
5. `smoke/run.js` test de pagina (`npm install jsdom d3@7` in `smoke/`).
6. Publiceer de CSV's als assets en `page/report.html` als bestand van het dashboard.

## Nieuwe store toevoegen
Voeg een regel toe aan `STORES` (shop-ID van PayPal, bestanden, prefix). Zonder PayPal: `shop` zonder PayPal-rijen. Andere valuta: `fx=True` (omrekening met de euro-bedragen van Shopify Payments).

## Bekende handmatige onderdelen
- Redenen per ordernummer (`DB_LISTS`, `DAV_LISTS`): uit de notities in Shopify.
- Open bank-inquiries (`inq`) en handmatige refunds (`manual_refund`).
- `not_pp`: orders die Shopify als PayPal markeert maar niet via PayPal liepen.
- Het PayPal-bestand mag overlappen met eerdere bestanden; dubbele rijen worden verwijderd.

## Productmatching
`photomatch.py` + `pmap2.py` + `pmap3.py` koppelen dezelfde producten tussen stores op foto's (publieke `products.json`). `checklist/template.html` is de afvinkpagina (database `status/<id>`).
