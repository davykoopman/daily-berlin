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
