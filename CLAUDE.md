# CLAUDE.md

## Competitor research (competitor-research/)

Werkwijze en criteria: `competitor-research/HOOFDPROMPT.md`.

### Competitor sheet (Excel)
- **Bron van waarheid:** `competitor-research/data/competitors.csv` (één rij per domein) en
  `competitor-research/data/bestsellers.csv`. Bewerk nooit alleen de .xlsx.
- **Nieuwe of bijgewerkte competitors:** pas de rij in `competitors.csv` aan op basis van het
  domein (niet dupliceren). Bij een bestaand domein: werk bezoekers/trend/paid/top landen bij,
  zet `Laatst gecheckt` op vandaag en laat `Eerst gevonden` en `Producten gekopieerd` staan.
  Getallen: bezoekers als geheel getal, trend en paid search als fractie (0.25 = 25%).
- **Sheet bouwen:**
  ```bash
  cd competitor-research && python3 build_excel.py
  python3 <xlsx-skill-dir>/scripts/recalc.py Competitor_Research.xlsx 120
  ```
  Let op: recalc.py slaat het bestand opnieuw op via LibreOffice. Bij de Launch File draai je recalc daarom ALLEEN op een
  kopie (in de scratchpad), anders gaan statuskleuren/opmaak verloren.
  (openpyxl en `libreoffice-calc` zijn nodig; installeer ze als ze ontbreken.)
- **Wanneer de gebruiker om de sheet vraagt** ("stuur de competitor sheet", "stuur de excel",
  e.d.): bouw de sheet opnieuw vanuit de CSV's, controleer dat recalc `total_errors: 0` geeft,
  commit + push, en stuur `competitor-research/Competitor_Research.xlsx` met SendUserFile
  (display: attach).
- Na elke research-ronde: resultaten eerst in de CSV's zetten, dan de sheet bouwen en meesturen.

### Listinglijsten per eigen store
- Eigen stores en markten: `competitor-research/config/stores.json`; seizoenen: `config/seasons.json`.
- Stap 1 `python3 pool.py --extra <domein:MARKT ...>` haalt alle competitors op (≥25K bezoekers + extra's),
  vergelijkt foto's en groepeert hetzelfde product over stores (`.cache/pool.json`).
- Stap 2 `python3 select_products.py --aantal 200` maakt `listings/Launch File Davy Koopman.xlsx` (ENGELS):
  'Strategy & explanation' + per store een producttab en een '<Store> – Links'-tab met Lister (Dhafnie/Fatima/Davy),
  Status (Not listed/Draft/Live/Issues/Duplicate) en Comment. De lijst staat ook in `listings/launch_state.json` (altijd committen).
- **Teruggestuurde Launch File** (van de gebruiker): sla hem op en draai
  `python3 select_products.py --aantal 300 --merge <pad>`: Lister/Status/Comment blijven behouden (per store + link),
  bestaande regels blijven staan en elke store wordt aangevuld tot 300 'Not listed'. Nieuwe regels krijgen 'Added on' = vandaag.
  Draai NOOIT zonder --merge als er al een Launch File in gebruik is (dan gaan statussen verloren).
  Stuur daarna het bestand terug met SendUserFile (display: attach).
- Bronlinks ALLEEN van competitors met ≥75K bezoekers/mnd volgens SimilarWeb (sinds sept toont SW alleen nog het
  cijfer in het vergelijkingsblok; akkoord Davy 9-10), ≥60% paid search (Leon Boutique 59% bewust binnen), match ≥4,
  geen eigen label. Dalers blijven bron (kleine correctie ±5% op score). Controleer na elke run dat er 0 bronnen buiten de regel zijn.
- Bron die in het eigen land van de store adverteert: alleen bij sterke trend + volledige match; adviesprijs dan
  iets onder de bron, maximaal €5 / 5% lager.
- **Wekelijkse cyclus** (max 200 open per store): (1) teruggestuurde file → `python3 clean_returned.py <file> --autocheck`
  (statussen Not listed/Draft/Live/Issues/Duplicate, Listed=Live, ontbrekende lister bij status = Dhafnie,
  'Already in store' = Duplicate); (2) SimilarWeb-check bronnen + nieuwe competitors (Tranco-nieuwkomers);
  (3) `pool.py --extra …`; (4) `season_report.py` en `config/seasons.json` bijstellen; (5) eerst met Davy bespreken;
  (6) `python3 select_products.py --update --aantal 200`; (7) `python3 photo_upgrade.py` (beste fotoversie van
  hetzelfde product: conversie 55% + fotokwaliteit 45%, prijs blijft van de bewezen ≥75K-bron) en `python3 quality_gate.py`
  (dode link = alleen echte 404, <3 foto's, merknaam → Issues); herhaal 6-7 tot elke store 200 open heeft;
  (8) controleren, committen, file sturen. Geen nieuwe kolommen in de files.
- Regels van de gebruiker: bron liefst NIET uit de eigen markt (zelfde foto+prijs = concurrentie);
  adviesprijs = prijs van de bronlink (niet onderprijzen, hoger is beter; alleen 'kan hoger' bij te lage prijs);
  foto's wegen zwaar (vooral de 1e); ~300 per store voor 20-25 dagen, koudere items later in de lijst.
