#!/bin/sh
# Holt Logos und Schriften von den Originalquellen. Bewusst nicht im Repo,
# um fremde Marken- und Schriftdateien nicht weiterzuverbreiten.
set -e
cd "$(dirname "$0")"
curl -sSL -o ck26-logo.png "https://channeling-portal.de/wp-content/uploads/2026/08/Logo_CK26_1080p_final_weiss_Schatten-Kopie.png"
curl -sSL -o vs-logo.png   "https://vanessa-spaleck.de/wp-content/uploads/Vanessa_Spaleck_Logo.png"
curl -sSL -o Runalto.ttf   "https://vanessa-spaleck.de/wp-content/uploads/Runalto.ttf"
curl -sSL -o AdornStoryScript.ttf "https://vanessa-spaleck.de/wp-content/uploads/AdornStoryScript.ttf"
curl -sSL -o Montserrat.ttf "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
echo "Assets geladen."
