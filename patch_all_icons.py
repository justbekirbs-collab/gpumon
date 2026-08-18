import os
import struct
from PIL import Image

BASE = "/Users/bekirkarakose/Documents/ProjectAlascatra"
BRAIN_DIR = "/Users/bekirkarakose/.gemini/antigravity-ide/brain/9278a478-ffc5-40b2-acf9-aa13454eaadd"

src_icon = None
for f in os.listdir(BRAIN_DIR):
    if f.startswith("party_gpu_icon_"):
        src_icon = os.path.join(BRAIN_DIR, f)
        break

if not src_icon:
    print("Source icon not found!")
    exit(1)

img = Image.open(src_icon).convert("RGB")
img = img.resize((32, 32), Image.LANCZOS)
sheet = Image.new("RGB", (32, 64), (255, 0, 255))
px = img.load()
for y in range(32):
    for x in range(32):
        r, g, b = px[x, y]
        if r > 230 and g > 230 and b > 230:
            pass
        else:
            sheet.putpixel((x, y), (r, g, b))
            sheet.putpixel((x, y + 32 - 1 if y > 0 else 32), (r, g, b))

p = sheet.convert("P", palette=Image.ADAPTIVE, colors=15)
pal = p.getpalette()

# Ensure palette has 48 elements
while len(pal) < 48:
    pal.append(0)

bg_idx = -1
for i in range(16):
    r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
    if r > 240 and g < 10 and b > 240:
        bg_idx = i
        break

if bg_idx == -1:
    pal[0:3] = [255, 0, 255]
    p.putpalette(pal)
elif bg_idx != 0:
    pal[0:3], pal[bg_idx*3:bg_idx*3+3] = pal[bg_idx*3:bg_idx*3+3], pal[0:3]
    p.putpalette(pal)
    px = p.load()
    for y in range(64):
        for x in range(32):
            v = px[x, y]
            if v == bg_idx: px[x, y] = 0
            elif v == 0: px[x, y] = bg_idx

pal_data = bytearray(32)
for i in range(16):
    r = pal[i*3] >> 3
    g = pal[i*3+1] >> 3
    b = pal[i*3+2] >> 3
    val = r | (g << 5) | (b << 10)
    struct.pack_into("<H", pal_data, i*2, val)

with open(os.path.join(BASE, "graphics/pokemon/icon_palettes/icon_palette_0.gbapal"), "wb") as f:
    f.write(pal_data)

poke_dir = os.path.join(BASE, "graphics/pokemon")
count = 0
for folder in os.listdir(poke_dir):
    d = os.path.join(poke_dir, folder)
    if os.path.isdir(d):
        icon_path = os.path.join(d, "icon.png")
        if os.path.exists(icon_path):
            p.save(icon_path)
            count += 1

print(f"Patched {count} pokemon icons with GPU icon! Updated icon_palette_0.")
