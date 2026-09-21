"""Strukturtest: bekomme ich seidige Faeden? Graustufen, keine Choreografie."""
import sys, os
sys.path.insert(0, ".")
import numpy as np
from PIL import Image
from partikel import Stroemung, Wolke, auftragen, fertig

W, H = 1920, 1080
FPS, DAUER, TEIL = 30, 2.0, 6
CREME = np.array([248, 243, 232], np.float32)
TINTE = np.array([30, 34, 44], np.float32)


def lauf(ausgabe, partikel=700000, tempo=26.0, skalen=((13, 1.0), (6, 0.55), (3, 0.25)),
         saat=1, radius=120, drift=(5.0, 2.2), zittern=1.5, deckung=0.40):
    feld = Stroemung(W, H, skalen, saat=saat)
    wolke = Wolke(partikel, W, H, saat=saat + 7)
    # laenglich saeen statt als Scheibe: die Referenzen starten als Band, nicht
    # als Klumpen, und ein Band wird vom Feld sofort weiter ausgezogen
    for k in range(7):
        f = k / 6.0
        wolke.saeen_fleck((W * (0.20 + 0.30 * f), H * (0.26 + 0.26 * f)),
                          radius, anzahl=partikel // 7, streuung=0.6)
    os.makedirs(os.path.dirname(ausgabe) or ".", exist_ok=True)
    import subprocess, imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    enc = subprocess.Popen(
        [ff, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
         "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", ausgabe],
        stdin=subprocess.PIPE)
    proben = {}
    n = int(DAUER * FPS)
    for i in range(n):
        puffer = np.zeros(H * W, np.float32)
        for k in range(TEIL):
            t = (i + k / TEIL) / FPS
            # Zittern waechst: die Tinte verteilt sich mit der Zeit und wird
            # duenner, statt als kompakte Wolke zu bleiben
            z = zittern * (0.5 + 1.9 * (i / max(n - 1, 1)))
            wolke.bewegen(feld, t * 0.8, tempo, drift=drift, dt=1.0 / TEIL * 3.4,
                          zittern=z)
            auftragen(puffer, wolke, W, H, 1.0 / TEIL)
        d = fertig(puffer, W, H, 0.5)
        a = 1.0 - np.exp(-d * deckung)         # Dichte in Deckung uebersetzen
        rgb = CREME[None, None, :] * (1 - a[..., None]) + TINTE[None, None, :] * a[..., None]
        bild = np.clip(rgb, 0, 255).astype(np.uint8)
        enc.stdin.write(bild.tobytes())
        if i in (3, 12, 21, 32, 44, 56):
            proben[i] = Image.fromarray(bild)
    enc.stdin.close()
    enc.wait()
    return proben


if __name__ == "__main__":
    import time
    t0 = time.time()
    p = lauf(sys.argv[1] if len(sys.argv) > 1 else "/tmp/strukturtest.mp4")
    print("Lauf in %.0fs" % (time.time() - t0))
    bogen = Image.new("RGB", (1920, 540), (255, 255, 255))
    for i, (k, im) in enumerate(sorted(p.items())):
        bogen.paste(im.resize((640, 360), Image.LANCZOS).crop((0, 45, 640, 315)),
                    ((i % 3) * 640, (i // 3) * 270))
    bogen.save("/tmp/struktur.png")
    print("Bogen fertig")
