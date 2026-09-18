"""Baut 1080p-Vorschauen: Overlays ueber Beispielbilder gelegt.

Ein MOV mit Alphakanal laesst sich nicht direkt ansehen - diese Vorschauen
zeigen, wie die Einblendungen ueber echtem Bildmaterial wirken.
"""
import os, subprocess, sys
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
A = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def lauf(args):
    subprocess.run([FF, "-v", "error", "-y", *args], check=True)


# Stellvertreter fuer echtes Videomaterial: warme Szene und neutrales Grau
SZENE = sys.argv[3]

# 1) Bauchbinde ueber Standbild
lauf(["-loop", "1", "-t", "8", "-i", SZENE, "-i", f"{A}/bauchbinde-vanessa-spaleck.mov",
      "-filter_complex",
      "[0:v]scale=1920:1080,setsar=1[bg];[1:v]scale=1920:1080[ov];[bg][ov]overlay=format=auto",
      "-r", "60", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
      f"{OUT}/vorschau-bauchbinde.mp4"])

# 2) Uebergaenge: Schnitt in der Mitte, Overlay darueber
for name, dauer in [("lichtbluete", 1.0), ("atemblende", 0.6), ("faecher", 1.2)]:
    vor, nach = 1.0, 1.0
    ges = vor + dauer + nach
    mitte = vor + dauer / 2
    lauf(["-loop", "1", "-t", f"{ges}", "-i", SZENE,
          "-f", "lavfi", "-t", f"{ges}",
          "-i", f"color=c=0x2e2b28:s=1920x1080:r=60,"
                f"geq=lum='if(gt(X,0),120+40*sin(X/300)+30*sin(Y/220),0)':cb=128:cr=128",
          "-i", f"{A}/uebergang-{name}.mov",
          "-filter_complex",
          f"[0:v]scale=1920:1080,setsar=1,trim=0:{mitte},setpts=PTS-STARTPTS[a];"
          f"[1:v]trim=0:{ges-mitte},setpts=PTS-STARTPTS[b];"
          f"[a][b]concat=n=2:v=1[base];"
          f"[2:v]scale=1920:1080,setpts=PTS-STARTPTS+{vor}/TB[ov];"
          f"[base][ov]overlay=format=auto:eof_action=pass",
          "-t", f"{ges}", "-r", "60", "-c:v", "libx264", "-crf", "18",
          "-pix_fmt", "yuv420p", f"{OUT}/vorschau-uebergang-{name}.mp4"])

# 3) Vollbildkarten auf 1080p verkleinern
for f in ["titel-opener.mp4", "kapitelkarte-beispiel.mp4", "outro-anmeldung.mp4"]:
    if os.path.exists(f"{A}/{f}"):
        lauf(["-i", f"{A}/{f}", "-vf", "scale=1920:1080", "-c:v", "libx264",
              "-crf", "20", "-pix_fmt", "yuv420p", f"{OUT}/vorschau-{f}"])
print("Vorschauen fertig:", sorted(os.listdir(OUT)))
