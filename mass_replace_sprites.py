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

poke_dir = os.path.join(BASE, "graphics/pokemon")
species_dirs = sorted([d for d in os.listdir(poke_dir) if os.path.isdir(os.path.join(poke_dir, d))])

count = 0
for i, d in enumerate(species_dirs):
    folder = os.path.join(poke_dir, d)
    if not os.path.exists(os.path.join(folder, "front.png")):
        continue
    
    f_img = front_sprites[i % len(front_sprites)]
    b_img = back_sprites[i % len(back_sprites)]
    
    f_img.save(os.path.join(folder, "front.png"))
    b_img.save(os.path.join(folder, "back.png"))
    
    # Generate palettes
    for pal_file in ["normal.pal", "shiny.pal"]:
        pal_path = os.path.join(folder, pal_file)
        if os.path.exists(pal_path):
            with open(pal_path, "w") as pf:
                pf.write("JASC-PAL\n0100\n16\n")
                pal = f_img.getpalette()
                for c in range(16):
                    r, g, b = pal[c*3], pal[c*3+1], pal[c*3+2]
                    pf.write(f"{r} {g} {b}\n")
    count += 1

print(f"Replaced ALL {count} pokemon sprites with GPUs!")
