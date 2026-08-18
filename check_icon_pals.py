import os
import struct

BASE = "/Users/bekirkarakose/Documents/ProjectAlascatra"
pal_files = [
    "graphics/pokemon/icon_palettes/icon_palette_0.gbapal",
    "graphics/pokemon/icon_palettes/icon_palette_1.gbapal",
    "graphics/pokemon/icon_palettes/icon_palette_2.gbapal",
]

for f in pal_files:
    path = os.path.join(BASE, f)
    with open(path, "rb") as bf:
        data = bf.read()
    print(f"Palette {f[-8]}:")
    for i in range(16):
        c = struct.unpack("<H", data[i*2:i*2+2])[0]
        r = (c & 0x1F) * 8
        g = ((c >> 5) & 0x1F) * 8
        b = ((c >> 10) & 0x1F) * 8
        print(f"  {i}: RGB({r}, {g}, {b})")
