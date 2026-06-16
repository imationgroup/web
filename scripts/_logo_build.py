"""Generate favicon.ico + PNG icon set from the source PNG logo.

Source: D:/IMATIONGROUP/logo/logo3_1.png  (the circular isotipo).
Outputs into the repo root so nginx serves them at /favicon.ico etc.
"""
from pathlib import Path
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
SRC = Path(r"D:/IMATIONGROUP/logo/logo3_1.png")

assert SRC.is_file(), f"missing source logo at {SRC}"

img = Image.open(SRC).convert("RGBA")
print(f"source: {SRC.name}  {img.size}")

# The source PNG has a solid-white background even though it's RGBA. Flood-fill
# from the four corners turning near-white pixels into transparent ones. We
# only fill from the OUTSIDE, so any white pixel that lives inside the logo
# (e.g. an inner highlight) is preserved.
w, h = img.size
fill_tolerance = 18  # 0..255: accept slight color variance at antialiased edge
for corner in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    px = img.getpixel(corner)
    if px[0] > 245 and px[1] > 245 and px[2] > 245:
        ImageDraw.floodfill(img, corner, (0, 0, 0, 0), thresh=fill_tolerance)

# Soften residual halo: a near-white pixel that BORDERS a transparent one is
# part of the aliased ring around the outside of the circle. Dissolve only
# those — interior white pixels (the "ig" letters) have no transparent
# neighbor, so they stay untouched.
pixels = img.load()
to_soften = []
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if a == 0:
            continue
        if r > 235 and g > 235 and b > 235:
            has_transparent_neighbor = False
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and pixels[nx, ny][3] == 0:
                    has_transparent_neighbor = True
                    break
            if has_transparent_neighbor:
                to_soften.append((x, y, r, g, b, a))
for x, y, r, g, b, a in to_soften:
    whiteness = (r + g + b) / 3
    pixels[x, y] = (r, g, b, max(0, int(a * (255 - whiteness) / 20)))
print(f"flood-filled white background -> alpha (softened {len(to_soften)} edge pixels)")

# Ensure square: pad transparent to make it square if not already.
w, h = img.size
if w != h:
    side = max(w, h)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    img = sq
    print(f"padded to square {side}x{side}")

# Outputs.
OUT = {
    "favicon.png": [256],                # generic PNG favicon (modern browsers)
    "favicon-16x16.png": [16],
    "favicon-32x32.png": [32],
    "apple-touch-icon.png": [180],       # iOS home screen
    "icon-192.png": [192],               # PWA manifest
    "icon-512.png": [512],               # PWA manifest
    "logo-icon.png": [128],              # navbar use
}
for name, sizes in OUT.items():
    size = sizes[0]
    resized = img.resize((size, size), Image.LANCZOS)
    out = REPO / name
    resized.save(out, "PNG", optimize=True)
    print(f"  wrote {name}  ({size}x{size}, {out.stat().st_size//1024} KB)")

# Multi-resolution ICO (Windows/legacy browsers expect 16, 32, 48 inside ONE file).
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
ico_path = REPO / "favicon.ico"
img.save(ico_path, format="ICO", sizes=ico_sizes)
print(f"  wrote favicon.ico  ({len(ico_sizes)} sizes, {ico_path.stat().st_size//1024} KB)")

# Replace favicon.svg with a minimal SVG that just <image>-embeds the 256 PNG
# base64 -- keeps the .svg URL the previous templates link to working.
import base64
png256 = REPO / "favicon.png"
b64 = base64.b64encode(png256.read_bytes()).decode("ascii")
svg = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">\n'
    f'  <image href="data:image/png;base64,{b64}" width="256" height="256"/>\n'
    '</svg>\n'
)
(REPO / "favicon.svg").write_text(svg, encoding="utf-8")
print(f"  wrote favicon.svg (PNG-embedded SVG wrapper, {len(svg)//1024} KB)")
