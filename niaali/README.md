# Niaali – productpagina (Fabric-thema)

Herbruikbare productpagina-opzet ("PP-kit") voor alle stores. Gebouwd en getest op Niaali
(thema-kopie "Fabric - Product page v2", nog niet gepubliceerd).

## Bestanden
| Bestand | Wat het doet |
|---|---|
| `theme/blocks/pp-title.liquid` | Producttitel als `<h1>`, 20px mobiel → 24px desktop |
| `theme/blocks/pp-benefits.liquid` | 3 bullets met icoon: gratis verzending, X-dagen geld-terug-garantie (link naar refund policy), buy more save more. Instelling *Return period in days* per store gelijkzetten aan de refund policy |
| `theme/snippets/pp-i18n.liquid` | Vertalingen voor de kit op basis van de taal van de bezoeker (pl, en, nl, de, fr, it, es; anders Engels) |
| `theme/snippets/price1.liquid` | Prijs: "Save X%" in rood, per variant berekend uit de compare-at-prijs (naar beneden afgerond) |
| `theme/blocks/pp-delivery.liquid` | Levertijd onder de knop: "Verzonden binnen [x] werkdagen". Dagen per store gelijkzetten aan de verzendpolicy |
| `theme/sections/header-group.json` | Aankondigingsbalk: 3 wisselende berichten (gratis verzending, staffelkorting, retourdagen), om de 4 sec, op mobiel 1 regel. Teksten per store aanpassen aan de echte staffel en policy, vertalen via *Translate & Adapt* |
| `theme/sections/pp-trust.liquid` | Iconenrij met 4 garanties (verzending, retour + ruilen, veilig betalen, klantenservice 7 dagen). Instellingen: retourdagen en gebruikelijke reactietijd (uit contactpagina) |
| `theme/sections/pp-steps.liquid` | "Zo werkt het" in 3 stappen (bestellen, thuis passen, niet goed = retour/ruilen). Instellingen: verzenddagen en retourdagen |
| `theme/templates/product.json` | Volgorde: titel → prijs → bullets → kleuren → maten → zwarte Add to cart → betaaliconen (automatisch, wat actief is) |
| `*.original.*` | Back-up van de bestanden vóór de wijziging |

Mix & match (product recommendations): kop + staffelregel, 4 kaarten desktop / 2 + swipen mobiel, -X% vakje, "W PROMOCJI"-label verborgen, titels max 2 regels, quick add ook op mobiel (CSS in `pp-benefits`, inclusief fix voor de Swatch King-kiezer in het quick add-venster). Volgorde: productinfo → Mix & match → iconenrij → O nas → Zo werkt het → FAQ. O nas op mobiel: lagere foto, tekst links.

Foto's: carousel in 4:5 staand kader, begrensd op schermhoogte, bolletjes op mobiel en desktop.

## Op een nieuwe store zetten
1. Thema dupliceren, bovenstaande bestanden uploaden in de kopie.
2. In de template `return_days` gelijkzetten aan de refund policy van die store.
3. Teksten in de template (accordions/FAQ) in de hoofdtaal zetten en via *Translate & Adapt* vertalen.
4. Controleren in preview, per markt, op mobiel en desktop. Daarna pas publiceren.

## Policies
`policies/` bevat de verzendpolicy (Pools en Engels) met algemene landen-zin en gratis verzending, plus back-ups (`*.original.*`).
