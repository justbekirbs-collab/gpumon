import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'

def make_text_image(out_path, text, size, bg_color, text_color):
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    # try to use a default PIL font or just draw lines?
    # Better to just draw the text using ImageDraw
    try:
        # standard truetype font if available on mac
        font = ImageFont.truetype("Arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw text centered
    w = 200 # arbitrary
    h = 40
    # Center approx
    draw.text((10, size[1]//2 - h//2), text, font=font, fill=text_color)
    
    img = img.quantize(colors=16)
    img.save(out_path)

def main():
    # 1. Game freak logo (96x48)
    gf_path = os.path.join(BASE_DIR, 'graphics/intro/game_freak/game_freak.png')
    make_text_image(gf_path, "JustBekir", (96, 48), (0, 0, 0), (255, 255, 255))
    
    # 2. Title screen logo (128x64 or 256x64? Let's check dimensions of original)
    title_path = os.path.join(BASE_DIR, 'graphics/title_screen/firered/game_title_logo.png')
    orig = Image.open(title_path)
    make_text_image(title_path, "JustBekir", orig.size, (255, 0, 255), (255, 0, 0)) # Magenta BG (transparent), Red Text

    print("Replaced intro and title logos.")

if __name__ == '__main__':
    main()
