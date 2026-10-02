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
| `theme/snippets/pp-tier-progress.liquid` | Staffel-voortgangsbalk in Mix & match: leest het aantal producten in de winkelwagen en toont live "Dodaj jeszcze 1 produkt i oszczędź 10%" met een dunne balk in 3 stappen, zonder labels (eerlijke urgency). Instelling `2:10,3:15,4:20` gelijk aan de kortings-app |
| `theme/snippets/pp-tiers.liquid` | (Niet meer in gebruik) staffel als labels |
| `theme/snippets/pp-reveal.liquid` | Rustig verschijnen bij scrollen (iconenrij en stappen), uit bij "minder beweging" |
| `theme/sections/pp-bundle.liquid` | Mix & match: producten uit dezelfde menugroep als het product (Kobiety/Mężczyźni, uit het hoofdmenu), staffel-voortgangsbalk onder de kop, tegel "Bekijk hele collectie", kaart-hover op desktop |
| `theme/blocks/pp-delivery.liquid` | Levertijd onder de knop: "Verzonden binnen [x] werkdagen". Dagen per store gelijkzetten aan de verzendpolicy |
| `theme/sections/header-group.json` | Aankondigingsbalk: 3 wisselende berichten (gratis verzending, staffelkorting, retourdagen), om de 4 sec, op mobiel 1 regel. Teksten per store aanpassen aan de echte staffel en policy, vertalen via *Translate & Adapt* |
| `theme/sections/pp-trust.liquid` | Iconenrij met 4 garanties (verzending, retour + ruilen, veilig betalen, klantenservice met echte openingstijden, klikbaar naar e-mail). Instellingen: retourdagen, e-mail (leeg = store-e-mail), openingstijden en tijdzone (wordt in andere talen dan de hoofdtaal getoond, bv. "(CET)" op /gb). Teksten kort gehouden zodat alles op 1 regel past |
| `theme/sections/pp-steps.liquid` | "Zo werkt het" in 3 stappen (bestellen, thuis passen, niet goed = retour/ruilen). Instellingen: verzenddagen en retourdagen |
| `theme/sections/pp-collection-head.liquid` | Collectiepagina: compacte titel, staffel-voortgangsbalk en categorieknoppen uit het hoofdmenu (de subitems van de groep waar de collectie onder valt, met de menutitels, actieve knop zwart, op mobiel swipebaar). Bevat ook de CSS voor het productgrid: 4 kolommen desktop / 2 mobiel binnen paginabreedte, geen "W PROMOCJI"-labels, titel/prijs/kleuren altijd op 1 regel |
| `theme/sections/pp-home-categories.liquid` | Homepage: subcollecties uit het hoofdmenu als fototegels met een Kobiety/Mężczyźni-schakelaar (labels = menutitels, volgorde = menuvolgorde), één swipebare rij (6 per rij op desktop), laatste tegel linkt naar de hoofdcollectie. Foto = collectieafbeelding, of de eerste productfoto als de collectie er geen heeft |
| `theme/sections/pp-home-best.liquid` | Homepage: bestsellers (volgorde van de collectie, staat op Best verkocht) met dezelfde Kobiety/Mężczyźni-schakelaar, staffel-voortgangsbalk en dezelfde kaartjes als "Łącz i oszczędzaj" |
| `theme/snippets/pp-gender-tabs.liquid` | Groepsschakelaar voor de homepage: elke collectielink in het hoofdmenu met subitems wordt een knop. De keuze geldt voor alle secties op de pagina en wordt per bezoek onthouden |
| `theme/snippets/pp-card.liquid` | Licht productkaartje voor alle productlijsten (homepage-bestsellers, Mix & match, collectie- en zoekpagina): 1 foto (2e foto bij hover, pas geladen als de muis erop staat), kleurfoto's direct in het thema (geen app), titel/prijs/-X% op 1 regel, knop "Wybierz" altijd zichtbaar. ±7 KB per kaartje i.p.v. ±28 KB. Bevat ook de CSS van de scrollrij (swipen op mobiel, pijlen op desktop) |
| `theme/sections/main-collection.liquid`, `theme/sections/search-results.liquid` | Collectie- en zoekpagina gebruiken ook `pp-card` + `pp-quick-pick` (alleen de kaartregel is vervangen; filters, sorteren en pagina's zijn van het thema). Collectiepagina 1,42 MB → 0,94 MB |
| `theme/snippets/pp-quick-pick.liquid` | Eigen keuzevenster (kleur + maat) voor pp-card: opent direct zonder laden (productgegevens staan klein in de pagina), voegt toe via /cart/add.js waarna de Kaching-winkelwagen zelf opent (zonder winkelwagen-app: naar de winkelwagenpagina). Teksten uit de themavertalingen, dus elke taal |
| `theme/assets/quick-add.js` | Snel toevoegen (knopje op productkaarten): laadt alleen de productsectie in plaats van de hele productpagina (±145 KB i.p.v. ±900 KB; de sectie-id wordt per bezoek geleerd, dus werkt op elke store), begint al te laden bij hover (desktop) of aanraken (mobiel), deelt geladen producten tussen secties, knop pulseert tijdens laden, en gaat naar de productpagina als laden mislukt |
| `theme/snippets/quick-add-modal.liquid` | Snel-toevoegen-venster: de kleur/maat-kiezer van Swatch King wordt nu ook op desktop getoond (het thema verborg alles wat het niet kende) |
| `theme/snippets/pp-see-all-key.liquid` | Kiest de tekst van de tegel "Bekijk hele collectie" (dames/heren/neutraal) op basis van de groepscollectie, in elke taal |
| `theme/templates/index.json` | Homepage: banner → trust-punten → categorieën → bestsellers → O nas → FAQ (FAQ in lijn met de policies) |
| `theme/templates/collection.json` | Collectie-template: PP Collection heading + productgrid (kaarten zonder inspringing, 4:5 foto's) |
| `theme/templates/product.json` | Volgorde: titel → prijs → bullets → kleuren → maten → zwarte Add to cart → betaaliconen (automatisch, wat actief is) |
| `*.original.*` | Back-up van de bestanden vóór de wijziging |

Mix & match (`pp-bundle`): kop + staffel-voortgangsbalk, 4 kaarten desktop / 2 + swipen mobiel, -X% vakje, "W PROMOCJI"-label verborgen, titels max 2 regels, quick add ook op mobiel (CSS in `pp-benefits`, inclusief fix voor de Swatch King-kiezer in het quick add-venster). Volgorde: productinfo → Mix & match → iconenrij → O nas → Zo werkt het → FAQ. O nas op mobiel: lagere foto, tekst links.

Menu = enige bron: groepen en categorieën komen uit het hoofdmenu (`main-menu`, per sectie te wijzigen). Een collectielink op het hoogste niveau met subitems is een groep (Kobiety, Mężczyźni); de collectie-subitems zijn de categorieën. Nieuwe categorie = collectie aanmaken en als subitem onder de groep in het menu zetten; homepage, collectieknoppen, bestsellers en Mix & match volgen vanzelf. Lege collecties en een subitem dat naar de groep zelf linkt ("Zobacz wszystko") worden overgeslagen. Vertalingen (T-Lab) vertalen alleen de menutitels, de links blijven kloppen.

Foto's: carousel in 4:5 staand kader, begrensd op schermhoogte, bolletjes op mobiel en desktop.

## Op een nieuwe store zetten
1. Thema dupliceren, bovenstaande bestanden uploaden in de kopie.
2. In de template `return_days` gelijkzetten aan de refund policy van die store; staffel invullen. Hoofdmenu opbouwen als groep → subcollecties (zie boven); verder geen handles nodig.
   In *Theme settings* "Currency code" op productpagina's uit.
3. Teksten in de template (accordions/FAQ) in de hoofdtaal zetten en via *Translate & Adapt* vertalen.
4. Controleren in preview, per markt, op mobiel en desktop. Daarna pas publiceren.

## Policies
`policies/` bevat de verzendpolicy (Pools en Engels) met algemene landen-zin en gratis verzending, plus back-ups (`*.original.*`).
