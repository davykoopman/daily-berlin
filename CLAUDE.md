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
- Stap 2 `python3 select_products.py --aantal 300` maakt per store `listings/<Store>_<datum>.xlsx`.
- Regels van de gebruiker: bron liefst NIET uit de eigen markt (zelfde foto+prijs = concurrentie);
  adviesprijs = prijs van de bronlink (niet onderprijzen, hoger is beter; alleen 'kan hoger' bij te lage prijs);
  foto's wegen zwaar (vooral de 1e); ~300 per store voor 20-25 dagen, koudere items later in de lijst.
