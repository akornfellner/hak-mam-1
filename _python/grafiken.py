"""Hilfsfunktionen für die matplotlib-Grafiken im Skript.

Einbinden in einer .qmd-Datei (Code wird dank `echo: false` nie angezeigt):

    ```{python}
    #| include: false
    from _python.grafiken import *
    ```

Stil laut CLAUDE.md: Linien schwarz, Flächen hellrot, Schrift sans-serif,
weißer Hintergrund (damit die Grafik auch im dunklen HTML-Modus lesbar ist).
"""

import matplotlib.pyplot as plt
import numpy as np

SCHWARZ = "#000000"
ROT = "#CE1F2C"
HELLROT = "#EBA5AB"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 13,
    "mathtext.fontset": "dejavusans",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
})


def zahl(x):
    """Zahl österreichisch formatieren: Dezimalkomma, echtes Minuszeichen."""
    if float(x).is_integer():
        text = str(int(x))
    else:
        text = f"{x:g}".replace(".", ",")
    return text.replace("-", "−")


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
