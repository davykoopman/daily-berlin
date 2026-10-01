# Niaali – productpagina (Fabric-thema)

Herbruikbare productpagina-opzet ("PP-kit") voor alle stores. Gebouwd en getest op Niaali
(thema-kopie "Fabric - Product page v2", nog niet gepubliceerd).

## Bestanden
| Bestand | Wat het doet |
|---|---|
| `theme/blocks/pp-title.liquid` | Producttitel als `<h1>`, 20px mobiel → 24px desktop |
| `theme/blocks/pp-benefits.liquid` | 3 bullets met icoon: gratis verzending, X-dagen geld-terug-garantie (link naar refund policy), buy more save more. Instelling *Return period in days* per store gelijkzetten aan de refund policy |
| `theme/snippets/pp-i18n.liquid` | Vertalingen voor de kit op basis van de taal van de bezoeker (pl, en, nl, de, fr, it, es; anders Engels) |
| `theme/snippets/price1.liquid` | Prijs: kortingsprijs vet en rood, normale prijs zwart, rood -X%-vakje uit de compare-at-prijs |
| `theme/snippets/cart-products.liquid` | Winkelwagen: kortingsprijs vet en rood (klasse `pp-sale-price`, CSS in `pp-benefits`) |
| `theme/snippets/pp-tier-progress.liquid` | Staffel-voortgangsbalk in Mix & match: leest het aantal producten in de winkelwagen en toont live "Dodaj jeszcze 1 produkt i oszczędź 10%" (eerlijke urgency). Instelling `2:10,3:15,4:20` gelijk aan de kortings-app |
| `theme/snippets/pp-tiers.liquid` | (Niet meer in gebruik) staffel als labels |
| `theme/snippets/pp-reveal.liquid` | Rustig verschijnen bij scrollen (iconenrij en stappen), uit bij "minder beweging" |
| `theme/sections/pp-bundle.liquid` | Mix & match: producten uit dezelfde collectie (heren/dames via collectie-handle), staffel-voortgangsbalk onder de kop, tegel "Bekijk hele collectie", kaart-hover op desktop |
| `theme/blocks/pp-delivery.liquid` | Levertijd onder de knop: "Verzonden binnen [x] werkdagen". Dagen per store gelijkzetten aan de verzendpolicy |
| `theme/sections/header-group.json` | Aankondigingsbalk: 3 wisselende berichten (gratis verzending, staffelkorting, retourdagen), om de 4 sec, op mobiel 1 regel. Teksten per store aanpassen aan de echte staffel en policy, vertalen via *Translate & Adapt* |
| `theme/sections/pp-trust.liquid` | Iconenrij met 4 garanties (verzending, retour + ruilen, veilig betalen, klantenservice met echte openingstijden, klikbaar naar e-mail). Instellingen: retourdagen, e-mail (leeg = store-e-mail), openingstijden en tijdzone (wordt in andere talen dan de hoofdtaal getoond, bv. "(CET)" op /gb). Teksten kort gehouden zodat alles op 1 regel past |
| `theme/sections/pp-steps.liquid` | "Zo werkt het" in 3 stappen (bestellen, thuis passen, niet goed = retour/ruilen). Instellingen: verzenddagen en retourdagen |
| `theme/templates/product.json` | Volgorde: titel → prijs → bullets → kleuren → maten → zwarte Add to cart → betaaliconen (automatisch, wat actief is) |
| `*.original.*` | Back-up van de bestanden vóór de wijziging |

Mix & match (`pp-bundle`): kop + staffel-voortgangsbalk, 4 kaarten desktop / 2 + swipen mobiel, -X% vakje, "W PROMOCJI"-label verborgen, titels max 2 regels, quick add ook op mobiel (CSS in `pp-benefits`, inclusief fix voor de Swatch King-kiezer in het quick add-venster). Volgorde: productinfo → Mix & match → iconenrij → O nas → Zo werkt het → FAQ. O nas op mobiel: lagere foto, tekst links.

Foto's: carousel in 4:5 staand kader, begrensd op schermhoogte, bolletjes op mobiel en desktop.

## Op een nieuwe store zetten
1. Thema dupliceren, bovenstaande bestanden uploaden in de kopie.
2. In de template `return_days` gelijkzetten aan de refund policy van die store; in Mix & match de collectie-handles en staffel invullen.
   In *Theme settings* "Currency code" op productpagina's uit.
3. Teksten in de template (accordions/FAQ) in de hoofdtaal zetten en via *Translate & Adapt* vertalen.
4. Controleren in preview, per markt, op mobiel en desktop. Daarna pas publiceren.

## Policies
`policies/` bevat de verzendpolicy (Pools en Engels) met algemene landen-zin en gratis verzending, plus back-ups (`*.original.*`).
