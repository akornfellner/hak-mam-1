"""Zeichnungen für die matplotlib-Grafiken dieses Skripts.

Einbinden in einer .qmd-Datei (Code wird dank `echo: false` nie angezeigt):

    ```{python}
    #| include: false
    from _python.grafiken import *
    ```

Farben, Schrift, `zahl()` und `tausender()` sind für alle Klassen gleich und
kommen aus `_extensions/hak/stil.py` (Repo hak-quarto, dort ändern). Hier stehen
nur die Zeichnungen, die diese Klasse braucht.
"""

import sys
from pathlib import Path

# Stil aus der Extension laden (Farben, rcParams, zahl(), tausender(), plt, np)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_extensions" / "hak"))
from stil import *  # noqa: E402,F401,F403


def zahlengerade(von, bis, intervalle=(), punkte=(), schritt=1,
                 breite=7, hoehe=1.0):
    """Zahlengerade von `von` bis `bis` mit markierten Intervallen und Punkten.

    intervalle: Liste von (a, b, a_dabei, b_dabei).
        a = None bedeutet −∞, b = None bedeutet +∞.
        a_dabei / b_dabei: True → Randpunkt ausgefüllt (Zahl gehört dazu),
        False → Randpunkt leer (Zahl gehört nicht dazu).
    punkte: einzelne Zahlen, die als ausgefüllte Punkte markiert werden.
    """
    rand = 0.6 * schritt
    links, rechts = von - rand, bis + rand

    fig, ax = plt.subplots(figsize=(breite, hoehe))
    ax.set_xlim(links, rechts)
    ax.set_ylim(-0.8, 0.5)
    ax.axis("off")

    # Achse mit Pfeil
    ax.annotate("", xy=(rechts, 0), xytext=(links, 0),
                arrowprops=dict(arrowstyle="-|>", color=SCHWARZ, lw=1.2,
                                shrinkA=0, shrinkB=0))

    # Striche und Beschriftung
    for k in np.arange(von, bis + schritt / 2, schritt):
        ax.plot([k, k], [-0.1, 0.1], color=SCHWARZ, lw=1.2)
        ax.text(k, -0.3, zahl(k), ha="center", va="top")

    # Intervalle: dicke rote Linie, Randpunkte voll oder leer
    for a, b, a_dabei, b_dabei in intervalle:
        x0 = links if a is None else a
        x1 = rechts - 0.15 * schritt if b is None else b
        ax.plot([x0, x1], [0, 0], color=ROT, lw=4, solid_capstyle="butt",
                zorder=3)
        for x, dabei, offen in ((a, a_dabei, a is None), (b, b_dabei, b is None)):
            if offen:
                continue
            ax.plot(x, 0, "o", ms=11, mew=2, mec=ROT,
                    mfc=ROT if dabei else "white", zorder=4)

    for x in punkte:
        ax.plot(x, 0, "o", ms=9, color=ROT, zorder=4)

    return fig


def primfaktoren(n):
    """Liste der Primfaktoren von n, der Größe nach: 1092 → [2, 2, 3, 7, 13]."""
    faktoren, teiler = [], 2
    while n > 1:
        while n % teiler == 0:
            faktoren.append(teiler)
            n //= teiler
        teiler += 1
    return faktoren


def primfaktor_treppe(*zahlen, zeile=0.32):
    """Primfaktorzerlegung als „Treppe“: links die Zahl, rechts der Teiler.

    Mehrere Zahlen stehen nebeneinander. Die Ausgangszahl ist rot.
    """
    spalten = []
    for n in zahlen:
        faktoren = primfaktoren(n)
        reste = [n]
        for p in faktoren:
            reste.append(reste[-1] // p)
        spalten.append((reste, faktoren))

    zeilen = max(len(reste) for reste, _ in spalten)
    fig, ax = plt.subplots(figsize=(1.8 * len(zahlen), zeile * zeilen + 0.1))
    ax.set_xlim(0, 1.8 * len(zahlen))
    ax.set_ylim(-zeile * (zeilen - 0.5), zeile * 0.6)
    ax.axis("off")

    for i, (reste, faktoren) in enumerate(spalten):
        strich = 1.8 * i + 0.95
        for k, rest in enumerate(reste):
            ax.text(strich - 0.1, -k * zeile, tausender(rest), ha="right",
                    va="center",
                    color=ROT if k == 0 else SCHWARZ,
                    fontweight="bold" if k == 0 else "normal")
        for k, p in enumerate(faktoren):
            ax.text(strich + 0.1, -k * zeile, str(p), ha="left",
                    va="center")
        ax.plot([strich, strich], [zeile * 0.5, -zeile * (len(reste) - 0.5)],
                color=SCHWARZ, lw=1.5)

    return fig
