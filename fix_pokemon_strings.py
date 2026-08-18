import os
import re
from pathlib import Path

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # Replacements
    # Since we are replacing inside strings, we can just replace the words.
    
    content = content.replace("POKéMON", "GPU")
    content = content.replace("POKEMON", "GPU")
    content = content.replace("Pokémon", "GPU")
    content = content.replace("Pokemon", "GPU")
    content = content.replace("pokémon", "gpu")
    content = content.replace("pokemon", "gpu")

    content = content.replace("POKé BALL", "RIG")
    content = content.replace("POKéBALL", "RIG")
    content = content.replace("POKE BALL", "RIG")
    content = content.replace("POKEBALL", "RIG")
    content = content.replace("Poké Ball", "Rig")
    content = content.replace("Pokéball", "Rig")

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    dirs_to_check = ['src', 'data', 'include']
    extensions = ['.c', '.h', '.inc']
    
    count = 0
    for d in dirs_to_check:
        dir_path = os.path.join(BASE_DIR, d)
        for ext in extensions:
            for filepath in Path(dir_path).rglob(f'*{ext}'):
                if replace_in_file(filepath):
                    count += 1
    
    print(f"Replaced Pokemon with GPU in {count} files.")

if __name__ == '__main__':
    main()
