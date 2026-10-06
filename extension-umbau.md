Ich möchte die Technik meines Skripts in eine eigene Quarto-Extension auslagern,
damit ich später für jede Klasse ein eigenes Skript-Repo habe (eigene GitHub
Pages-Seite pro Klasse), Design, Filter, Regeln und Befehle aber nur an einer
Stelle pflege.

Stand dieses Prompts: 5. Oktober 2026, Commit `909e614`. Seither habe ich am
Skript weitergearbeitet (neue Kapitel, vielleicht neue Zeichnungen in
`grafiken.py`, neue Regeln in CLAUDE.md, neue just-Befehle). Alle Angaben unten
zu Dateien und Inhalten beschreiben den Stand von damals. Maßgeblich ist, was
jetzt im Repo steht: Nimm den Bestand neu auf und übernimm alles, was seither
dazugekommen ist. CLAUDE.md und README wissen bewusst noch nichts vom Umbau.
Wenn etwas Neues nicht zum Plan passt, frag mich.

Ausgangslage:
- Wir sind in `~/Dokumente/Skript/hak-mam-1` (Skript 1. Klasse, läuft fehlerfrei).
- Die Folien sind bereits auf GitHub Pages veröffentlicht (Übersichtsseite
  unter `/hak-mam-1/folien/`, Aufbau siehe unten „Folien“). Das muss nach
  dem Umbau unverändert funktionieren, ich brauche die Folien im Unterricht.
- Rückfallpunkt: der **letzte Commit vor dem Umbau**, also der aktuelle Stand
  von `main` beim Start dieser Sitzung (nicht `909e614`, seither sind Kapitel
  dazugekommen). Prüfe als Erstes, dass der Arbeitsordner sauber und alles
  gepusht ist und dass der letzte Lauf des Workflows auf GitHub erfolgreich
  war. Nenne mir die Commit-Nummer und setze nach Rückfrage das Tag
  `vor-extension-umbau` darauf (auch pushen).
  Zurück geht es später mit `git revert --no-commit vor-extension-umbau..HEAD`
  (bzw. mit der Commit-Nummer statt des Tags), danach committen und pushen.
  Kein `git reset --hard`, kein force push.
- Daneben liegt `~/Dokumente/Skript/hak-quarto`: ein leeres, öffentliches
  GitHub-Repo (`akornfellner/hak-quarto`), bereits per SSH geklont.
- Übersicht auf GitHub: Alle zusammengehörigen Repos beginnen mit `hak-` und
  tragen das Topic `mathe-skript`. Topics und angeheftete Repos stelle ich
  selbst auf GitHub ein (`gh` ist auf diesem Rechner nicht installiert).
  Erinnere mich am Ende daran und nimm „Topic `mathe-skript` setzen, Repo am
  Profil anheften“ in die Checkliste „Neue Klasse anlegen“ auf.
- Prüfe zuerst, ob du auf `../hak-quarto` zugreifen kannst. Falls nicht, sag
  mir, dass ich `/add-dir ../hak-quarto` ausführen soll.

## Folien (Stand `909e614`, bitte mit dem Repo abgleichen)

- `_quarto-folien.yml`: Profil mit Projekttyp `website` (nicht `default`), rendert
  `folien-uebersicht.qmd` und `*/folien-*.qmd` nach `_folien/`. Nur mit
  `website` schreibt Quarto das Logo aus `_brand.yml` mit relativem Pfad
  (`../hak-logo.png`); sonst fehlt es unter `/hak-mam-1/folien/`.
- `folien-uebersicht.qmd` → `_folien/index.html`: normale HTML-Seite, eine
  Python-Zelle findet alle `NN-…/folien-N.qmd` und verlinkt sie. Aussehen in
  `_includes/folien-uebersicht.css`.
- Workflow: Skript als HTML rendern, Folien rendern, `_folien/` nach
  `_book/folien/` kopieren, `_book/` veröffentlichen.
- `_quarto.yml`: Link „Folien“ in der Navigationsleiste (`book: navbar`,
  `href: folien/index.html`).
- `justfile`: `online-bauen` und `online` bauen `_online/hak-mam-1/` wie der
  Workflow und liefern es unter <http://localhost:8000/hak-mam-1/> aus. Der
  Repo-Name `hak-mam-1` steht dort fest drin.
- Alle Verweise sind relativ, weil die Seite unter `/hak-mam-1/` liegt.

## Zielstruktur

```
~/Dokumente/Skript/
  hak-quarto/        Extension-Repo (Technik für alle Klassen)
  hak-mam-1/         Skript 1. Klasse
  hak-mam-2/ …       später, durch Klonen + Checkliste
```

`hak-quarto` (alles, was alle Klassen gemeinsam haben):

```
hak-quarto/
  README.md                 Zweck, Installation, Update, Checkliste
                            „Neue Klasse anlegen“
  CLAUDE.md                 Regeln für die Arbeit am Extension-Repo selbst
  justfile                  Befehle für das Extension-Repo, v. a.
                            `alle-aktualisieren` (siehe Abläufe)
  .github/workflows/pages.yml   wiederverwendbarer Workflow (workflow_call):
                            Skript und Folien rendern, zusammenkopieren, auf
                            GitHub Pages veröffentlichen; Quarto- und
                            uv-Version stehen nur hier
  _extensions/hak/
    _extension.yml          Formate hak-html, hak-typst, hak-revealjs mit allen
                            heutigen Einstellungen, Filtern, Kurzbefehlen
    _brand.yml, hak-logo.png, hak-logo-dunkel.png
    filters/                dezimalkomma, intervallklammern,
                            deutsche-anfuehrungszeichen, pdf-nummerierung
    buch.lua                Kurzbefehl {{< buch … >}}
    buchbeispiele.css, typst-anpassungen.typ
    folien-uebersicht.css   Aussehen der Folien-Übersichtsseite
    _folien-uebersicht.qmd  Inhalt der Übersichtsseite (Python-Zelle, Link
                            „Zum Skript“), wird im Skript per include eingebunden
    stil.py                 Farben, rcParams, zahl(), tausender()
    regeln.md               allgemeine Regeln (Großteil der heutigen CLAUDE.md,
                            auch Folien-Aufteilung, „Verweise relativ“,
                            Test mit `just online`)
    hak.just                gemeinsame just-Befehle, auch online-bauen/online
                            ohne festen Repo-Namen (aus dem Ordnernamen bzw.
                            einer Variable im justfile des Skripts)
```

`hak-mam-1` (nur was zur Klasse gehört, plus Projektdateien, die Quarto im
Projektordner braucht):

```
hak-mam-1/
  _extensions/hak/          Kopie der Extension, mitcommittet, nie direkt bearbeiten
  _quarto.yml               Projekttyp book, Titel, Untertitel, Kapitelliste,
                            Navbar-Link „Folien“, format: hak-html / hak-typst
  _quarto-folien.yml        Projektteil bleibt (website, output-dir, render-Liste),
                            Format: hak-revealjs; Klasse/Untertitel der Folien
                            möglichst nur hier
  folien-uebersicht.qmd     nur noch Kopf (Titel, Format, output-file) + include
                            des Inhalts aus der Extension
  NN-…/folien-N.qmd         Titel + includes, format: hak-revealjs
  _python/grafiken.py       importiert stil.py, dazu nur die Zeichnungen dieser
                            Klasse (damals: zahlengerade, primfaktoren,
                            primfaktor_treppe; inzwischen evtl. mehr)
  CLAUDE.md                 kurz: 1. Klasse, Adressen, Import
                            @_extensions/hak/regeln.md, Hinweis „Allgemeines nur
                            in ../hak-quarto ändern“
  justfile                  import '_extensions/hak/hak.just' (+ Klassenbefehle)
  .claude/settings.json     ../hak-quarto als zusätzlicher Ordner (additionalDirectories)
  .github/workflows/pages.yml   nur wenige Zeilen: Auslöser (Push auf main) und
                            Aufruf des Workflows aus akornfellner/hak-quarto
  pyproject.toml, uv.lock, .python-version, _environment, .gitignore,
  README.md, index.qmd, 01-…/
```

Bewusst pro Skript bleiben: `pyproject.toml`/`uv.lock`, `_environment`,
`grafiken.py` mit den Zeichnungen der Klasse und der kurze Workflow, der den
gemeinsamen aufruft. Geplant sind fünf Skripten (eines pro Klasse), deshalb
soll auch der Workflow nur an einer Stelle gepflegt werden. Projekt-Einstellungen (`project:`, `book:`)
kann eine Format-Extension nicht liefern, sie bleiben in `_quarto.yml` und
`_quarto-folien.yml`. Kein Quarto-Template: neue Klassen entstehen durch Klonen
des neuesten Skripts und die Checkliste im README von `hak-quarto`.

Die Klasse („1. Klasse HAK“) und der Repo-Name (`hak-mam-1`) sollen nach dem
Umbau an möglichst wenigen Stellen stehen. Heute: `_quarto.yml`, jede
`folien-N.qmd`, `folien-uebersicht.qmd`, `justfile`, CLAUDE.md, README,
`pyproject.toml`, Kommentar in `_quarto-folien.yml`. Alle verbleibenden Stellen
in die Checkliste aufnehmen.

## Abläufe, die danach funktionieren sollen (in regeln.md / CLAUDE.md festhalten)

- **Allgemeine Änderung beim Arbeiten an einer Klasse:** Claude ändert die
  Datei in `../hak-quarto` (nie in `_extensions/` des Skripts), testet mit
  `quarto add ../hak-quarto` im aktuellen Skript, committet in beiden Repos und
  pusht `hak-quarto` erst nach Rückfrage.
- **Andere Klassen aktualisieren:** just-Befehl (z. B. `just extension`), der
  die Extension von GitHub holt (`akornfellner/hak-quarto`), ohne Rückfragen;
  danach rendern und committen. Funktioniert auch ohne lokalen
  `hak-quarto`-Ordner.
- **Alle Klassen auf einmal aktualisieren:** `just alle-aktualisieren` im
  Ordner `hak-quarto`: geht der Reihe nach durch alle Nachbarordner
  `../hak-mam-*`, aktualisiert dort die Extension aus dem lokalen `hak-quarto`
  und rendert zur Kontrolle (HTML, PDF, Folien). Am Ende eine Übersicht, in
  welchem Skript es geklappt hat und wo nicht. Nicht committen und nicht
  pushen, das mache ich bewusst pro Klasse. Skripten mit nicht committeten
  Änderungen überspringen und melden.
- **Workflow ändern** (z. B. neue Quarto-Version): nur in
  `hak-quarto/.github/workflows/pages.yml`. Die Skripten übernehmen das beim
  nächsten Push von selbst.
- **Neue Klasse:** Checkliste im README von `hak-quarto` (neue Git-Historie bzw.
  „Use this template“, Kapitel löschen, `grafiken.py` auf den Stil-Import
  reduzieren, Klasse und Repo-Name an allen verbleibenden Stellen anpassen,
  `index.qmd`, `uv sync`, Pages einschalten, mit `just online` testen).
- **Neue Regeln:** allgemeine in `hak-quarto/_extensions/hak/regeln.md`,
  klassenspezifische in die CLAUDE.md des Skripts. Die „Pflege“-Regel der
  heutigen CLAUDE.md entsprechend umformulieren.

## Vorgehen

1. Bestand aufnehmen: CLAUDE.md, README, `_quarto.yml`, `_quarto-folien.yml`,
   `justfile`, Workflow, `folien-uebersicht.qmd`, `_filters/`, `_includes/`,
   `_shortcodes/`, `_python/grafiken.py` lesen.
2. Vergleichsstand sichern: vor jeder Änderung HTML, PDF und Folien rendern
   (`just render`, `just online-bauen`) und `_book/`, `_folien/` und `_online/`
   ins Scratchpad kopieren.
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
   - Folien-Logo: Heute liegt es im Projektordner und kommt mit relativem Pfad
     in die Folien (nur mit Projekttyp `website`, dazu `resources:
     /hak-logo.png`). Bleibt der Pfad relativ, wenn Logo und `_brand.yml` in
     `_extensions/hak/` liegen, und wird die Datei nach `_folien/` kopiert?
     Das ist der heikelste Punkt, zuerst klären.
   - Wiederverwendbarer Workflow: Funktioniert die Veröffentlichung auf GitHub
     Pages (Rechte `pages: write`, `id-token: write`, Umgebung `github-pages`,
     `concurrency`) aus einem aufgerufenen Workflow eines anderen Repos, und
     was muss dafür im aufrufenden Workflow stehen? Auf welchen Stand verweisen
     die Skripten (`@main` oder ein Tag)? Empfehlung mit Begründung, dann frag
     mich. Actions-Versionen wie bisher online prüfen.
   - Kann `folien-uebersicht.qmd` ihren Inhalt per `{{< include >}}` aus
     `_extensions/hak/` holen (Python-Zelle läuft im Projektordner, Glob auf
     `[0-9]*/folien-*.qmd` findet weiter alle Kapitel)?
   - Wo lässt sich der Untertitel der Folien (Klasse) einmal festlegen, sodass
     er für alle `folien-N.qmd` und die Übersichtsseite gilt?
   Wenn eine Frage zu einer anderen Lösung führt als oben geplant, frag mich
   vorher.
4. `hak-quarto` aufbauen (Dateikopf-Kommentare wie bisher, alles auf Deutsch),
   inkl. README mit Checkliste und eigener CLAUDE.md.
5. `hak-mam-1` umstellen: Extension mit `quarto add ../hak-quarto` einbinden,
   alte Dateien entfernen, die nun aus der Extension kommen, Konfiguration,
   CLAUDE.md, README und `justfile` kürzen, `.claude/settings.json` anlegen.
6. Testen: HTML, PDF und Folien neu rendern und mit dem Vergleichsstand
   vergleichen. Das Ergebnis muss gleich aussehen (Farben, Schriften, Logos
   hell/dunkel, Dezimalkomma, Intervalle, Anführungszeichen, Buchbeispiel-Kästen,
   Grafiken, PDF-Nummerierung, Folien-Aufteilung). Alle just-Befehle
   ausprobieren. Den Workflow Schritt für Schritt lokal nachstellen
   (`uv sync --locked --no-dev`, `quarto render --to html`,
   `quarto render --profile folien`, Kopieren nach `_book/folien/`).
7. Online-Version testen: `just online` und unter
   <http://localhost:8000/hak-mam-1/> prüfen: Skript, Link „Folien“ in der
   Navigationsleiste, Übersichtsseite (alle Kapitel, Aussehen), Folien mit
   Logo, Grafiken und Buchbeispiel-Kästen, Link „Zum Skript“. In den erzeugten
   HTML-Dateien darf kein Verweis mit führendem `/` stehen. `_online/` mit dem
   Vergleichsstand vergleichen.

8. Workflow auf GitHub prüfen: Zuerst `hak-quarto` pushen (der Workflow muss
   dort vorhanden sein), dann `hak-mam-1`. Den Lauf unter „Actions“ verfolgen
   (mit `gh run watch`, falls `gh` installiert ist; sonst bitte mich, den Lauf
   im Browser anzusehen, und warte auf meine Rückmeldung) und danach die echte Seite prüfen: Skript, Übersichtsseite
   und Folien mit Logo unter <https://akornfellner.github.io/hak-mam-1/>.
   Schlägt der Lauf fehl, bleibt die alte Version online; sag mir trotzdem
   sofort Bescheid und schlage vor, wie es weitergeht (notfalls Rückfallpunkt).
9. `just alle-aktualisieren` in `hak-quarto` ausprobieren (derzeit nur ein
   Skript).
10. Abschluss: eine ausführliche Erklärung der neuen Struktur, im Chat und
    dauerhaft im README von `hak-quarto` (die README der Skripten verweist
    darauf). Für mich geschrieben: Ich kenne das Skript gut, Git und die
    Quarto-Technik aber wenig. Inhalt:
    - Wo liegt was: jede Datei bzw. jeder Ordner in `hak-quarto` und in einem
      Skript mit einem Satz zum Zweck.
    - „Ich will … ändern“ als Tabelle mit Ort und nötigen Schritten danach,
      mindestens für: Farbe/Schrift/Logo, Aussehen der Buchbeispiel-Kästen,
      Filter (Dezimalkomma, Intervalle), PDF-Vorlage, Folien-Einstellungen,
      Folien-Übersichtsseite, Grafikstil, neue Zeichnung für eine Klasse,
      Regel für Claude (allgemein bzw. nur eine Klasse), just-Befehl
      (allgemein bzw. nur eine Klasse), Workflow bzw. Quarto-/uv-Version,
      Python-Paket, neues Kapitel, Titel/Klasse.
    - Die Abläufe Schritt für Schritt mit den genauen Befehlen: allgemeine
      Änderung testen und übernehmen, eine Klasse aktualisieren, alle Klassen
      aktualisieren, neue Klasse anlegen (Checkliste), neuer Rechner.
    - Was man nie tun darf (z. B. `_extensions/` im Skript direkt bearbeiten)
      und wie man zum Rückfallpunkt zurückkommt.
    - Was vom ursprünglichen Plan abweicht und warum.

Bevor du in einem der beiden Repos committest oder etwas pushst, zeig mir die
Änderungen und das Testergebnis und frag mich. Commit-Messages auf Deutsch.
