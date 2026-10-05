// Power Query (M): leest alle Daily Profit Sheets uit één map en plakt de maandtabs onder elkaar.
// Gebruik: Gegevens ophalen > Lege query > Geavanceerde editor > plak dit.
// Stel eerst de parameter MapPad in (zie README-stappen in de chat).
let
    Bron      = Folder.Files(MapPad),
    Xlsx      = Table.SelectRows(Bron, each [Extension] = ".xlsx" and not Text.StartsWith([Name], "~$")),

    // Storenaam = tekst na de laatste " - " in de bestandsnaam, zonder ".xlsx"
    MetStore  = Table.AddColumn(Xlsx, "Store", each
                    Text.BeforeDelimiter(
                        Text.AfterDelimiter([Name], " - ", {0, RelativePosition.FromEnd}),
                        ".", {0, RelativePosition.FromEnd}), type text),

    Tabs      = Table.AddColumn(MetStore, "Tabs", each Excel.Workbook([Content], true)),
    Klein     = Table.SelectColumns(Tabs, {"Store", "Tabs"}),
    Uitgeklapt= Table.ExpandTableColumn(Klein, "Tabs", {"Name", "Kind", "Data"}, {"Tab", "Kind", "Data"}),

    // Alleen maandtabs: 3-letter maand + 2 cijfers (Aug26, Sep26, Okt26, ...)
    Maanden   = {"Jan","Feb","Mrt","Apr","Mei","Jun","Jul","Aug","Sep","Okt","Nov","Dec"},
    Maandtabs = Table.SelectRows(Uitgeklapt, each
                    [Kind] = "Sheet"
                    and Text.Length([Tab]) = 5
                    and List.Contains(Maanden, Text.Start([Tab], 3))
                    and (try Number.FromText(Text.End([Tab], 2)) otherwise null) <> null),

    Kolommen  = {"Datum","Omzet","Cost of Goods","Adspend Google","Media Buyer","Team Kosten","Refunds","Subscriptions","Transactie","Profit"},
    Gekozen   = Table.TransformColumns(Maandtabs, {{"Data", each Table.SelectColumns(_, Kolommen, MissingField.UseNull)}}),
    Plat      = Table.ExpandTableColumn(Gekozen, "Data", Kolommen),

    // Totaalrij heeft tekst ("SEP") in Datum en valt hier weg
    Datums    = Table.TransformColumns(Plat, {{"Datum", each if Value.Is(_, type datetime) then DateTime.Date(_) else null, type date}}),
    ZonderTot = Table.SelectRows(Datums, each [Datum] <> null),

    // Toekomstige dagen (alles 0) weglaten
    Tot_Vandaag = Table.SelectRows(ZonderTot, each [Datum] <= Date.From(DateTime.LocalNow())),

    Getypt    = Table.TransformColumnTypes(Tot_Vandaag, List.Transform(List.Skip(Kolommen), each {_, type number})),
    Uitkomst  = Table.RemoveColumns(Getypt, {"Tab", "Kind"})
in
    Uitkomst

// ---- DAX-metingen voor Power BI (Nieuwe meting), tabel heet hier AlleStores ----
// Omzet          = SUM(AlleStores[Omzet])
// Adspend        = SUM(AlleStores[Adspend Google])
// Winst          = SUM(AlleStores[Profit])
// Profit %       = DIVIDE([Winst], [Omzet])
// ROAS           = DIVIDE([Omzet], [Adspend])
// Break-even ROAS =
//     VAR Kosten = SUM(AlleStores[Cost of Goods]) + SUM(AlleStores[Media Buyer]) + SUM(AlleStores[Team Kosten])
//                + SUM(AlleStores[Refunds]) + SUM(AlleStores[Subscriptions]) + SUM(AlleStores[Transactie])
//     RETURN DIVIDE([Omzet], [Omzet] - Kosten)
