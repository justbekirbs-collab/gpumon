import os
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
    return int(r * 255), int(g * 255), int(b * 255)

def process_image(src_path, out_path, target_height, hue_shift=0):
    # Process the base 64x64 frame
    base_img = Image.open(src_path).convert("RGB")
    base_img = base_img.resize((64, 64), Image.LANCZOS)
    
    pixels = base_img.load()
    for y in range(64):
        for x in range(64):
            r, g, b = pixels[x, y]
            if r > 235 and g > 235 and b > 235:
                pixels[x, y] = BG_COLOR
            else:
                if hue_shift != 0:
                    h, s, v = rgb_to_hsv(r, g, b)
                    h = (h + hue_shift) % 360
                    if s > 15:
                        s = s / 100.0
                        v = v / 100.0
                        pixels[x, y] = hsv_to_rgb(h, s, v)

    # If the target height is more than 64 (sprite sheet), tile the base frame
    num_frames = target_height // 64
    final_img = Image.new("RGB", (64, target_height), BG_COLOR)
    for i in range(num_frames):
        final_img.paste(base_img, (0, i * 64))

    # Quantize to 16 colors
    final_img = final_img.convert("P", palette=Image.ADAPTIVE, colors=16)
    pal = final_img.getpalette()
    
    bg_idx = -1
    for i in range(16):
        r, g, b = pal[i*3], pal[i*3+1], pal[i*3+2]
        if (r, g, b) == BG_COLOR:
            bg_idx = i
            break
            
    if bg_idx == -1:
        pal[0], pal[1], pal[2] = BG_COLOR
        final_img.putpalette(pal)
    elif bg_idx != 0:
        pal[0], pal[1], pal[2], pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2] = \
            pal[bg_idx*3], pal[bg_idx*3+1], pal[bg_idx*3+2], pal[0], pal[1], pal[2]
        final_img.putpalette(pal)
        
        px = final_img.load()
        for y in range(target_height):
            for x in range(64):
                if px[x, y] == bg_idx:
                    px[x, y] = 0
                elif px[x, y] == 0:
                    px[x, y] = bg_idx

    final_img.save(out_path)

BRAIN_DIR = "/Users/bekirkarakose/.gemini/antigravity-ide/brain/9278a478-ffc5-40b2-acf9-aa13454eaadd"
blackwell_f = os.path.join(BRAIN_DIR, [f for f in os.listdir(BRAIN_DIR) if f.startswith("blackwell_front")][0])
blackwell_b = os.path.join(BRAIN_DIR, [f for f in os.listdir(BRAIN_DIR) if f.startswith("blackwell_back")][0])
consumer_f = os.path.join(BRAIN_DIR, [f for f in os.listdir(BRAIN_DIR) if f.startswith("consumer_gpu_front")][0])
consumer_b = os.path.join(BRAIN_DIR, [f for f in os.listdir(BRAIN_DIR) if f.startswith("consumer_gpu_back")][0])

special_map = ['mewtwo', 'ho_oh', 'lugia', 'rayquaza', 'deoxys', 'groudon']

for folder in os.listdir(GRAPHICS_DIR):
    folder_path = os.path.join(GRAPHICS_DIR, folder)
    if os.path.isdir(folder_path):
        front = os.path.join(folder_path, 'front.png')
        back = os.path.join(folder_path, 'back.png')
        
        hue = 0
        if folder in special_map:
            hue = (special_map.index(folder) * 60)
            src_f, src_b = blackwell_f, blackwell_b
        else:
            hue = sum(ord(c) for c in folder) % 360
            src_f, src_b = consumer_f, consumer_b

        if os.path.exists(front):
            with Image.open(front) as orig:
                target_h_f = orig.height
            process_image(src_f, front, target_h_f, hue)
            
        if os.path.exists(back):
            with Image.open(back) as orig:
                target_h_b = orig.height
            process_image(src_b, back, target_h_b, hue)

print("Applied AI pixel arts SAFELY.")
