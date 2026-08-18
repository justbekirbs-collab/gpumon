import os
from PIL import Image, ImageDraw

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'

def make_rig_icon(out_path, color_bg, color_fan, letter=None):
    img = Image.new('RGB', (24, 24), (255, 0, 255)) # transparent background (magenta)
    draw = ImageDraw.Draw(img)
    
    # Rig Body
    draw.rectangle([2, 2, 21, 21], fill=(50, 50, 50), outline=(20, 20, 20))
    # Inner board
    draw.rectangle([4, 4, 19, 19], fill=color_bg, outline=(30, 30, 30))
    # Fan or center
    draw.ellipse([6, 6, 17, 17], fill=(40, 40, 40), outline=color_fan)
    # Inner fan hub
    if letter:
        # Just simple cross for fan or "JB" via pixels
        draw.rectangle([10, 10, 13, 13], fill=(255, 215, 0)) # Gold center
    else:
        draw.rectangle([10, 10, 13, 13], fill=color_fan)
        
    # Convert to 16 colors
    img = img.quantize(colors=16)
    img.save(out_path)

def make_party_menu_rigs():
    # pokeball.png is 32x64, let's just make it a static grid for now
    img = Image.new('RGB', (32, 64), (255, 0, 255))
    draw = ImageDraw.Draw(img)
    # 4 frames of 16x16? Or maybe 2 frames of 32x32?
    # Usually it's 32x32 for the big one maybe. Let's just draw some chips.
    for y in range(0, 64, 16):
        for x in range(0, 32, 16):
            draw.rectangle([x+2, y+2, x+13, y+13], fill=(50, 50, 50), outline=(100, 100, 100))
            draw.rectangle([x+6, y+6, x+9, y+9], fill=(0, 255, 0))
    img = img.quantize(colors=16)
    img.save(os.path.join(BASE_DIR, 'graphics/party_menu/pokeball.png'))

    # pokeball_small.png is 16x96
    img2 = Image.new('RGB', (16, 96), (255, 0, 255))
    draw2 = ImageDraw.Draw(img2)
    for y in range(0, 96, 16):
        draw2.rectangle([2, y+2, 13, y+13], fill=(50, 50, 50), outline=(100, 100, 100))
        draw2.rectangle([6, y+6, 9, y+9], fill=(0, 255, 0))
    img2 = img2.quantize(colors=16)
    img2.save(os.path.join(BASE_DIR, 'graphics/party_menu/pokeball_small.png'))


def main():
    icons_dir = os.path.join(BASE_DIR, 'graphics/items/icons')
    
    # Replace all *_ball.png
    for f in os.listdir(icons_dir):
        if f.endswith('_ball.png'):
            path = os.path.join(icons_dir, f)
            if f == 'master_ball.png':
                make_rig_icon(path, (100, 0, 150), (255, 215, 0), letter="JB") # Purple & Gold
            else:
                make_rig_icon(path, (0, 100, 0), (0, 200, 0)) # Green

    make_party_menu_rigs()
    print("Rig graphics generated.")

if __name__ == '__main__':
    main()
