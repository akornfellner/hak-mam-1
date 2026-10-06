# Befehle für das Skript. Übersicht: just
#
# Die gemeinsamen Befehle (preview, render, folien, online, extension, …) kommen
# aus der Extension. Hier darunter nur Befehle, die es nur in dieser Klasse gibt.

import '_extensions/hak/hak.just'

# Muss hier stehen, nicht in der Extension: just nimmt als Standardbefehl nur
# einen Befehl aus dem justfile selbst, keinen eingebundenen.
[private]
default:
  @just --list
