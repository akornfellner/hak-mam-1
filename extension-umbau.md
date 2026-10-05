Ich möchte die Technik meines Skripts in eine eigene Quarto-Extension auslagern,
damit ich später für jede Klasse ein eigenes Skript-Repo habe (eigene GitHub
Pages-Seite pro Klasse), Design, Filter, Regeln und Befehle aber nur an einer
Stelle pflege.

Ausgangslage:
- Wir sind in `~/Dokumente/Skript/hak-mam-1` (Skript 1. Klasse, läuft fehlerfrei).
- Die Folien sind bereits auf GitHub Pages veröffentlicht (Übersichtsseite
  unter `/hak-mam-1/folien/`, siehe CLAUDE.md und Workflow). Das muss nach dem
  Umbau unverändert funktionieren, ich brauche die Folien im Unterricht.
- Rückfallpunkt: Der Stand **jetzt, vor dem Umbau** (mit Folien online), nicht
  der ältere Commit `a4078e3` (dort gibt es die Folien online noch nicht).
  Prüfe als Erstes, dass der Arbeitsordner sauber und alles gepusht ist, und
  setze dann nach Rückfrage das Tag `vor-extension-umbau` auf den aktuellen
  Commit (auch pushen). Nenne mir die Commit-Nummer.
  Zurück geht es später mit `git revert --no-commit vor-extension-umbau..HEAD`,
  danach committen und pushen. Kein `git reset --hard`, kein force push.
- Daneben liegt `~/Dokumente/Skript/quarto-hak`: ein leeres, öffentliches
  GitHub-Repo (`akornfellner/quarto-hak`), bereits per SSH geklont.
- Prüfe zuerst, ob du auf `../quarto-hak` zugreifen kannst. Falls nicht, sag
  mir, dass ich `/add-dir ../quarto-hak` ausführen soll.

## Zielstruktur

```
~/Dokumente/Skript/
  quarto-hak/        Extension-Repo (Technik für alle Klassen)
  hak-mam-1/         Skript 1. Klasse
  hak-mam-2/ …       später, durch Klonen + Checkliste
```

`quarto-hak` (alles, was alle Klassen gemeinsam haben):

```
quarto-hak/
  README.md                 Zweck, Installation, Update, Checkliste
                            „Neue Klasse anlegen“
  CLAUDE.md                 Regeln für die Arbeit am Extension-Repo selbst
  _extensions/hak/
    _extension.yml          Formate hak-html, hak-typst, hak-revealjs mit allen
                            heutigen Einstellungen, Filtern, Kurzbefehlen
    _brand.yml, hak-logo.png, hak-logo-dunkel.png
    filters/                dezimalkomma, intervallklammern,
                            deutsche-anfuehrungszeichen, pdf-nummerierung
    buch.lua                Kurzbefehl {{< buch … >}}
    buchbeispiele.css, typst-anpassungen.typ
    stil.py                 Farben, rcParams, zahl(), tausender()
    regeln.md               allgemeine Regeln (Großteil der heutigen CLAUDE.md)
    hak.just                gemeinsame just-Befehle
```

`hak-mam-1` (nur was zur Klasse gehört):

```
hak-mam-1/
  _extensions/hak/          Kopie der Extension, mitcommittet, nie direkt bearbeiten
  _quarto.yml               Titel, Untertitel, Kapitelliste, format: hak-html / hak-typst
  _quarto-folien.yml        kurz, format: hak-revealjs
  _python/grafiken.py       importiert stil.py, dazu nur die Zeichnungen dieser
                            Klasse (zahlengerade, primfaktoren, primfaktor_treppe)
  CLAUDE.md                 kurz: 1. Klasse, Import @_extensions/hak/regeln.md,
                            Hinweis „Allgemeines nur in ../quarto-hak ändern“
  justfile                  import '_extensions/hak/hak.just' (+ Klassenbefehle)
  .claude/settings.json     ../quarto-hak als zusätzlicher Ordner (additionalDirectories)
  .github/workflows/pages.yml, pyproject.toml, uv.lock, .python-version,
  _environment, README.md, index.qmd, 01-…/
```

Bewusst pro Skript bleiben: Workflow, `pyproject.toml`/`uv.lock`,
`_environment`, `grafiken.py` mit den Zeichnungen der Klasse. Kein Quarto-
Template: neue Klassen entstehen durch Klonen des neuesten Skripts und die
Checkliste im README von `quarto-hak`.

## Abläufe, die danach funktionieren sollen (in regeln.md / CLAUDE.md festhalten)

- **Allgemeine Änderung beim Arbeiten an einer Klasse:** Claude ändert die
  Datei in `../quarto-hak` (nie in `_extensions/` des Skripts), testet mit
  `quarto add ../quarto-hak` im aktuellen Skript, committet in beiden Repos und
  pusht `quarto-hak` erst nach Rückfrage.
- **Andere Klassen aktualisieren:** just-Befehl (z. B. `just extension`), der
  die Extension von GitHub holt (`akornfellner/quarto-hak`), ohne Rückfragen;
  danach rendern und committen. Funktioniert auch ohne lokalen
  `quarto-hak`-Ordner.
- **Neue Klasse:** Checkliste im README von `quarto-hak` (neue Git-Historie bzw.
  „Use this template“, Kapitel löschen, `grafiken.py` auf den Stil-Import
  reduzieren, Titel/Klasse in `_quarto.yml`, `folien-N.qmd`, CLAUDE.md, README,
  `pyproject.toml` anpassen, `index.qmd`, `uv sync`, Pages einschalten).
- **Neue Regeln:** allgemeine in `quarto-hak/_extensions/hak/regeln.md`,
  klassenspezifische in die CLAUDE.md des Skripts. Die „Pflege“-Regel der
  heutigen CLAUDE.md entsprechend umformulieren.

## Vorgehen

1. Bestand aufnehmen: CLAUDE.md, README, `_quarto.yml`, `_quarto-folien.yml`,
   `justfile`, Workflow, `_filters/`, `_includes/`, `_shortcodes/`,
   `_python/grafiken.py` lesen.
2. Vergleichsstand sichern: vor jeder Änderung HTML, PDF und Folien rendern und
   die Ergebnisse ins Scratchpad kopieren.
3. Offene technische Fragen klären (Quarto-Doku online prüfen, lokale Version
   1.10.18), bevor du baust:
   - Kann `_brand.yml` samt Logos in der Extension liegen und für html, typst
     und revealjs wirken (inkl. hell/dunkel im HTML)? Falls nicht: beste
     Alternative vorschlagen.
   - Kopiert `quarto add` alle Dateien des Extension-Ordners (auch `hak.just`,
     `stil.py`, `regeln.md`)?
   - Wie importiert `grafiken.py` sauber aus `_extensions/hak/stil.py`, sodass
     die Setup-Zellen weiter `from _python.grafiken import *` verwenden können?
   - Laufen die importierten just-Befehle im Skript-Ordner?
   - Wie wird das Folien-Logo (heute absoluter Pfad `/hak-logo.png`) aus der
     Extension eingebunden?
   Wenn eine Frage zu einer anderen Lösung führt als oben geplant, frag mich
   vorher.
4. `quarto-hak` aufbauen (Dateikopf-Kommentare wie bisher, alles auf Deutsch),
   inkl. README mit Checkliste und eigener CLAUDE.md.
5. `hak-mam-1` umstellen: Extension mit `quarto add ../quarto-hak` einbinden,
   alte Dateien entfernen, die nun aus der Extension kommen, Konfiguration,
   CLAUDE.md, README und `justfile` kürzen, `.claude/settings.json` anlegen.
6. Testen: HTML, PDF und Folien neu rendern und mit dem Vergleichsstand
   vergleichen. Das Ergebnis muss gleich aussehen (Farben, Schriften, Logos
   hell/dunkel, Dezimalkomma, Intervalle, Anführungszeichen, Buchbeispiel-Kästen,
   Grafiken, PDF-Nummerierung, Folien-Aufteilung). Alle just-Befehle
   ausprobieren. Auch den GitHub-Workflow prüfen (`uv sync --locked --no-dev`,
   Skript und Folien rendern mit Extension).
7. Folien auf GitHub Pages: Was davon für alle Klassen gilt (z. B.
   Übersichtsseite, Logo-Einbindung, gemeinsame just-Befehle), in die Extension
   verschieben. Lokal so testen wie im Workflow (Skript und Folien rendern,
   zusammenkopieren, unter dem Unterpfad `/hak-mam-1/` ausliefern):
   Übersichtsseite, Links, Logo, Grafiken, Link vom Skript zu den Folien.
   Die Datei `folien-online.md` ist erledigt; frag mich, ob sie gelöscht
   werden soll.

Bevor du in einem der beiden Repos committest oder etwas pushst, zeig mir die
Änderungen und das Testergebnis und frag mich. Commit-Messages auf Deutsch.
