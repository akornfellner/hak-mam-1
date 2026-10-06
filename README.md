# hak-mam-1

Mathematik-Skript für die **1. Klasse HAK** an der HAK/HAS Eferding, erstellt mit
[Quarto](https://quarto.org).

Design, Filter, Formate und Befehle teilt sich dieses Skript mit den Skripten
der anderen Klassen. Sie kommen aus der Extension
[hak-quarto](https://github.com/akornfellner/hak-quarto). **Dort steht die
ausführliche Anleitung:** wo was liegt, wo man was ändert, wie man die Extension
aktualisiert und wie man eine neue Klasse anlegt.

## Inhalt

1. Zahlen und Mengen
2. Terme und Variablen
3. Gleichungen und Formelumwandlungen
4. Funktionen

## Ausgabeformate

| Format | Verwendung |
|---|---|
| PDF (Typst) | Skript zum Ausdrucken, vollständig |
| HTML | Skript online, vollständig |
| revealjs | Folien für den Unterricht, nur Formeln und Kernaussagen |

Alle drei Formate entstehen aus denselben Quelldateien. Erklärtexte werden in den
Folien automatisch ausgeblendet.

## Projektstruktur

```
_quarto.yml            Titel, Klasse, Kapitelliste
_quarto-folien.yml     Profil für die Folien, Untertitel der Folien
_extensions/hak/       Kopie der Extension hak-quarto (nie direkt bearbeiten)
index.qmd              Startseite
folien-uebersicht.qmd  Übersichtsseite der Folien (alle Kapitel)
01-…/ – 04-…/          ein Ordner pro Kapitel, darin eine Datei pro Unterkapitel
_python/grafiken.py    Zeichnungen dieser Klasse
justfile               Kurzbefehle (just render, just folien 1, …)
CLAUDE.md              Regeln und Konventionen für dieses Skript
```

## Voraussetzungen

- [Quarto](https://quarto.org/docs/get-started/) ≥ 1.10 (Typst ist enthalten)
- [uv](https://docs.astral.sh/uv/) für die Python-Umgebung
- [just](https://just.systems) ≥ 1.19 für die Kurzbefehle
- Internetverbindung beim ersten Rendern (Schriften Oswald und Lato werden geladen)

## Rendern

Die wichtigsten Befehle (Übersicht mit `just`):

```bash
just sync            # Python-Umgebung einrichten (einmalig / nach git pull)

just preview         # Skript mit Live-Vorschau (HTML)
just preview-pdf     # Skript mit Live-Vorschau (PDF)
just folien 1        # Folien von Kapitel 1 mit Live-Vorschau

just render          # Skript als HTML und PDF → _book/
just pdf             # nur das PDF
just render-folien   # alle Folien → _folien/
just alles           # Skript und Folien
just online          # Online-Version lokal testen: http://localhost:8000/hak-mam-1/
just aufraeumen      # _book/, _folien/, _online/ und .quarto/ löschen

just extension       # Extension von GitHub aktualisieren
just extension-lokal # Extension aus ../hak-quarto übernehmen (zum Testen)
```

Ohne just:

```bash
uv sync
quarto render                    # Skript als HTML und PDF → _book/
quarto render --profile folien   # Folien → _folien/
quarto preview --render hak-html # Skript mit Live-Vorschau

# Folien mit Live-Vorschau (immer eine einzelne Foliendatei angeben)
quarto preview 01-zahlen-und-mengen/folien-1.qmd --profile folien
```

Nicht `quarto render --to html` verwenden: Das rendert ohne Extension. Das
HTML-Format heißt hier `hak-html`.

## Online-Version

Bei jedem Push auf `main` rendert GitHub Actions das Skript als HTML und die
Folien und veröffentlicht beides auf GitHub Pages:

- Skript: <https://akornfellner.github.io/hak-mam-1/>
- Folien: <https://akornfellner.github.io/hak-mam-1/folien/> (Übersicht aller
  Kapitel, ein Klick öffnet die Folien; im Skript oben rechts unter „Folien“)

Für die Folien im Unterricht reicht damit ein Browser. Neue Kapitel erscheinen
auf der Übersichtsseite von selbst. Vor dem Push lässt sich die Online-Version
mit `just online` lokal prüfen.

Der Ablauf steht im gemeinsamen Workflow in `hak-quarto` und wird nur dort
geändert. Einmalig nötig: *Settings → Pages → Build and deployment → Source:
„GitHub Actions“*.

## Lizenz

[MIT](LICENSE) © 2026 Alexander Kornfellner
