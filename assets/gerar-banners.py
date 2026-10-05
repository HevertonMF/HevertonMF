# Genera header.svg y footer.svg animados para el README
import os

DIR = os.path.dirname(os.path.abspath(__file__))
W = 900
FONT = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "Consolas, Menlo, 'Courier New', monospace"

GRAD = '''<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#7c3aed"><animate attributeName="stop-color" values="#7c3aed;#2563eb;#0ea5e9;#7c3aed" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="100%" stop-color="#2563eb"><animate attributeName="stop-color" values="#2563eb;#0ea5e9;#7c3aed;#2563eb" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>'''


def wave(y, amp, opacity, dur, flip=False, h=0):
    # two periods wide so it can slide seamlessly
    p = W
    d = f"M0,{y} "
    for k in range(4):
        x0 = k * p / 2
        sgn = -1 if k % 2 == 0 else 1
        if flip:
            sgn = -sgn
        d += f"Q{x0 + p / 4},{y + sgn * amp} {x0 + p / 2},{y} "
    edge = 0 if flip else h
    d += f"L{2 * p},{edge} L0,{edge} Z"
    return (f'<path d="{d}" fill="#ffffff" fill-opacity="{opacity}">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{-p} 0" dur="{dur}s" repeatCount="indefinite"/></path>')


# ---------- header ----------
H = 230
phrases = [
    "Estudiante de DAM",
    "Python · SQL · HTML · CSS",
    "Ciclista y stand up paddle",
    "Brasileño en España",
    "Amante de la vida",
]
CW, FS = 12.1, 20          # ancho aproximado de cada letra en monospace
STEP = 3.6                 # segundos por frase
DUR = STEP * len(phrases)
TYPE = 1.4                 # tiempo escribiendo

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f'<defs>{GRAD}<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>']
for i, ph in enumerate(phrases):
    w = len(ph) * CW
    s, e = i * STEP / DUR, (i + 1) * STEP / DUR
    t = (i * STEP + TYPE) / DUR
    out.append(f'<clipPath id="c{i}"><rect x="{W / 2 - w / 2:.1f}" y="110" height="40" width="0">'
               f'<animate attributeName="width" values="0;0;{w:.1f};{w:.1f};0" keyTimes="0;{s:.4f};{t:.4f};{e - 0.001:.4f};1" '
               f'calcMode="discrete" dur="{DUR}s" repeatCount="indefinite"/></rect></clipPath>')
out.append('</defs><g clip-path="url(#r)">')
out.append(f'<rect width="{W}" height="{H}" fill="url(#g)"/>')

# little floating bubbles
for x, r, d, b in [(80, 6, 7, 0), (190, 4, 9, 2), (300, 5, 8, 4), (620, 7, 10, 1), (720, 4, 7, 3), (830, 5, 9, 5), (470, 3, 6, 2.5)]:
    out.append(f'<circle cx="{x}" cy="{H}" r="{r}" fill="#ffffff" fill-opacity="0.25">'
               f'<animate attributeName="cy" values="{H + 10};-10" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')

out.append(f'<text x="{W / 2}" y="85" text-anchor="middle" font-family="{FONT}" font-size="46" font-weight="800" fill="#ffffff">'
           f'¡Hola! Soy Heverton <tspan>👋<animate attributeName="rotate" '
           f'values="0;18;-8;18;0;0" keyTimes="0;0.1;0.2;0.3;0.4;1" dur="2.5s" repeatCount="indefinite"/></tspan></text>')

# typing phrases (written char by char with discrete steps)
for i, ph in enumerate(phrases):
    w = len(ph) * CW
    x0 = W / 2 - w / 2
    s, e = i * STEP / DUR, (i + 1) * STEP / DUR
    n = len(ph)
    # build step-by-step width animation for a real typing feel
    kts, vals = ["0"], ["0"]
    for k in range(1, n + 1):
        kts.append(f"{(i * STEP + TYPE * k / n) / DUR:.4f}")
        vals.append(f"{k * CW:.1f}")
    out[out.index(next(l for l in out if l.startswith(f'<clipPath id="c{i}">')))] = (
        f'<clipPath id="c{i}"><rect x="{x0:.1f}" y="108" height="40" width="0">'
        f'<animate attributeName="width" values="0;0;{";".join(vals[1:])};0" '
        f'keyTimes="0;{s:.4f};{";".join(kts[1:])};{e:.4f}" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite"/></rect></clipPath>')
    out.append(f'<text x="{x0:.1f}" y="136" font-family="{MONO}" font-size="{FS}" fill="#e0f2fe" textLength="{w:.1f}" clip-path="url(#c{i})">{ph}</text>')
    # cursor
    cur_x = ";".join([f"{x0:.1f}"] + [f"{x0 + float(v):.1f}" for v in vals[1:]] + [f"{x0 + w:.1f}"])
    out.append(f'<rect y="116" width="3" height="24" fill="#ffffff" x="{x0:.1f}" opacity="0">'
               f'<animate attributeName="x" values="{x0:.1f};{cur_x};{x0:.1f}" keyTimes="0;{s:.4f};{";".join(kts[1:])};{e - 0.0005:.4f};1" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{s:.4f};{e:.4f}" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite"/></rect>')

out.append(wave(200, 12, 0.18, 9, h=H))
out.append(wave(212, 9, 0.28, 6, flip=True, h=H).replace(f"L{2 * W},0 L0,0", f"L{2 * W},{H} L0,{H}"))
out.append('</g></svg>')
open(os.path.join(DIR, "header.svg"), "w", encoding="utf-8").write("\n".join(out))

# ---------- footer ----------
H = 120
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f'<defs>{GRAD}<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs><g clip-path="url(#r)">',
       f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
       wave(22, 10, 0.25, 8, flip=True).replace("L1800,0 L0,0", "L1800,0 L0,0"),
       wave(14, 8, 0.15, 11).replace(f"L{2 * W},0 L0,0", f"L{2 * W},0 L0,0"),
       f'<text x="{W / 2}" y="78" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="#ffffff">'
       f'Gracias por visitar mi perfil ⭐'
       f'<animate attributeName="opacity" values="0.75;1;0.75" dur="3s" repeatCount="indefinite"/></text>',
       f'<text x="{W / 2}" y="102" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#e0e7ff">'
       f'Cada proyecto es una oportunidad para aprender algo nuevo</text>',
       '</g></svg>']
open(os.path.join(DIR, "footer.svg"), "w", encoding="utf-8").write("\n".join(out))
print("ok")
