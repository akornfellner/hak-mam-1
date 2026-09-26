# CLAUDE.md – Mathematik-Skript HAK/HAS Eferding

Diese Datei gilt für alle Mathematik-Skripte (1.–5. Klasse HAK) und wird in jedes
Skript-Repository kopiert. Nur der Abschnitt **„Projektspezifisch“** am Ende
unterscheidet sich zwischen den Skripten.

**Pflege:** Sobald der Benutzer eine neue Regel oder Vorgabe nennt, wird sie hier
eingetragen. Diese Datei ist immer auf dem aktuellen Stand zu halten.

## Allgemein

- Sprache: Deutsch (Österreich). Auch Kommentare, Dateinamen und Commit-Messages
  auf Deutsch.
- Werkzeug: Quarto (Buch-Projekt). PDF wird mit **Typst** erzeugt, nicht mit LaTeX.

## Ausgabeformate

Jedes Skript wird in **drei Formaten** gerendert:

| Format | Zweck | Inhalt |
|---|---|---|
| PDF (Typst) | Skript zum Ausdrucken | vollständig: Erklärungen, Texte, Formeln, Beispiele |
| HTML | Skript online | vollständig: Erklärungen, Texte, Formeln, Beispiele |
| revealjs | Folien für den Unterricht | **nur** Formeln und Kernaussagen, **keine** Erklärtexte |

- Erklärungen und Fließtext stehen nur in PDF und HTML. Sie werden in die Folien
  nicht übernommen.
- Umsetzung mit Quarto-Bedingungen im selben Quelltext, nicht mit doppelten Dateien:
  ```markdown
  ::: {.content-hidden when-format="revealjs"}
  Erklärender Text, nur im Skript (PDF + HTML).
  :::
  ```
  Formeln, Definitionen, Beispiele und Merksätze stehen ohne Bedingung und erscheinen
  damit überall. Nur für Folien bestimmte Inhalte: `::: {.content-visible when-format="revealjs"}`.
- Einführungsbeispiele sind Erklärtext und kommen daher **nicht** in die Folien.

### Rendern

- Skript (HTML + PDF): `quarto render` → Ausgabe in `_book/`
- Folien: `quarto render --profile folien` → Ausgabe in `_folien/`
- Ein Quarto-Buch kann keine revealjs-Folien erzeugen. Deshalb gibt es das Profil
  `_quarto-folien.yml`, das auf ein normales Projekt umschaltet und nur die
  Foliendateien rendert. Folien-Einstellungen gehören in dieses Profil, nicht in die
  einzelnen Foliendateien.
- Das Folien-Logo hat einen absoluten Pfad (`/hak-logo.png`). Es erscheint daher nur,
  wenn die Folien über einen Webserver geöffnet werden, nicht beim Doppelklick auf die
  HTML-Datei.
- Folien-Preview immer mit einer einzelnen Datei:
  `quarto preview 01-zahlen-und-mengen/folien-1.qmd --profile folien`.
  `quarto preview --profile folien` allein funktioniert nicht (kein `index.qmd` im
  Folien-Profil).

### Veröffentlichung

- `.github/workflows/pages.yml` rendert bei jedem Push auf `main` nur das HTML
  (`quarto render --to html`) und veröffentlicht `_book/` auf GitHub Pages
  (Deployment über Actions-Artefakt, kein `gh-pages`-Branch).
- Quarto-Version im Workflow = lokale Version (derzeit 1.10.18). Bei einem
  Quarto-Update beide anpassen.
- Actions-Versionen vor Änderungen online prüfen (die Doku hinkt oft hinterher),
  z. B. mit `git ls-remote --tags https://github.com/actions/deploy-pages.git`.

### Folien-Aufteilung

- `slide-level: 4`: Überschriften `#` bis `###` werden Titel-/Abschnittsfolien (mit
  ihrem direkten Inhalt), jede `####`-Überschrift beginnt eine neue Folie.
- Wird eine Folie zu voll, einen Umbruch einfügen, der nur in den Folien wirkt:
  ```markdown
  ::: {.content-visible when-format="revealjs"}
  * * *
  :::
  ```
  Achtung: **nicht** `---` verwenden, das hält Quarto für einen YAML-Block.
- Faustregel: pro Folie höchstens Definition + Formel + Abbildung. Beispiele bei
  Bedarf auf eine eigene Folie.

## Ordner- und Dateistruktur

```
_quarto.yml              Projekt-Konfiguration (Buch: HTML + PDF)
_quarto-folien.yml       Profil für die Folien
_brand.yml               Design (Farben, Schriften, Logo)
_filters/                Lua-Filter (siehe „Mathematik & Technik“)
_includes/               Typst-Anpassungen für das PDF
index.qmd                Startseite / Vorwort
NN-kapitelname/          ein Ordner pro Hauptkapitel (01-, 02-, …)
  kapitel-N.qmd          Kapiteldatei: "# Titel" + includes der Unterkapitel
  folien-N.qmd           Folien: nur Titel + dieselben includes wie kapitel-N.qmd
  _N-M-thema.qmd         Unterkapitel N.M, beginnt mit "## Titel"
  _zusammenfassung.qmd   nicht nummeriert
  _weitere-aufgaben.qmd  nicht nummeriert
  _wissens-check.qmd     nicht nummeriert
  images/                Bilder dieses Kapitels
```

- Niemals alles in eine Datei schreiben.
- In `_quarto.yml` werden nur die Kapiteldateien (`kapitel-N.qmd`) eingetragen. Die
  Unterkapitel werden per `{{< include _N-M-thema.qmd >}}` eingebunden. So
  nummeriert Quarto korrekt 1.1, 1.2, … statt jede Datei als eigenes Kapitel zu zählen.
- Unterkapitel-Dateien beginnen mit `_`, damit Quarto sie nicht einzeln rendert.
- Überschriften-Ebenen: `#` Kapitel (1), `##` Unterkapitel (1.1), `###` Thema im
  Unterkapitel, `####` Teilthema. Nummeriert wird nur bis 1.1 (`number-depth: 2`).
- Jede Überschrift bekommt eine ID mit `sec-`, z. B. `### Teilmengen {#sec-teilmengen}`.
- Zusammenfassung, Weitere Aufgaben, Wissens-Check usw. bekommen `{.unnumbered}`.
- Dateinamen: Kleinbuchstaben, Bindestriche, keine Umlaute/ß (ä→ae, ö→oe, ü→ue, ß→ss).

## Design

- Das gesamte Design kommt aus `_brand.yml`. In `.qmd`-Dateien keine Farben oder
  Schriften hart codieren.
- Schulfarben: **Rot `#CE1F2C`** (aus dem Schullogo) und **Schwarz `#000000`**
  (reines Schwarz, kein „Fast-Schwarz“).
- Schriften: Oswald (Überschriften), Lato (Fließtext).
- Logo: `hak-logo.png` im Projektordner, dazu `hak-logo-dunkel.png` (weiße Buchstaben)
  für den dunklen HTML-Modus.
- HTML hat einen Umschalter hell/dunkel: `cosmo` (hell) und `darkly` (dunkel), jeweils
  mit `brand` als letztem Eintrag, damit `_brand.yml` Vorrang hat.
- Im dunklen Modus wird statt des Schulrots das hellere Rot `#F0616B` verwendet
  (Schulrot hätte auf `#222222` zu wenig Kontrast). PDF und Folien sind immer hell.
- Neue Farben in `_brand.yml` immer mit `light`- und `dark`-Variante anlegen, wenn sie
  im HTML sichtbar sind.

## Inhaltliche Bausteine

- **Jedes Thema beginnt mit einem Einführungsbeispiel** aus dem Alltag der
  Schülerinnen und Schüler, danach folgt die Mathematik. Kein Callout, sondern normaler
  Text mit fettem Label (wie bei Beispielen):
  ```markdown
  ::: {.content-hidden when-format="revealjs"}
  **Einführungsbeispiel:** …
  :::
  ```
- `callout-note` ist **ausschließlich** für Definitionen reserviert.
- Definitionen immer als Callout, **ohne Nummer**:
  ```markdown
  ::: {.callout-note title="Definition: Titel"}
  …
  :::
  ```
- Beispiele **ohne Nummer**, als normaler Absatz mit fettem Label:
  `**Beispiel:** Gegeben ist …` (bei reiner Formel: `**Beispiel:**`, dann Leerzeile
  und `$$…$$`). Keine `#def-`/`#exm-`-Blöcke verwenden, die nummeriert Quarto immer.
- Merksätze: `::: {.callout-important title="Merke"}`
- Tipps: `::: {.callout-tip title="Tipp: …"}`
- Abbildungen mit ID und Beschriftung: `![Beschriftung](images/datei.svg){#fig-name width="45%"}`
- Schreibweisen mit Sprechweise als Tabelle (Spalten „Schreibweise“ | „Sprechweise“).

## Mathematik & Technik

- Formeln in LaTeX-Mathe-Syntax (`$...$`, `$$...$$`). Quarto übersetzt sie für Typst.
- Keine Roh-LaTeX-Blöcke, keine eigenen LaTeX-Makros, kein TikZ (funktioniert mit
  Typst nicht). Grafiken als Bilder oder mit R/Python-Plots erzeugen.
- Einfache Grafiken (z. B. Venn-Diagramme) als handgeschriebene SVG in `images/`:
  Linien schwarz `#000000`, Flächen hellrot `#EBA5AB`, Schrift `sans-serif`.
- Mengen mit Dezimalzahlen: Elemente mit Strichpunkt trennen, Dezimalkomma als `{,}`
  schreiben, z. B. `$\{1{,}5;\ 2\}$`.
- Deutsche Anführungszeichen „…“ direkt im Text verwenden.
- Die PDF-Vorlage „orange-book“ ignoriert einige Einstellungen. Korrekturen dafür:
  - `_includes/typst-anpassungen.typ`: Schrift Lato, kein Absatzeinzug, keine Formelnummern
  - `_filters/pdf-nummerierung.lua`: im PDF nur bis 1.1 nummerieren
  - `_filters/deutsche-anfuehrungszeichen.lua`: korrekte „…“ im PDF
- Buch-Metadaten (Titel, Untertitel) dürfen nicht mit „1.“ beginnen, sonst macht
  Typst daraus eine Aufzählung.

## Projektspezifisch: hak-mam-1 (1. Klasse)

1. Zahlen und Mengen (`01-zahlen-und-mengen/`)
   1.1 Die Zahlenmengen · 1.2 Rechnen mit Zahlen · 1.3 Umrechnen von Maßeinheiten ·
   1.4 Zahlenangabe in Prozent und Promille · Zusammenfassung · Weitere Aufgaben ·
   Wissens-Check
2. Terme und Variablen (`02-terme-und-variablen/`)
   2.1 Grundbegriffe · 2.2 Addition, Subtraktion und Multiplikation von Termen ·
   2.3 Potenzterme · 2.4 Das Potenzieren eines Binoms · 2.5 Faktorisieren ·
   2.6 Bruchterme · Zusammenfassung · Vermischte Aufgaben · Weitere Aufgaben zum
   Üben von Textverständnis und Modellbilden · Wissens-Check
3. Gleichungen und Formelumwandlungen (`03-gleichungen-und-formelumwandlungen/`)
   3.1 Grundbegriffe zu den Gleichungen · 3.2 Das Lösen von linearen Gleichungen ohne
   Rechengerät · 3.3 Lineare Gleichungen mit Bruchzahlen · 3.4 Bruchgleichungen ·
   3.5 Verhältnisse und Proportionen · 3.6 Umformen von Formeln · 3.7 Vermischte
   Aufgaben aus Wirtschaft und Geldwesen · 3.8 Mischungsaufgaben und
   Prozentrechnung · Zusammenfassung · Weitere anwendungsorientierte Aufgaben zur
   Wiederholung · Wissens-Check
4. Funktionen (`04-funktionen/`)
   4.1 Definition und Darstellung der Funktion · 4.2 Die Gleichung der linearen
   Funktion · 4.3 Einige Anwendungen der Funktion · 4.4 Stückweise lineare
   Funktionen · 4.5 Die Nullstelle der linearen Funktion · 4.6 Beziehung von zwei
   Funktionen · 4.7 Indirekt proportionaler Zusammenhang
