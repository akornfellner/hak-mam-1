# CLAUDE.md – Mathematik-Skript HAK/HAS Eferding

Mathematik-Skript für die 1. Klasse HAK. Welche Kapitel und Themen dazukommen, gibt
der Benutzer jeweils vor.

**Pflege:** Neue Regeln oder Vorgaben des Benutzers sofort hier eintragen.

## Allgemein

- Deutsch (Österreich), auch Kommentare, Dateinamen und Commit-Messages.
- Quarto-Buchprojekt, PDF mit **Typst** (nicht LaTeX).

## Ausgabeformate

| Format | Zweck | Inhalt |
|---|---|---|
| PDF (Typst), HTML | Skript | vollständig: Erklärungen, Formeln, Beispiele |
| revealjs | Folien | **nur** Formeln und Kernaussagen, **keine** Erklärtexte |

- Alles im selben Quelltext. Erklärtext (auch Einführungsbeispiele) steht in
  `::: {.content-hidden when-format="revealjs"}`. Formeln, Definitionen, Beispiele
  und Merksätze stehen ohne Bedingung. Nur für Folien:
  `::: {.content-visible when-format="revealjs"}`.

### Rendern

- Kurzbefehle im `justfile` (Übersicht: `just`): `just preview`, `just folien N`,
  `just render`, `just render-folien`, `just alles` usw. Neue häufige Befehle dort
  ergänzen und in README.md nachtragen.
- Skript: `quarto render` → `_book/`. Folien: `quarto render --profile folien` → `_folien/`.
- Ein Quarto-Buch kann keine revealjs-Folien erzeugen. Deshalb gibt es das Profil
  `_quarto-folien.yml` (Projekttyp `website`, nur `folien-*.qmd` und die
  Übersichtsseite). Folien-Einstellungen gehören dorthin, nicht in die Foliendateien.
- Übersichtsseite der Folien: `folien-uebersicht.qmd` → `_folien/index.html`
  (normales HTML, Aussehen in `_includes/folien-uebersicht.css`). Sie findet alle
  `NN-…/folien-N.qmd` selbst und zeigt Kapitelnummer und `title` aus deren
  YAML-Kopf. Bei neuen Kapiteln ist nichts zu ergänzen.
- Folien-Preview nur mit einer einzelnen Datei:
  `quarto preview 01-zahlen-und-mengen/folien-1.qmd --profile folien`.
- Folien-Logo: kommt aus `_brand.yml` und wird mit relativem Pfad
  (`../hak-logo.png`) eingebunden. Das klappt nur mit Projekttyp `website`; bei
  `default` schreibt Quarto `/hak-logo.png`, und das Logo fehlt unter
  `/hak-mam-1/folien/`. Den Projekttyp im Folien-Profil deshalb nicht ändern.
- Python: Projekt-venv `.venv/`, verwaltet mit **uv** (`pyproject.toml`, `uv.lock`,
  `.python-version` immer mitcommitten). `_environment` setzt
  `QUARTO_PYTHON=.venv/bin/python`, sonst nimmt Quarto einen fremden Kernel.
  - Einrichten / nach `git pull`: `uv sync`
  - Paket fürs Rendern: `uv add paket`, nur als Werkzeug am Rechner: `uv add --dev paket`
  - Nie `pip install` in die `.venv` (entfernt der nächste `uv sync`), nie
    `python3 -m venv` (auf dem Arbeitsrechner fehlt `ensurepip`).
- Neuer Rechner: `git clone …`, `uv sync`, `quarto render`.

### Veröffentlichung

- `.github/workflows/pages.yml`: bei jedem Push auf `main` Skript als HTML und
  Folien rendern (`uv sync --locked --no-dev`, `quarto render --to html`,
  `quarto render --profile folien`), `_folien/` nach `_book/folien/` kopieren und
  `_book/` per Actions-Artefakt auf GitHub Pages veröffentlichen. Kein PDF.
- Adressen: Skript <https://akornfellner.github.io/hak-mam-1/>, Folien
  <https://akornfellner.github.io/hak-mam-1/folien/>. Im Skript führt der Link
  „Folien“ in der Navigationsleiste (`book: navbar` in `_quarto.yml`) dorthin, er
  funktioniert nur online bzw. mit `just online`.
- Alle Verweise müssen relativ sein (kein führendes `/`), weil die Seite unter
  `/hak-mam-1/` liegt. Vor Änderungen an Workflow, Profil oder Verweisen mit
  `just online` testen: baut `_online/hak-mam-1/` wie der Workflow und liefert es
  unter <http://localhost:8000/hak-mam-1/> aus.
- Quarto- und uv-Version im Workflow = lokale Version (derzeit Quarto 1.10.18,
  uv 0.11.9). Bei einem Update beide anpassen.
- Actions-Versionen vor Änderungen online prüfen, z. B.
  `git ls-remote --tags https://github.com/actions/deploy-pages.git`.

### Folien-Aufteilung

- `slide-level: 4`: `#` bis `###` werden Titel-/Abschnittsfolien, jede `####`
  beginnt eine neue Folie.
- Zu volle Folie: Umbruch, der nur in den Folien wirkt (**nicht** `---`, das hält
  Quarto für YAML):
  ```markdown
  ::: {.content-visible when-format="revealjs"}
  * * *
  :::
  ```
- Pro Folie höchstens Definition + Formel + Abbildung, höchstens eine
  Zahlengerade. Beispiele bei Bedarf auf eine eigene Folie.

## Ordner- und Dateistruktur

```
_quarto.yml, _quarto-folien.yml, _brand.yml
_filters/, _includes/    Korrekturen für PDF und Mathe (siehe unten)
_shortcodes/buch.lua     Kurzbefehl {{< buch … >}} für Übungsbeispiele aus dem Buch
folien-uebersicht.qmd    Übersichtsseite der Folien (nur im Folien-Profil)
_python/grafiken.py      gemeinsame matplotlib-Funktionen
index.qmd                Startseite / Vorwort
NN-kapitelname/          ein Ordner pro Kapitel (01-, 02-, …)
  kapitel-N.qmd          "# Titel" + includes der Unterkapitel
  folien-N.qmd           nur Titel + dieselben includes
  _N-M-thema.qmd         Unterkapitel N.M, beginnt mit "## Titel"
  _zusammenfassung.qmd, _weitere-aufgaben.qmd, _wissens-check.qmd  ({.unnumbered})
  images/
```

- Niemals alles in eine Datei schreiben. In `_quarto.yml` nur `kapitel-N.qmd`
  eintragen, Unterkapitel per `{{< include _N-M-thema.qmd >}}` (sonst stimmt die
  Nummerierung 1.1, 1.2, … nicht). Unterkapitel-Dateien beginnen mit `_`.
- Überschriften: `#` Kapitel, `##` Unterkapitel, `###` Thema, `####` Teilthema.
  Nummeriert wird nur bis 1.1. Jede Überschrift bekommt eine ID `{#sec-…}`.
- Dateinamen: Kleinbuchstaben, Bindestriche, keine Umlaute/ß (ä→ae, ß→ss).

## Design

- Design nur in `_brand.yml`, keine Farben oder Schriften in `.qmd`-Dateien.
  Neue Farben, die im HTML sichtbar sind, mit `light`- und `dark`-Variante.
- Schulfarben: Rot `#CE1F2C`, reines Schwarz `#000000`. Schriften: Oswald
  (Überschriften), Lato (Text). Logo `hak-logo.png`, im dunklen HTML-Modus
  `hak-logo-dunkel.png`.
- HTML hat hell/dunkel (`cosmo`/`darkly`, jeweils `brand` zuletzt). PDF und Folien
  sind immer hell.

## Inhaltliche Bausteine

- **Jedes Thema beginnt mit einem Einführungsbeispiel** aus dem Alltag der
  Schülerinnen und Schüler: normaler Text `**Einführungsbeispiel:** …` in
  `content-hidden when-format="revealjs"`, kein Callout.
- Definitionen: `::: {.callout-note title="Definition: Titel"}`. `callout-note` ist
  **nur** für Definitionen.
- Beispiele: Absatz `**Beispiel:** …` (bei reiner Formel danach Leerzeile + `$$…$$`).
- Merksätze: `callout-important title="Merke"`, Tipps: `callout-tip title="Tipp: …"`.
- Nichts nummerieren außer Abbildungen: keine `#def-`/`#exm-`-Blöcke.
- Schreibweisen als Tabelle mit den Spalten „Schreibweise“ | „Sprechweise“.
- **Übungsbeispiele aus dem Schulbuch** mit dem Kurzbefehl `{{< buch 1.23 1.24ab 1.27 >}}`
  (eigene Zeile, Nummern mit Leerzeichen getrennt, keine Seitenzahlen). Ergibt einen
  Kasten „Übungsbeispiele: 1.23, 1.24ab, 1.27“ im Skript und auf den Folien.
  - Nummern gibt nur der Benutzer vor, nie selbst erfinden. Nennt er sie beim
    Einarbeiten eines Kapitels, den Kasten an die angegebene Stelle setzen (meist
    am Ende des passenden `###`- oder `####`-Abschnitts).
  - Aussehen: HTML/Folien in `_includes/buchbeispiele.css` (Farben per
    `var(--bs-primary)` bzw. `var(--brand-hak-rot)` aus `_brand.yml`), PDF in
    `buchbeispiele()` in `_includes/typst-anpassungen.typ`.

## Mathematik & Technik

- Formeln in LaTeX-Mathe-Syntax (`$…$`, `$$…$$`). Keine Roh-LaTeX-Blöcke, keine
  eigenen Makros, kein TikZ (geht mit Typst nicht).
- Dezimalkomma als `{,}`, Elemente in Mengen mit Dezimalzahlen durch Strichpunkt
  trennen: `$\{1{,}5;\ 2\}$`. Den Abstand nach dem Komma im PDF entfernt
  `_filters/dezimalkomma.lua`.
- Intervalle österreichisch: `$[2; 5]$`, `$]2; 5[$`, `$]-\infty; 5]$`. Einfach so
  schreiben, die Abstände korrigiert `_filters/intervallklammern.lua`.
- Deutsche Anführungszeichen „…“ direkt im Text.
- Buch-Titel/-Untertitel nicht mit „1.“ beginnen (Typst macht eine Aufzählung daraus).
- Korrekturen für die PDF-Vorlage „orange-book“ und Mathe stehen in
  `_includes/typst-anpassungen.typ` und `_filters/*.lua` (Zweck jeweils im
  Dateikopf). Neue Korrekturen dort ergänzen, nicht in den `.qmd`-Dateien.

### Grafiken

- **Grafiken mit Python/matplotlib, Code nie sichtbar** (global `echo: false`).
  Handgeschriebene SVG nur, wenn es mit matplotlib nicht sinnvoll geht.
- Pro Unterkapitel einmal eine Zelle mit `#| include: false` und
  `from _python.grafiken import *`. Wiederverwendbare Zeichnungen (z. B.
  `zahlengerade()`) in `_python/grafiken.py`, einmalige direkt in der Zelle.
- Jede Grafik-Zelle hat `#| label: fig-…` und `#| fig-cap: "…"`. Die letzte Zeile
  endet mit `;`, damit keine Textausgabe erscheint. Mathe in `fig-cap` mit doppeltem
  Backslash: `"$\\mathbb{R}$"`.
- Stil: Linien schwarz, Flächen hellrot `#EBA5AB` (hellere Abstufungen erlaubt),
  Markierungen Schulrot, Schrift sans-serif, weißer Hintergrund (lesbar im dunklen
  Modus), Zahlen mit Dezimalkomma und echtem Minus (`zahl()`).
