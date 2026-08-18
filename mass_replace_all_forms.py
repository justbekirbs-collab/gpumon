import os
from PIL import Image

BASE = "/Users/bekirkarakose/Documents/ProjectAlascatra"
BRAIN_DIR = "/Users/bekirkarakose/.gemini/antigravity-ide/brain/9278a478-ffc5-40b2-acf9-aa13454eaadd"

front_images = [
    os.path.join(BRAIN_DIR, "consumer_gpu_front_1787044168280.jpg"),
    os.path.join(BRAIN_DIR, "blackwell_front_1787044149120.jpg"),
    os.path.join(BRAIN_DIR, "gpu_base_pixel_art_1787039353747.jpg"),
    os.path.join(BRAIN_DIR, "gpu_datacenter_base_1787039373514.jpg"),
    os.path.join(BRAIN_DIR, "basic_rig_icon_1787054862910.jpg"),
    os.path.join(BRAIN_DIR, "justbekir_rig_rgb_1787054838025.jpg")
]
back_images = [
    os.path.join(BRAIN_DIR, "consumer_gpu_back_1787044176360.jpg"),
    os.path.join(BRAIN_DIR, "blackwell_back_1787044160348.jpg"),
    os.path.join(BRAIN_DIR, "gpu_base_pixel_art_1787039353747.jpg"),
    os.path.join(BRAIN_DIR, "gpu_datacenter_base_1787039373514.jpg"),
    os.path.join(BRAIN_DIR, "basic_rig_icon_1787054862910.jpg"),
    os.path.join(BRAIN_DIR, "justbekir_rig_rgb_1787054838025.jpg")
]

icon_src = None
for f in os.listdir(BRAIN_DIR):
    if f.startswith("party_gpu_icon_"):
        icon_src = os.path.join(BRAIN_DIR, f)
        break

def create_sprite(src_path, size):
    img = Image.open(src_path).convert("RGB")
    img = img.resize(size, Image.LANCZOS)
    p = img.convert("P", palette=Image.ADAPTIVE, colors=15)
    pal = p.getpalette()
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
        for y in range(size[1]):
            for x in range(size[0]):
                v = px[x, y]
                if v == bg_idx: px[x, y] = 0
                elif v == 0: px[x, y] = bg_idx
    return p

front_sprites = [create_sprite(f, (64, 64)) for f in front_images]
back_sprites = [create_sprite(f, (64, 64)) for f in back_images]

# For icons (32x64)
img = Image.open(icon_src).convert("RGB")
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
p_icon = sheet.convert("P", palette=Image.ADAPTIVE, colors=15)
pal = p_icon.getpalette()
while len(pal) < 48: pal.append(0)
bg_idx = -1
for i in range(16):
    r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
    if r > 240 and g < 10 and b > 240:
        bg_idx = i; break
if bg_idx == -1:
    pal[0:3] = [255, 0, 255]
    p_icon.putpalette(pal)
elif bg_idx != 0:
    pal[0:3], pal[bg_idx*3:bg_idx*3+3] = pal[bg_idx*3:bg_idx*3+3], pal[0:3]
    p_icon.putpalette(pal)
    px = p_icon.load()
    for y in range(64):
        for x in range(32):
            v = px[x, y]
            if v == bg_idx: px[x, y] = 0
            elif v == 0: px[x, y] = bg_idx

poke_dir = os.path.join(BASE, "graphics/pokemon")
count_sprites = 0
count_icons = 0

for root, dirs, files in os.walk(poke_dir):
    for fname in files:
        if not fname.endswith(".png"): continue
        if fname.startswith("front"):
            # Randomly select a front sprite based on the hash of the directory so it's consistent
            idx = hash(root) % len(front_sprites)
            front_sprites[idx].save(os.path.join(root, fname))
            count_sprites += 1
        elif fname.startswith("back"):
            idx = hash(root) % len(back_sprites)
            back_sprites[idx].save(os.path.join(root, fname))
            count_sprites += 1
        elif fname.startswith("icon"):
            p_icon.save(os.path.join(root, fname))
            count_icons += 1

print(f"Replaced {count_sprites} front/back sprites and {count_icons} icons recursively!")
