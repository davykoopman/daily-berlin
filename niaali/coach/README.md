# Niaali – coachpunten (16 nov 2026)

## 2. Gender + age group (UK-feed) — UITGEVOERD (GO gebruiker)
- Namespace `mm-google-shopping` (gelezen door Google & YouTube-app), type single_line_text_field.
- `gender` gezet op alle 1150 actieve producten: Mens → male, Womens → female,
  Prezent (7) + unisex ski-jas 16314004275532 → unisex, Kids-jas 16228549230924 → unisex.
- `age_group` gezet waar leeg (844): adult; Kids-jas → kids. Bestaande 306 waarden (adult) ongemoeid.
- Controle: alle 1150 opnieuw opgehaald, 0 afwijkingen (feed/verify.json).
- Bestanden: feed/prods.json (uitgangssituatie), feed/mf_all.json (alle 1994 writes), feed/q*.gql (batches).
- Terugdraaien: metafieldsDelete op mm-google-shopping.gender (+ age_group voor de 844 uit mf_all.json).

## 3. Uitverkochte varianten — WACHT OP GO
- 206 varianten (DENY, voorraad 0) in 47 actieve producten (soldout.json).
- 21 van 47 producten hadden verkoop in 90 dagen (samen ± 13.056 zł), 26 geen verkoop.

## 4. Zomerjurken — AL OP CONCEPT
- Tags: SS = lente/zomer, AW = herfst/winter, AS = vermoedelijk all-season.
- Alle 5 SS-jurken zijn al draft. De 11 actieve jurken zijn AW/AS, 0 verkopen in 90 dagen.

## 3. Uitverkochte varianten — UITGEVOERD (GO: rand verwijderen, midden laten)
- Regel: per kleur; uitverkochte maat aan begin/eind van de maatreeks → verwijderd; met leverbare maten aan beide kanten → blijft als uitverkocht.
- 172 varianten verwijderd in 27 producten (sizes/plan.json "delete"; volledige backup sizes/prods.json).
  19 kleuren waren in alle maten uitverkocht en zijn daardoor verdwenen (zie plan.json "fullcolor").
- 34 middenmaten blijven uitverkocht → sizes/middenmaten_uitsluiten.csv (voor uitsluiten in campagnes).
- Controle: na afloop staan precies deze 34 nog op voorraad 0 (DENY) in de winkel.

## 1. NL-winkelwagen — KLAAR IN THEMAKOPIE (gebruiker publiceert)
- Nieuw thema "Black Friday v4 (totaal NL)" #210865717580 = kopie van live v2 (#209403576652) + alleen snippets/cart-summary.liquid uit v3.
- "Verwacht totaal" → "Totaal" (PL: "Suma", UK: "Total"); regel "Gratis verzending inbegrepen." (tax-info) verwijderd.
- Gecontroleerd in preview /nl-nl/cart (desktop + mobiel): "Totaal €… EUR", geen verzendregel. Overige bestanden identiek aan live.
- Op verzoek: "Totaal" even groot en vet als het bedrag; beloftes (gratis verzending · 60 dagen retour · veilig betalen) als tekst zonder icoontjes.
