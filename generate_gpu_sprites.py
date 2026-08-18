import os
import random
from PIL import Image, ImageDraw

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'
GRAPHICS_DIR = os.path.join(BASE_DIR, 'graphics/pokemon')

BG_COLOR = (255, 0, 255) # Magenta for transparency
OUTLINE_COLOR = (0, 0, 0) # Black outline

def enforce_transparency(img, bg_color):
    """Ensures the background color is at index 0 of the 16-color palette."""
    img = img.convert("P", palette=Image.ADAPTIVE, colors=16)
    pal = img.getpalette()
    
    # Find the index of the background color
    bg_idx = -1
    for i in range(16):
        r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
        if (r, g, b) == bg_color:
            bg_idx = i
            break
            
    if bg_idx == -1:
        # Bg color got lost in quantization, force it to index 0
        pal[0], pal[1], pal[2] = bg_color
        img.putpalette(pal)
        return img
        
    if bg_idx != 0:
        # Swap bg_idx with 0 in palette
        pal[0], pal[1], pal[2], pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2] = \
            pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2], pal[0], pal[1], pal[2]
        img.putpalette(pal)
        
        # Swap pixel data
        px = img.load()
        for y in range(img.height):
            for x in range(img.width):
                if px[x, y] == bg_idx:
                    px[x, y] = 0
                elif px[x, y] == 0:
                    px[x, y] = bg_idx
                    
    return img

def draw_consumer_gpu(draw, primary_color, secondary_color):
    # Main shroud
    draw.rectangle([10, 15, 54, 45], fill=primary_color, outline=OUTLINE_COLOR)
    # PCIe
    draw.rectangle([20, 45, 44, 49], fill=(218, 165, 32), outline=OUTLINE_COLOR)
    # Fans
    draw.ellipse([12, 17, 30, 35], fill=secondary_color, outline=OUTLINE_COLOR)
    draw.ellipse([34, 17, 52, 35], fill=secondary_color, outline=OUTLINE_COLOR)
    # Fan hubs
    draw.ellipse([19, 24, 23, 28], fill=(50, 50, 50))
    draw.ellipse([41, 24, 45, 28], fill=(50, 50, 50))
    # Accents
    draw.line([10, 40, 54, 40], fill=(200, 200, 200), width=1)

def draw_datacenter_gpu(draw, primary_color, secondary_color):
    # PCB
    draw.rectangle([12, 10, 52, 50], fill=primary_color, outline=OUTLINE_COLOR)
    # PCIe
    draw.rectangle([22, 50, 42, 54], fill=(218, 165, 32), outline=OUTLINE_COLOR)
    # Huge Heatsink
    draw.rectangle([16, 14, 48, 46], fill=secondary_color, outline=OUTLINE_COLOR)
    # Heatsink fins
    for i in range(18, 48, 4):
        draw.line([i, 14, i, 46], fill=(50, 50, 50), width=1)

def draw_retro_gpu(draw, primary_color, secondary_color):
    # Small PCB
    draw.rectangle([16, 20, 48, 44], fill=primary_color, outline=OUTLINE_COLOR)
    # PCIe
    draw.rectangle([24, 44, 40, 48], fill=(218, 165, 32), outline=OUTLINE_COLOR)
    # Single small fan
    draw.ellipse([24, 24, 40, 40], fill=secondary_color, outline=OUTLINE_COLOR)
    # Chips
    draw.rectangle([18, 22, 22, 26], fill=(30, 30, 30))
    draw.rectangle([42, 22, 46, 26], fill=(30, 30, 30))

def draw_special_gpu(draw, name):
    if name == "BLACKWELL":
        # Massive gold/black AI chip
        draw.rectangle([8, 8, 56, 52], fill=(20, 20, 20), outline=OUTLINE_COLOR) # Black board
        draw.rectangle([14, 14, 50, 46], fill=(255, 215, 0), outline=OUTLINE_COLOR) # Gold core
        draw.rectangle([22, 22, 42, 38], fill=(10, 10, 10), outline=OUTLINE_COLOR) # Inner die
        draw.rectangle([26, 48, 38, 56], fill=(218, 165, 32), outline=OUTLINE_COLOR) # PCIe
    elif name == "H100":
        # Green PCB, silver heatsink
        draw_datacenter_gpu(draw, (34, 139, 34), (192, 192, 192))
        draw.rectangle([30, 28, 34, 32], fill=(0, 255, 0)) # Green glowing light
    elif name == "A100":
        # Orange/bronze trim
        draw_datacenter_gpu(draw, (205, 127, 50), (105, 105, 105))
    elif name == "MI300X":
        # Red/Black AMD
        draw_consumer_gpu(draw, (30, 30, 30), (220, 20, 60))
    elif name == "TPU v5e":
        # White/Blue Google
        draw_datacenter_gpu(draw, (240, 240, 240), (65, 105, 225))
    elif name == "GAUDI 3":
        # Purple/Black Intel
        draw_datacenter_gpu(draw, (10, 10, 10), (128, 0, 128))

def create_sprite(path, name, is_back=False, shiny=False):
    img = Image.new("RGB", (64, 64), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    if name in ["BLACKWELL", "H100", "A100", "MI300X", "TPU v5e", "GAUDI 3"]:
        draw_special_gpu(draw, name)
    else:
        # Determine random template based on hash of name
        h = sum(ord(c) for c in name)
        template = h % 3
        
        # Determine random colors
        random.seed(h + (1 if shiny else 0))
        pc = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        sc = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        
        if template == 0:
            draw_consumer_gpu(draw, pc, sc)
        elif template == 1:
            draw_datacenter_gpu(draw, pc, sc)
        else:
            draw_retro_gpu(draw, pc, sc)

    # Convert to indexed with enforced background
    final_img = enforce_transparency(img, BG_COLOR)
    final_img.save(path)

# 150 = BLACKWELL (Mewtwo)
# 250 = H100 (Ho-Oh)
# 249 = A100 (Lugia)
# 384 = MI300X (Rayquaza)
# 386 = TPU v5e (Deoxys)
# 383 = GAUDI 3 (Groudon)

special_map = {
    'mewtwo': 'BLACKWELL',
    'ho_oh': 'H100',
    'lugia': 'A100',
    'rayquaza': 'MI300X',
    'deoxys': 'TPU v5e',
    'groudon': 'GAUDI 3'
}

count = 0
for folder in os.listdir(GRAPHICS_DIR):
    folder_path = os.path.join(GRAPHICS_DIR, folder)
    if os.path.isdir(folder_path):
        name = special_map.get(folder, folder.upper())
        
        front = os.path.join(folder_path, 'front.png')
        back = os.path.join(folder_path, 'back.png')
        
        if os.path.exists(front):
            create_sprite(front, name, False, False)
        if os.path.exists(back):
            create_sprite(back, name, True, False)
            
        count += 1
        
print(f"Generated {count} GPU sprites.")
