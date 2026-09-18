"""Rendert die sechs Kapitelkarten und die passenden Themen-Bauchbinden."""
import sys
sys.path.insert(0, ".")
import render_ck as R

R.OUT = "/home/user/Marlene/kongress-2026/assets"

KAPITEL = [
    ("1", "Kapitel 1", "Was ist der Seelenplan?",          None),
    ("2", "Kapitel 2", "Was heißt es, ehrlich zu leben?",  "Authentisch im Sinne deines Seelenplans"),
    ("3", "Kapitel 3", "Wie findest du deinen Seelenplan?", None),
    ("4", "Übung",     "Alles darf da sein",               "Wahrnehmen, was gerade ist"),
    ("5", "Kapitel 5", "Annehmen, was ist",                "Deine Anteile integrieren und ganz werden"),
    ("6", "Kapitel 6", "Deine Geistführer",                "Begleiter durch dein Leben"),
]

for nr, kennz, titel, unter in KAPITEL:
    R.kapitel(titel, kennz, f"kapitel-{nr}-karte.mp4", unterzeile=unter)
for nr, kennz, titel, unter in KAPITEL:
    R.themen_bauchbinde(titel, kennz, f"kapitel-{nr}-bauchbinde.mov")
print("alle Kapitel fertig")
