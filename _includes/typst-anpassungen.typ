// Anpassungen der Buchvorlage "orange-book" für das PDF
// (wird nach book.with() eingebunden und überschreibt deren Einstellungen)

// Fließtextschrift aus _brand.yml (orange-book übernimmt sie nicht automatisch)
#set text(font: "Lato")

// Kein Einzug in der ersten Zeile, dafür Abstand zwischen Absätzen
#set par(first-line-indent: 0em, spacing: 1em)

// Formeln nicht nummerieren
#set math.equation(numbering: none)
