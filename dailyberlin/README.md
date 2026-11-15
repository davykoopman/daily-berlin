# Daily Berlin (dailyberlin.de) – addresses, company number, return address (2026-10-13)

Live theme "Daily Berlin" (Impulse 5.2.1, 196738941277). Locales: de (primary), fr. Markets DE, AT, FR, LI.
Policies are Shopify policies (Settings → Policies); the app has no write_legal_policies → user pastes.

Company block (as supplied by the user):
- Daily Berlin, Firmensitz (NL): Merseloseweg 62A, 5801 CE Venray, Niederlande
- Lager Deutschland: Jänickestraße 40, 14167 Berlin (Steglitz-Zehlendorf), Deutschland
- Firmennummer: 61429573861
Return address: Liu Changxing, Freight Elevator 2, 3rd Floor, Building D, Aidema E-Commerce Park,
No. 409 Suxi Avenue, Suxi Town, 322000 Yiwu, Zhejiang, China

Done by Claude:
- Page "Widerrufsformular": return address added under "Rücksendung der Ware" (pages/widerrufsformular.orig.html → .html).
- Duplicated theme "Daily Berlin - footer adressen (werk)" (210852741469) – not used, footer is pasted by the user
  (footer settings live in the 19 KB settings_data.json; rewriting it for one text block was too risky).

To paste by the user (policies/ = new, policies-orig/ = before):
- contact-information, privacy-policy, terms-of-service: company block replaces the old address lines;
  terms §20 + refund policy: new "Rücksendeadresse" with the China address; refund + shipping: company block at the end.
- legal-notice.html: Impressum, only if the user wants it (did not exist).
- Footer "Unsere Informationen" block: text in footer.txt. French (fr) translations via T-Lab afterwards.

## Check 2026-10-13 (after user pasted)
- DE live: all 6 policies match policies/*.html word for word; footer block updated; Widerrufsformular has the return address.
- Open: /pages/kontakt still shows the old address (not in scope); French (fr-fr) footer, policies and legal notice are
  still the old translations (old address, no company number; FR legal notice still says "Représenté par: Davy Koopman");
  work theme "Daily Berlin - footer adressen (werk)" still exists.
- Recheck: FR footer, Widerrufsformular, refund, terms, contact, shipping OK. Still open: FR privacy policy and FR legal notice
  (old address, "Représenté par: Davy Koopman"), Kontakt page DE+FR old address, work theme not deleted.

## Impulse DMCA → Horizon (15 Nov 2026)
Shopify flagged "Daily Berlin" (Impulse 5.2.1, no Theme Store license) as an unlicensed copy; store suspension
on 16 Nov 15:33 UTC unless removed. All 3 Impulse themes (Daily Berlin, footer adressen (werk), Kopie van
204232-…) are the same unlicensed Impulse. The user chose not to buy Impulse (500 USD).
- Work theme "Daily Berlin Horizon (werk)" (211837288797) = duplicate of the licensed Horizon (themeStoreId 2481).
- Only Daily Berlin's own content was carried over (texts, images, menus, settings values), NO Impulse code:
  impulse-content/ = the content JSON read from the Impulse theme; horizon/ = generated Horizon JSON
  (build.py, hf.py, prod.py); horizon-orig/ = Horizon files before changes.
- Global: logo/favicon, Alegreya Sans, uppercase headings, square corners, wide page, scheme-5 = #0f0f0f.
- Header: announcement (free shipping DE/AT/FR/LI), logo centered, menu "Informationen" (main-menu-1) below.
- Home: hero (Daily_Berlin_Banner1) + Damen/Herren buttons, 3 benefits, collections Damen/Herren, Über uns, FAQ.
- Product: title, price, variants, Kiwi size chart app block, buy buttons, 3 benefits, payment icons (enabled
  methods only), description, accordion Lieferinformationen/Rückgabe, recommendations, Über uns.
- Footer: Unsere Informationen, menus Informationen + Rechtliche Hinweise, newsletter, Instagram.
- Page template "about" for /pages/uber-uns. Other pages use Horizon's page / contact templates.
Next for the owner: publish the Horizon theme, then delete the 3 Impulse themes before the deadline.
