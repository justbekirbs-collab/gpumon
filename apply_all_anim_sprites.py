import os
import colorsys
from PIL import Image, ImageDraw

BRAIN_DIR = "/Users/bekirkarakose/.gemini/antigravity-ide/brain/9278a478-ffc5-40b2-acf9-aa13454eaadd"
BASE = "/Users/bekirkarakose/Documents/ProjectAlascatra"

# Find source images
justbekir_src = None
ultra_src = None

for f in os.listdir(BRAIN_DIR):
    if f.startswith("justbekir_rig_rgb_"): justbekir_src = os.path.join(BRAIN_DIR, f)
    elif f.startswith("ultra_rig_icon_"): ultra_src = os.path.join(BRAIN_DIR, f)

BG = (255, 0, 255)

def safe_quantize(img_rgb):
    """Quantize RGB to 16-color palette, force BG=magenta at index 0"""
    p = img_rgb.convert("P", palette=Image.ADAPTIVE, colors=15)
    pal = p.getpalette()
    
    bg_idx = -1
    for i in range(16):
        r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
        if abs(r-255)+abs(g-0)+abs(b-255) < 80:
            bg_idx = i
            break
    
    if bg_idx == -1:
        pal[0:3] = [255, 0, 255]
        p.putpalette(pal)
    elif bg_idx != 0:
        pal[0:3], pal[bg_idx*3:bg_idx*3+3] = pal[bg_idx*3:bg_idx*3+3], pal[0:3]
        p.putpalette(pal)
        px = p.load()
        w, h = p.size
        for y in range(h):
            for x in range(w):
                v = px[x, y]
                if v == bg_idx: px[x, y] = 0
                elif v == 0: px[x, y] = bg_idx
    return p

def make_rig_frame(src_path, size, hue_shift=0):
    """Make a single rig frame at given size from source image"""
    img = Image.open(src_path).convert("RGB")
    img = img.resize(size, Image.LANCZOS)
    px = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            r, g, b = px[x, y]
            if r > 230 and g > 230 and b > 230:
                px[x, y] = BG
            elif hue_shift != 0 and (abs(r-255)+abs(g-0)+abs(b-255)) > 80:
                h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
                h = (h + hue_shift/360.) % 1.
                rn, gn, bn = colorsys.hsv_to_rgb(h, s, v)
                px[x, y] = (int(rn*255), int(gn*255), int(bn*255))
    return img

def make_sheet(src, frames_layout, out_path, hue=0):
    """frames_layout: list of (x, y, w, h) positions in output sheet"""
    if not frames_layout:
        return
    # Compute sheet size
    max_x = max(x+w for x,y,w,h in frames_layout)
    max_y = max(y+h for x,y,w,h in frames_layout)
    sheet = Image.new("RGB", (max_x, max_y), BG)
    for (fx, fy, fw, fh) in frames_layout:
        frame = make_rig_frame(src, (fw, fh), hue)
        sheet.paste(frame, (fx, fy))
    p = safe_quantize(sheet)
    p.save(out_path)
    print(f"  -> {out_path} ({max_x}x{max_y})")

print("=== Applying rig animations ===")

# 1. Battle throw animation: 16x16 single frame
make_sheet(justbekir_src, [(0,0,16,16)],
           f"{BASE}/graphics/battle_anims/sprites/pokeball.png")

# 2. Ball open sprite: 16x16
make_sheet(justbekir_src, [(0,0,16,16)],
           f"{BASE}/graphics/interface/ball_open.png")

# 3. Sliding pokeball (battle transition): 32x32
make_sheet(justbekir_src, [(0,0,32,32)],
           f"{BASE}/graphics/battle_transitions/sliding_pokeball.png")

# 4. Big pokeball (battle transition): 32x88 (multiple frames stacked)
frames = []
frame_h = 32
num = 88 // frame_h
for i in range(num):
    frames.append((0, i*frame_h, 32, frame_h))
# pad remaining
if 88 % frame_h != 0:
    frames.append((0, num*frame_h, 32, 88 % frame_h if 88 % frame_h >= 8 else 8))
make_sheet(justbekir_src, [(0,0,32,88)],
           f"{BASE}/graphics/battle_transitions/big_pokeball.png")

# 5. Party menu pokeball: 32x64 (2x16px frames)
make_sheet(justbekir_src, [(0,0,32,32),(0,32,32,32)],
           f"{BASE}/graphics/party_menu/pokeball.png")

# 6. Party menu small pokeball: 16x96 (6x16px frames)
frames6 = [(0, i*16, 16, 16) for i in range(6)]
make_sheet(justbekir_src, frames6,
           f"{BASE}/graphics/party_menu/pokeball_small.png")

# 7. Trade pokeball: 16x192 (12x16px animation frames)
frames12 = [(0, i*16, 16, 16) for i in range(12)]
make_sheet(justbekir_src, frames12,
           f"{BASE}/graphics/trade/pokeball.png")

# 8. Trade pokeball symbol: 64x104
make_sheet(justbekir_src, [(0,0,64,104)],
           f"{BASE}/graphics/trade/pokeball_symbol.png")

# 9. Pokeball glow: 8x8
make_sheet(justbekir_src, [(0,0,8,8)],
           f"{BASE}/graphics/field_effects/pics/pokeball_glow.png")

# 10. Fame checker spinning pokeball: 32x32
make_sheet(justbekir_src, [(0,0,32,32)],
           f"{BASE}/graphics/fame_checker/spinning_pokeball.png")

# 11. Credits pokeball
img_cred = make_rig_frame(justbekir_src, (32, 32))
pq = safe_quantize(img_cred)
cred_path = f"{BASE}/graphics/credits/pokeball.png"
if os.path.exists(cred_path):
    pq.save(cred_path)
    print(f"  -> {cred_path}")

# 12. Item icons (24x24 each)
icon_dir = f"{BASE}/graphics/items/icons"
icon_balls = {
    "master_ball.png": (justbekir_src, 0),
    "ultra_ball.png":  (ultra_src, 0),
    "great_ball.png":  (ultra_src, 240),
    "poke_ball.png":   (ultra_src, 0),
    "safari_ball.png": (ultra_src, 30),
    "net_ball.png":    (ultra_src, 120),
    "dive_ball.png":   (ultra_src, 200),
    "nest_ball.png":   (ultra_src, 270),
    "repeat_ball.png": (ultra_src, 15),
    "timer_ball.png":  (ultra_src, 180),
    "luxury_ball.png": (ultra_src, 300),
    "premier_ball.png":(ultra_src, 0),
}
for fname, (src, hue) in icon_balls.items():
    out = os.path.join(icon_dir, fname)
    if os.path.exists(out) and src:
        frame = make_rig_frame(src, (24, 24), hue)
        p = safe_quantize(frame)
        p.save(out)
        print(f"  -> {out}")

print("\nAll animation sprites updated!")
