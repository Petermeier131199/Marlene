"""Innerself Detox - Intro-Renderer.

Komponiert den animierten Titel ueber den (bewegten oder stehenden) Hintergrund
und schreibt ein MP4. Timing folgt einem Atemrhythmus.
"""
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import titleart as T

W, H = T.W, T.H
import os
FPS = int(os.environ.get("FPS", 30))
DUR = 5.0
N = int(round(DUR * FPS))

# --- Timeline (Sekunden) -----------------------------------------------------
GLOW_IN, GLOW_FULL = 1.10, 2.60
TITLE_IN, TITLE_STAGGER, TITLE_LEN = 1.25, 0.55, 1.15
RULE_IN, RULE_LEN = 2.55, 0.90
FOL_IN, FOL_LEN = 2.70, 1.40
SUB_IN, SUB_LEN = 3.05, 1.10

PUSH_START = 1.045          # Heranfahren ueber die gesamte Laenge


def clamp01(x):
    return 0.0 if x < 0 else (1.0 if x > 1 else x)


def ease_out_cubic(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_out_sine(x):
    return math.sin(clamp01(x) * math.pi / 2)


def ease_in_out(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


# --- statische Elemente vorbereiten ------------------------------------------
TFONT = T.title_font()
SFONT = T.sub_font()
GLYPHS, _ = T.layout(T.TITLE, TFONT, T.TITLE_TRACK, W / 2, T.TITLE_CY)
SGLYPHS, _ = T.layout(T.SUB, SFONT, T.SUB_TRACK, W / 2, T.SUB_CY)

FOL_SIZE = int(0.58 * H)
FOL = T.flower_of_life(FOL_SIZE, int(FOL_SIZE * 0.163), width=2)


def _radial_glow():
    """Weicher warmer Schatten hinter der Schrift, damit der Titel traegt."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2.0, 0.53 * H
    d = np.sqrt(((xx - cx) / (0.46 * W)) ** 2 + ((yy - cy) / (0.30 * H)) ** 2)
    g = np.clip(1.0 - d, 0, 1) ** 1.6
    return (g * 255).astype(np.uint8)


GLOW_MASK = Image.fromarray(_radial_glow(), "L").filter(ImageFilter.GaussianBlur(60))


def glyph_layer(glyphs, color, tracking_extra, dy, alpha, blur, shadow=True, shadow_blur=16, shadow_str=0.55, cy=None):
    """Zeichnet eine Textzeile mit aktueller Sperrung/Unschaerfe/Deckkraft."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    amax = max(alpha) if isinstance(alpha, list) else alpha
    if amax <= 0.002:
        return layer
    n = len(glyphs)
    widths = [g["adv"] for g in glyphs]
    total = sum(widths) + tracking_extra * (n - 1)
    pen = W / 2.0 - total / 2.0
    for i, g in enumerate(glyphs):
        a = alpha if not isinstance(alpha, list) else alpha[i]
        b = blur if not isinstance(blur, list) else blur[i]
        d = dy if not isinstance(dy, list) else dy[i]
        if a > 0.002:
            m = g["img"]
            if b > 0.4:
                m = m.filter(ImageFilter.GaussianBlur(b))
            x = int(round(pen + g["dx"]))
            y = int(round(g["y"] + d))
            if shadow:
                sh = m.filter(ImageFilter.GaussianBlur(shadow_blur))
                sh = sh.point(lambda v, a=a: int(v * a * shadow_str))
                layer.paste((26, 20, 14, 255), (x, y), sh)
            mm = m.point(lambda v, a=a: int(v * a))
            layer.paste(color + (255,), (x, y), mm)
        pen += widths[i] + tracking_extra
    return layer


def prep(glyphs, font, text, track):
    """Ergaenzt Vorschub/Offsets, damit die Sperrung pro Frame variieren kann."""
    out = []
    idx = 0
    for ch in text:
        adv = font.getlength(ch)
        if ch == " ":
            if out:
                out[-1]["adv_extra"] = adv
            continue
        g = glyphs[idx]
        idx += 1
        out.append({"img": g["img"], "y": g["y"], "adv": adv, "dx": 0.0, "adv_extra": 0.0})
    return out


def build(glyphs, font, text, track):
    gg = prep(glyphs, font, text, track)
    # dx = Abstand vom Stiftanfang zum linken Rand der Glyphenkachel
    idx = 0
    for ch in text:
        if ch == " ":
            continue
        box = font.getbbox(ch)
        pad = int(T.TITLE_SIZE * 0.6)
        gg[idx]["dx"] = box[0] - pad
        idx += 1
    # Leerzeichenvorschub in den jeweiligen Vorschub einrechnen
    for g in gg:
        g["adv"] += g.pop("adv_extra")
    return gg


TG = build(GLYPHS, TFONT, T.TITLE, T.TITLE_TRACK)
SG = build(SGLYPHS, SFONT, T.SUB, T.SUB_TRACK)


def rules_layer(p, alpha):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if alpha <= 0.002 or p <= 0:
        return layer
    d = ImageDraw.Draw(layer)
    hw = T.RULE_HALFW * p
    col = T.GOLD + (int(255 * alpha),)
    for y in (T.RULE_TOP_Y, T.RULE_BOT_Y):
        d.line([(W / 2 - hw, y), (W / 2 + hw, y)], fill=col, width=2)
    return layer.filter(ImageFilter.GaussianBlur(0.6))


def fol_layer(alpha, scale):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if alpha <= 0.002:
        return layer
    s = max(2, int(FOL_SIZE * scale))
    m = FOL.resize((s, s), Image.LANCZOS).point(lambda v: int(v * alpha))
    x, y = int(W / 2 - s / 2), int(0.505 * H - s / 2)
    layer.paste(T.GOLD + (255,), (x, y), m)
    return layer


def frame(t, bg):
    """bg: PIL-Bild in Originalgroesse (>= 1920x1080)."""
    # Heranfahren
    s = PUSH_START + (1.0 - PUSH_START) * ease_out_sine(t / DUR)
    bw, bh = bg.size
    cw, ch = bw / s, bh / s
    box = ((bw - cw) / 2, (bh - ch) / 2, (bw + cw) / 2, (bh + ch) / 2)
    img = bg.resize((W, H), Image.LANCZOS, box=box).convert("RGBA")

    # warmer Schatten hinter der Schrift
    ga = 0.34 * ease_in_out((t - GLOW_IN) / (GLOW_FULL - GLOW_IN))
    if ga > 0.002:
        glow = Image.new("RGBA", (W, H), (24, 18, 13, 0))
        glow.putalpha(GLOW_MASK.point(lambda v: int(v * ga)))
        img = Image.alpha_composite(img, glow)

    # Titel, Buchstabe fuer Buchstabe mit dem Rauch aufsteigend
    n = len(TG)
    al, bl, dl = [], [], []
    for i in range(n):
        p = ease_out_cubic((t - (TITLE_IN + TITLE_STAGGER * i / max(1, n - 1))) / TITLE_LEN)
        al.append(p)
        bl.append(22.0 * (1 - p) ** 1.7)
        dl.append(34.0 * (1 - p) ** 1.4)
    track_extra = 10.0 * (1 - ease_out_cubic((t - TITLE_IN) / (TITLE_LEN + TITLE_STAGGER)))
    if max(al) > 0.002:
        img = Image.alpha_composite(img, glyph_layer(TG, T.CREAM, T.TITLE_TRACK + track_extra, dl, al, bl))

    # Goldlinien von der Mitte nach aussen
    rp = ease_out_cubic((t - RULE_IN) / RULE_LEN)
    img = Image.alpha_composite(img, rules_layer(rp, 0.55 * rp))

    # Blume des Lebens: ein sanftes Aufglimmen (Ausatmen)
    fp = ease_in_out((t - FOL_IN) / FOL_LEN)
    swell = math.sin(min(1.0, max(0.0, (t - FOL_IN) / FOL_LEN)) * math.pi) * 0.06
    img = Image.alpha_composite(img, fol_layer(0.26 * fp + swell, 0.985 + 0.015 * fp))

    # Subline
    sp = ease_out_cubic((t - SUB_IN) / SUB_LEN)
    if sp > 0.002:
        img = Image.alpha_composite(
            img,
            glyph_layer(SG, T.GOLD_TEXT, T.SUB_TRACK + 5.0 * (1 - sp), 12.0 * (1 - sp) ** 1.4,
                        1.0 * sp, 7.0 * (1 - sp) ** 1.6, shadow_blur=9, shadow_str=1.0),
        )
    return img.convert("RGB")


def bg_frames(path, still):
    """Liefert N Hintergrundbilder - aus Video oder als Standbild."""
    if still:
        im = Image.open(path).convert("RGB")
        for _ in range(N):
            yield im
        return
    import imageio_ffmpeg
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    # Video auf 1920x1080/30fps normalisieren, leicht groesser fuer das Heranfahren
    cmd = [exe, "-v", "error", "-i", path, "-vf",
           f"fps={FPS},scale={int(W*PUSH_START)}:{int(H*PUSH_START)}:flags=lanczos:"
           f"force_original_aspect_ratio=increase,crop={int(W*PUSH_START)}:{int(H*PUSH_START)}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    bw, bh = int(W * PUSH_START), int(H * PUSH_START)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    size = bw * bh * 3
    last = None
    for _ in range(N):
        raw = p.stdout.read(size)
        if len(raw) < size:
            yield last
            continue
        last = Image.frombytes("RGB", (bw, bh), raw)
        yield last
    p.stdout.close()
    p.wait()


def main():
    src, out = sys.argv[1], sys.argv[2]
    still = src.lower().endswith((".png", ".jpg", ".jpeg"))
    import imageio_ffmpeg
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    enc = subprocess.Popen(
        [exe, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)
    for i, bg in enumerate(bg_frames(src, still)):
        enc.stdin.write(frame(i / FPS, bg).tobytes())
    enc.stdin.close()
    enc.wait()
    print("fertig:", out)


if __name__ == "__main__":
    main()
