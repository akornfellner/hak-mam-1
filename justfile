# Befehle für das Skript. Übersicht: just

default:
  @just --list

# Python-Umgebung einrichten (einmalig / nach git pull)
sync:
  uv sync

# Live-Vorschau des Skripts (HTML) im Browser
# (--render html: vorher alles neu rendern, sonst fehlen Änderungen in _N-M-*.qmd)
preview:
  uv run quarto preview --render html

# Live-Vorschau des Skripts als PDF
preview-pdf:
  uv run quarto preview --to typst --render typst

# Live-Vorschau der Folien eines Kapitels: just folien 1
folien n:
  uv run quarto preview "$(ls [0-9]*/folien-{{n}}.qmd)" --profile folien

# Skript als HTML und PDF nach _book/ rendern
render:
  uv run quarto render

# Nur das PDF des Skripts erzeugen
pdf:
  uv run quarto render --to typst

# Alle Folien nach _folien/ rendern
render-folien:
  uv run quarto render --profile folien

# Skript und Folien rendern
alles: render render-folien

# Skript (HTML) und Folien so zusammenbauen wie auf GitHub Pages → _online/hak-mam-1/
online-bauen:
  uv run quarto render --to html
  uv run quarto render --profile folien
  rm -rf _online
  mkdir -p _online/hak-mam-1/folien
  cp -r _book/. _online/hak-mam-1/
  cp -r _folien/. _online/hak-mam-1/folien/

# Online-Version lokal testen: http://localhost:8000/hak-mam-1/
online: online-bauen
  uv run python -m http.server 8000 --directory _online

# Erzeugte Dateien löschen (_book/, _folien/, _online/, .quarto/)
aufraeumen:
  rm -rf _book _folien _online .quarto
