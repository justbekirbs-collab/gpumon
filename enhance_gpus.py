import os
import re
import random
from PIL import Image, ImageEnhance, ImageOps
import glob
import numpy as np
from pathlib import Path

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'

def get_tier(name):
    name = name.upper()
    if 'BLACKWELL' in name or 'B200' in name or 'H100' in name or 'A100' in name:
        return 5 # Legendary
    if '5090' in name or '4090' in name or 'MI300' in name or 'TPUV5' in name or 'LPU' in name:
        return 4 # Ultra High End
    if '4080' in name or '3090' in name or '7900' in name or 'TPUV4' in name:
        return 3 # High End
    if '3080' in name or '4070' in name or '7800' in name or 'TITAN' in name:
        return 2 # Mid-High
    if '2080' in name or '3060' in name or '1080' in name or 'QUADRO' in name or 'ARCA' in name:
        return 1 # Mid
    return 0 # Low / Old

def get_stats_for_tier(tier):
    if tier == 5:
        return 130, 150, 120, 150, 120, 130, 3 # 800 BST, 3 catch rate (Legendary)
    if tier == 4:
        return 100, 130, 100, 130, 100, 110, 45
    if tier == 3:
        return 90, 110, 90, 110, 90, 100, 60
    if tier == 2:
        return 80, 95, 80, 95, 80, 90, 90
    if tier == 1:
        return 70, 80, 70, 80, 70, 80, 120
    return 50, 50, 50, 50, 50, 50, 255 # Tier 0

def rgb_to_gba(r, g, b):
    r, g, b = r >> 3, g >> 3, b >> 3
    return r, g, b

def write_jasc_pal(filepath, palette, is_shiny=False):
    with open(filepath, 'w') as f:
        f.write("JASC-PAL\n0100\n16\n")
        # Color 0 is transparent bg (205, 205, 172 is convention for some tools, but actual color doesn't matter for transparent as long as it's index 0)
        f.write("205 205 172\n")
        
        for i in range(1, 16):
            r, g, b = palette[i*3:i*3+3]
            if is_shiny:
                # shift hues
                r, g, b = g, b, r
            f.write(f"{r} {g} {b}\n")

def process_image(src_path, dest_folder, is_legendary, hue_shift):
    img = Image.open(src_path).convert('RGBA')
    # Crop to center square
    w, h = img.size
    s = min(w, h)
    img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    
    # Convert RGBA to RGB with black bg where transparent just in case
    bg = Image.new('RGBA', img.size, (0, 0, 0, 255))
    img = Image.alpha_composite(bg, img).convert('RGB')
    
    # Convert to numpy and apply hue shift if not legendary
    if not is_legendary:
        arr = np.array(img.convert('HSV'))
        arr[:, :, 0] = (arr[:, :, 0] + hue_shift) % 256
        img = Image.fromarray(arr, 'HSV').convert('RGB')
    
    # We must replace true black/dark background with the transparent color for quantization
    # Let's say any pixel very dark is background
    arr = np.array(img)
    mask = (arr[:, :, 0] < 15) & (arr[:, :, 1] < 15) & (arr[:, :, 2] < 15)
    arr[mask] = [205, 205, 172] # the transparent color
    img = Image.fromarray(arr)

    # Quantize to 16 colors using Pillow
    img = img.quantize(colors=16, method=Image.Quantize.FASTOCTREE)
    
    pal = img.getpalette()[:48]
    
    # ensure color 0 is our transparent color
    # we can just write it as transparent in the pal file
    
    front_path = os.path.join(dest_folder, 'front.png')
    back_path = os.path.join(dest_folder, 'back.png')
    img.save(front_path)
    img.save(back_path)
    
    icon_img = img.resize((32, 32), Image.Resampling.LANCZOS).quantize(colors=16)
    icon_final = Image.new('P', (32, 64), color=0)
    icon_final.putpalette(icon_img.getpalette())
    icon_final.paste(icon_img, (0, 0))
    icon_final.save(os.path.join(dest_folder, 'icon.png'))
    
    write_jasc_pal(os.path.join(dest_folder, 'normal.pal'), pal, is_shiny=False)
    write_jasc_pal(os.path.join(dest_folder, 'shiny.pal'), pal, is_shiny=True)

def main():
    # 1. Parse species names
    print("Parsing species names...")
    species_names_file = os.path.join(BASE_DIR, 'src/data/text/species_names.h')
    with open(species_names_file, 'r') as f:
        content = f.read()
    
    pattern = r'\[SPECIES_([A-Z0-9_]+)\] = _\("([^"]+)"\)'
    matches = re.findall(pattern, content)
    
    species_map = {}
    original_to_gpu = {}
    for original_species, gpu_name in matches:
        if original_species == 'NONE': continue
        tier = get_tier(gpu_name)
        species_map[original_species] = {'gpu_name': gpu_name, 'tier': tier}
        original_to_gpu[original_species] = gpu_name

    # 2. Update base stats
    print("Updating base stats...")
    base_stats_file = os.path.join(BASE_DIR, 'src/data/pokemon/species_info.h')
    with open(base_stats_file, 'r') as f:
        lines = f.readlines()
        
    in_species = None
    new_lines = []
    for line in lines:
        match = re.search(r'\[SPECIES_([A-Z0-9_]+)\]', line)
        if match:
            in_species = match.group(1)
            
        if in_species and in_species in species_map:
            t = species_map[in_species]['tier']
            hp, atk, df, satk, sdf, spd, catch = get_stats_for_tier(t)
            
            if '.baseHP' in line: line = re.sub(r'= \d+', f'= {hp}', line)
            elif '.baseAttack' in line: line = re.sub(r'= \d+', f'= {atk}', line)
            elif '.baseDefense' in line: line = re.sub(r'= \d+', f'= {df}', line)
            elif '.baseSpAttack' in line: line = re.sub(r'= \d+', f'= {satk}', line)
            elif '.baseSpDefense' in line: line = re.sub(r'= \d+', f'= {sdf}', line)
            elif '.baseSpeed' in line: line = re.sub(r'= \d+', f'= {spd}', line)
            elif '.catchRate' in line: line = re.sub(r'= \d+', f'= {catch}', line)
            
        new_lines.append(line)
        
    with open(base_stats_file, 'w') as f:
        f.writelines(new_lines)

    # 3. Process Images
    print("Processing images...")
    consumer_img = glob.glob(os.path.join(os.path.dirname(BASE_DIR), '.gemini', '**', 'gpu_base_pixel_art*.jpg'), recursive=True)
    datacenter_img = glob.glob(os.path.join(os.path.dirname(BASE_DIR), '.gemini', '**', 'gpu_datacenter_base*.jpg'), recursive=True)
    
    consumer_path = consumer_img[0] if consumer_img else None
    datacenter_path = datacenter_img[0] if datacenter_img else None
    
    if consumer_path and datacenter_path:
        for original_species, data in species_map.items():
            is_legendary = data['tier'] >= 4
            src_img = datacenter_path if is_legendary else consumer_path
            hue_shift = random.randint(0, 255)
            
            # map original species to lowercase folder
            folder_name = original_species.lower()
            if folder_name == 'nidoran_f': folder_name = 'nidoran_f'
            elif folder_name == 'nidoran_m': folder_name = 'nidoran_m'
            elif folder_name == 'ho_oh': folder_name = 'ho_oh'
            elif folder_name == 'mr_mime': folder_name = 'mr_mime'
            
            dest = os.path.join(BASE_DIR, 'graphics/pokemon', folder_name)
            if os.path.exists(dest):
                try:
                    process_image(src_img, dest, is_legendary, hue_shift)
                except Exception as e:
                    print(f"Failed image for {folder_name}: {e}")
                    
    # 4. Global Text Replacements
    print("Replacing texts...")
    for ext in ['**/*.inc', '**/*.json']:
        for filepath in Path(os.path.join(BASE_DIR, 'data')).rglob(ext):
            with open(filepath, 'r') as f:
                content = f.read()
            changed = False
            for old_sp, new_sp in original_to_gpu.items():
                if old_sp in content:
                    content = content.replace(old_sp, new_sp)
                    changed = True
            if changed:
                with open(filepath, 'w') as f:
                    f.write(content)

    # 5. Move Names
    print("Updating move names...")
    move_names_file = os.path.join(BASE_DIR, 'src/data/text/move_names.h')
    with open(move_names_file, 'r') as f:
        content = f.read()
        
    gpu_moves = ['OVERCLOCK', 'BITCOIN MINE', 'TRAIN AI', 'RAY TRACING', 'FRAME GEN', 'TENSOR SMASH', 'WATER COOL', 'LIQUID METAL', 'THERMAL THROTTLE', 'BLUE SCREEN', 'DRIVER CRASH', 'RGB BLAZE', 'DLSS 3', 'FSR 2', 'HASH CRACK', 'VRAM OVERFLOW']
    
    def repl_move(match):
        orig_move = match.group(1)
        if 'MOVE_NONE' in orig_move: return match.group(0)
        new_name = random.choice(gpu_moves)
        return f'{orig_move} = _("{new_name}"),'
        
    new_content = re.sub(r'(\[MOVE_[A-Z0-9_]+\])\s*= _\("[^"]+"\),', repl_move, content)
    with open(move_names_file, 'w') as f:
        f.write(new_content)
        
    print("Enhancements complete!")

if __name__ == '__main__':
    main()
