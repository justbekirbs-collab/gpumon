import os
import random
from PIL import Image

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'
GRAPHICS_DIR = os.path.join(BASE_DIR, 'graphics/pokemon')

BG_COLOR = (255, 0, 255)

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn: h = 0
    elif mx == r: h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g: h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b: h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0: s = 0
    else: s = (df/mx)*100
    v = mx*100
    return h, s, v

def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = int(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def process_image(src_path, out_path, hue_shift=0):
    img = Image.open(src_path).convert("RGB")
    # Resize high quality
    img = img.resize((64, 64), Image.LANCZOS)
    
    pixels = img.load()
    for y in range(64):
        for x in range(64):
            r, g, b = pixels[x, y]
            # Replace white background with magenta
            if r > 235 and g > 235 and b > 235:
                pixels[x, y] = BG_COLOR
            else:
                if hue_shift != 0:
                    h, s, v = rgb_to_hsv(r, g, b)
                    h = (h + hue_shift) % 360
                    # For non-grey pixels
                    if s > 15:
                        s = s / 100.0
                        v = v / 100.0
                        pixels[x, y] = hsv_to_rgb(h, s, v)

    # Quantize to 16 colors
    img = img.convert("P", palette=Image.ADAPTIVE, colors=16)
    pal = img.getpalette()
    
    bg_idx = -1
    for i in range(16):
        r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
        if (r, g, b) == BG_COLOR:
            bg_idx = i
            break
            
    if bg_idx == -1:
        pal[0], pal[1], pal[2] = BG_COLOR
        img.putpalette(pal)
    elif bg_idx != 0:
        pal[0], pal[1], pal[2], pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2] = \
            pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2], pal[0], pal[1], pal[2]
        img.putpalette(pal)
        
        px = img.load()
        for y in range(64):
            for x in range(64):
                if px[x, y] == bg_idx:
                    px[x, y] = 0
                elif px[x, y] == 0:
                    px[x, y] = bg_idx

    img.save(out_path)

# Look for our generated AI images in the brain folder
BRAIN_DIR = "/Users/bekirkarakose/.gemini/antigravity-ide/brain/9278a478-ffc5-40b2-acf9-aa13454eaadd"
blackwell_f = None
blackwell_b = None
consumer_f = None
consumer_b = None

for f in os.listdir(BRAIN_DIR):
    if f.startswith("blackwell_front_") and f.endswith(".jpg"): blackwell_f = os.path.join(BRAIN_DIR, f)
    if f.startswith("blackwell_back_") and f.endswith(".jpg"): blackwell_b = os.path.join(BRAIN_DIR, f)
    if f.startswith("consumer_gpu_front_") and f.endswith(".jpg"): consumer_f = os.path.join(BRAIN_DIR, f)
    if f.startswith("consumer_gpu_back_") and f.endswith(".jpg"): consumer_b = os.path.join(BRAIN_DIR, f)

special_map = ['mewtwo', 'ho_oh', 'lugia', 'rayquaza', 'deoxys', 'groudon']

count = 0
for folder in os.listdir(GRAPHICS_DIR):
    folder_path = os.path.join(GRAPHICS_DIR, folder)
    if os.path.isdir(folder_path):
        
        front = os.path.join(folder_path, 'front.png')
        back = os.path.join(folder_path, 'back.png')
        
        if folder in special_map:
            # Shift hue slightly for each legendary to make them distinct
            hue = (special_map.index(folder) * 60)
            if os.path.exists(front) and blackwell_f: process_image(blackwell_f, front, hue)
            if os.path.exists(back) and blackwell_b: process_image(blackwell_b, back, hue)
        else:
            h = sum(ord(c) for c in folder)
            hue = h % 360
            if os.path.exists(front) and consumer_f: process_image(consumer_f, front, hue)
            if os.path.exists(back) and consumer_b: process_image(consumer_b, back, hue)
            
        count += 1
        
print(f"Applied AI pixel arts to {count} GPUs.")
