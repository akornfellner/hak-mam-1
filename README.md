# hak-mam-1

Mathematik-Skript für die **1. Klasse HAK** an der HAK/HAS Eferding, erstellt mit
[Quarto](https://quarto.org).

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
_quarto.yml         Projekt-Konfiguration (Skript: HTML + PDF)
_quarto-folien.yml  Profil für die Folien
_brand.yml          Design: Schulfarben, Schriften, Logo
_filters/           Lua-Filter (Nummerierung, Anführungszeichen)
_includes/          Typst-Anpassungen für das PDF
index.qmd           Startseite
01-…/ – 04-…/       ein Ordner pro Kapitel, darin eine Datei pro Unterkapitel
justfile            Kurzbefehle (just render, just folien 1, …)
CLAUDE.md           Regeln und Konventionen für dieses Skript
```

## Voraussetzungen

- [Quarto](https://quarto.org/docs/get-started/) ≥ 1.10 (Typst ist enthalten)
- [uv](https://docs.astral.sh/uv/) für die Python-Umgebung
- [just](https://just.systems) für die Kurzbefehle (optional)
- Internetverbindung beim ersten Rendern (Schriften Oswald und Lato werden geladen)

## Rendern

Die wichtigsten Befehle stehen im `justfile` (Übersicht mit `just`):

```bash
just sync            # Python-Umgebung einrichten (einmalig / nach git pull)

just preview         # Skript mit Live-Vorschau (HTML)
just preview-pdf     # Skript mit Live-Vorschau (PDF)
just folien 1        # Folien von Kapitel 1 mit Live-Vorschau

just render          # Skript als HTML und PDF → _book/
just pdf             # nur das PDF
just render-folien   # alle Folien → _folien/
just alles           # Skript und Folien
just aufraeumen      # _book/, _folien/ und .quarto/ löschen
```

Ohne just:

```bash
uv sync
quarto render                    # Skript als HTML und PDF → _book/
quarto render --profile folien   # Folien → _folien/
quarto preview                   # Skript mit Live-Vorschau

# Folien mit Live-Vorschau (immer eine einzelne Foliendatei angeben)
quarto preview 01-zahlen-und-mengen/folien-1.qmd --profile folien
```

Die Folien am besten über den Preview öffnen. Beim direkten Öffnen der HTML-Datei
fehlt sonst das Logo.

## Online-Version

Bei jedem Push auf `main` rendert GitHub Actions das Skript als HTML und
veröffentlicht es auf GitHub Pages:
<https://akornfellner.github.io/hak-mam-1/>

Einmalig nötig: *Settings → Pages → Build and deployment → Source: „GitHub Actions“*.

## Lizenz

[MIT](LICENSE) © 2026 Alexander Kornfellner
