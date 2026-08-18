import os
from PIL import Image

BRAIN_DIR = "/Users/bekirkarakose/.gemini/antigravity-ide/brain/9278a478-ffc5-40b2-acf9-aa13454eaadd"
BALL_DIR = "/Users/bekirkarakose/Documents/ProjectAlascatra/graphics/interface/ball"

# Find our generated images
justbekir_img = None
ultra_img = None
great_img = None
basic_img = None

for f in os.listdir(BRAIN_DIR):
    if f.startswith("justbekir_rig_rgb_"): justbekir_img = os.path.join(BRAIN_DIR, f)
    elif f.startswith("ultra_rig_icon_"): ultra_img = os.path.join(BRAIN_DIR, f)
    elif f.startswith("great_rig_icon_"): great_img = os.path.join(BRAIN_DIR, f)
    elif f.startswith("basic_rig_icon_"): basic_img = os.path.join(BRAIN_DIR, f)

print(f"JustBekir RGB: {justbekir_img}")
print(f"Ultra: {ultra_img}")
print(f"Great: {great_img}")
print(f"Basic: {basic_img}")

BG_COLOR = (255, 0, 255)

def make_rig_sprite(src_path, out_path, is_rgb=False):
    """Convert AI image to 16x48 (3-frame) GBA sprite sheet"""
    src = Image.open(src_path).convert("RGB")
    
    # Create 16x48 sprite sheet (3 frames of 16x16 each)
    sheet = Image.new("RGB", (16, 48), BG_COLOR)
    
    # Each frame: resize source to 16x16
    frame = src.resize((16, 16), Image.LANCZOS)
    frame_pixels = frame.load()
    
    # Replace near-white with BG (transparent)
    for y in range(16):
        for x in range(16):
            r, g, b = frame_pixels[x, y]
            if r > 230 and g > 230 and b > 230:
                frame_pixels[x, y] = BG_COLOR
    
    # Paste same frame 3 times (GBA uses frame 0 for normal, 1/2 for animation)
    sheet.paste(frame, (0, 0))
    sheet.paste(frame, (0, 16))
    sheet.paste(frame, (0, 32))
    
    # Quantize to exactly 16 colors (GBA palette limit)
    sheet_p = sheet.convert("P", palette=Image.ADAPTIVE, colors=15)  # 15 + transparent
    pal = sheet_p.getpalette()
    
    # Force BG color to be palette index 0 (GBA transparency convention)
    bg_idx = -1
    for i in range(16):
        r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
        dist = abs(r-255) + abs(g-0) + abs(b-255)
        if dist < 60:
            bg_idx = i
            break
    
    # Insert BG at idx 0
    if bg_idx == -1:
        # Force slot 0 to be BG
        pal[0], pal[1], pal[2] = 255, 0, 255
        sheet_p.putpalette(pal)
    elif bg_idx != 0:
        # Swap with idx 0
        pal[0], pal[1], pal[2], pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2] = \
            pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2], pal[0], pal[1], pal[2]
        sheet_p.putpalette(pal)
        # Update pixel indices
        px = sheet_p.load()
        for y in range(48):
            for x in range(16):
                v = px[x, y]
                if v == bg_idx: px[x, y] = 0
                elif v == 0: px[x, y] = bg_idx
    
    sheet_p.save(out_path)
    print(f"  Saved: {out_path}")

# Map: (output_filename, source_image, is_rgb)
sprite_map = [
    ("master.png", justbekir_img, True),
    ("ultra.png",  ultra_img, False),
    ("great.png",  great_img, False),
    ("poke.png",   basic_img, False),
]

# For remaining balls, use great_rig with different hues
def hue_shift_img(src_path, hue_deg):
    """Return PIL image with hue shifted"""
    img = Image.open(src_path).convert("RGB")
    img = img.resize((16, 16), Image.LANCZOS)
    px = img.load()
    for y in range(16):
        for x in range(16):
            r, g, b = px[x, y]
            if r > 230 and g > 230 and b > 230:
                px[x, y] = (255, 0, 255)
                continue
            # Simple hue rotate
            import colorsys
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + hue_deg/360.0) % 1.0
            rn, gn, bn = colorsys.hsv_to_rgb(h, s, v)
            px[x, y] = (int(rn*255), int(gn*255), int(bn*255))
    return img

def make_hued_rig_sprite(src_path, out_path, hue_deg):
    frame = hue_shift_img(src_path, hue_deg)
    sheet = Image.new("RGB", (16, 48), (255, 0, 255))
    sheet.paste(frame, (0, 0))
    sheet.paste(frame, (0, 16))
    sheet.paste(frame, (0, 32))
    sheet_p = sheet.convert("P", palette=Image.ADAPTIVE, colors=15)
    pal = sheet_p.getpalette()
    pal[0], pal[1], pal[2] = 255, 0, 255
    sheet_p.putpalette(pal)
    sheet_p.save(out_path)
    print(f"  Saved (hued): {out_path}")

print("\n=== Converting AI images to GBA rig sprites ===")
for fname, src, is_rgb in sprite_map:
    if src:
        out = os.path.join(BALL_DIR, fname)
        make_rig_sprite(src, out, is_rgb)
    else:
        print(f"  SKIP {fname} - source not found")

# Other rigs get hue-shifted versions of Ultra Rig
others = [
    ("safari.png",  ultra_img, 30),
    ("net.png",     ultra_img, 120),
    ("dive.png",    ultra_img, 200),
    ("nest.png",    ultra_img, 270),
    ("repeat.png",  ultra_img, 15),
    ("timer.png",   ultra_img, 180),
    ("luxury.png",  ultra_img, 300),
    ("premier.png", ultra_img, 0),
]
for fname, src, hue in others:
    if src:
        out = os.path.join(BALL_DIR, fname)
        make_hued_rig_sprite(src, out, hue)

print("\nAll rig sprites applied!")
