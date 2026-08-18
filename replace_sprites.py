import os
import re
import random
from PIL import Image, ImageDraw

def generate_gpu_names(count):
    prefixes = ['RTX', 'GTX', 'RX', 'MI', 'TPU', 'LPU', 'A', 'H', 'B', 'PRO']
    suffixes = ['00', '0', 'X', 'M', 'Ti', 'XT', 'XTX', 'G', 'e']
    
    names = []
    # Add some predefined icons
    predefined = ["Voodoo5", "Titan", "Quadro", "H100", "A100", "B200", "MI300X", "TPUv4", "TPUv5", "LPU", "RTX4090", "RX7900", "RTX5090", "GTX1080", "GTX970", "RTX3080", "RTX2080", "ArcA770", "ArcA750", "Gaudi3"]
    for p in predefined:
        names.append(p[:10].upper())
        
    while len(names) < count:
        pref = random.choice(prefixes)
        num = str(random.randint(1, 9)) + random.choice(['00', '000', '090', '080', '070', '060', '050'])
        suf = random.choice(suffixes) if random.random() > 0.5 else ""
        name = f"{pref} {num}{suf}"
        name = name.replace(" ", "")
        if len(name) > 10:
            name = name[:10]
        if name.upper() not in names:
            names.append(name.upper())
            
    return names[:count]

def replace_species_names():
    filepath = '/Users/bekirkarakose/Documents/ProjectAlascatra/src/data/text/species_names.h'
    with open(filepath, 'r') as f:
        content = f.read()
        
    pattern = r'(\[SPECIES_[A-Z0-9_]+\] = _\(")(.*?)("\),?)'
    matches = list(re.finditer(pattern, content))
    
    gpu_names = generate_gpu_names(len(matches))
    
    new_content = content
    for idx, match in enumerate(matches):
        if 'SPECIES_NONE' in match.group(1):
            continue
        old_full = match.group(0)
        new_full = f'{match.group(1)}{gpu_names[idx]}{match.group(3)}'
        new_content = new_content.replace(old_full, new_full, 1)
        
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return gpu_names

def generate_pixel_art(name, size=(64, 64)):
    img = Image.new('P', size, color=0)
    
    # Create 16-color palette
    palette = [0, 0, 0] * 256
    
    # 0: Transparent (bg) -> light green in pal but 0 in image
    palette[0:3] = [205, 205, 172] # Transparent color convention in GBA
    
    # Black outline
    palette[3:6] = [10, 10, 10]
    
    # PCB Color (Green, Blue, Black, Red)
    pcb_colors = [[10, 120, 10], [10, 10, 120], [30, 30, 30], [120, 10, 10]]
    pcb_col = random.choice(pcb_colors)
    palette[6:9] = pcb_col
    
    # Chip color
    palette[9:12] = [60, 60, 60]
    
    # Text/Highlight color
    palette[12:15] = [200, 200, 200]
    
    # Fan / Heatsink color
    palette[15:18] = [100, 100, 100]
    
    img.putpalette(palette)
    
    draw = ImageDraw.Draw(img)
    
    # Draw PCB
    w, h = size
    margin = w // 8
    if margin == 0:
        margin = 1
    
    draw.rectangle([margin, margin, w - margin, h - int(margin*1.5)], fill=2, outline=1)
    
    # Draw Chip / Fan
    is_headless = random.random() > 0.5
    if is_headless:
        # Draw a big die (AI accelerator)
        draw.rectangle([margin*2, margin*2, w - margin*2, h - margin*3], fill=3, outline=1)
        if w > 16:
            draw.rectangle([margin*3, margin*3, w - margin*3, h - margin*4], fill=4, outline=1)
    else:
        # Draw fans (Consumer GPU)
        draw.ellipse([margin*1.5, margin*2, w//2 - margin*0.5, h - margin*2.5], fill=5, outline=1)
        draw.ellipse([w//2 + margin*0.5, margin*2, w - margin*1.5, h - margin*2.5], fill=5, outline=1)
        
    # Draw PCIe slot
    draw.rectangle([w//3, h - int(margin*1.5), w - w//3, h - int(margin*0.5)], fill=4, outline=1)
    
    return img, palette

def write_jasc_pal(filepath, palette, is_shiny=False):
    with open(filepath, 'w') as f:
        f.write("JASC-PAL\n0100\n16\n")
        for i in range(16):
            r = palette[i*3]
            g = palette[i*3+1]
            b = palette[i*3+2]
            if is_shiny and i == 2: # Invert PCB color for shiny
                r, g, b = (255-r), (255-g), (255-b)
            f.write(f"{r} {g} {b}\n")

def process_graphics():
    base_dir = '/Users/bekirkarakose/Documents/ProjectAlascatra/graphics/pokemon'
    if not os.path.exists(base_dir):
        return
    
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        
        # skip icon_palettes or other non-pokemon folders if they don't have front.png
        if folder == 'icon_palettes':
            continue
            
        front, pal = generate_pixel_art(folder, (64, 64))
        back, _ = generate_pixel_art(folder, (64, 64))
        icon, _ = generate_pixel_art(folder, (32, 32)) 
        
        icon = icon.resize((32, 64)) 
        
        front.save(os.path.join(folder_path, 'front.png'))
        back.save(os.path.join(folder_path, 'back.png'))
        
        # some folders might not have icon.png (e.g. egg), but we can just overwrite
        icon.save(os.path.join(folder_path, 'icon.png'))
        
        # footprint 16x16
        footprint, _ = generate_pixel_art(folder, (16, 16))
        footprint.save(os.path.join(folder_path, 'footprint.png'))
        
        write_jasc_pal(os.path.join(folder_path, 'normal.pal'), pal, is_shiny=False)
        write_jasc_pal(os.path.join(folder_path, 'shiny.pal'), pal, is_shiny=True)

if __name__ == '__main__':
    print("Replacing species names...")
    names = replace_species_names()
    print(f"Replaced names with {len(names)} GPUs.")
    
    print("Generating pixel art GPUs...")
    process_graphics()
    print("Done!")
