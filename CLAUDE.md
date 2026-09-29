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
