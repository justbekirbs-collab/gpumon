import os
import re

BASE = "/Users/bekirkarakose/Documents/ProjectAlascatra"
src_file = os.path.join(BASE, "src/pokemon_icon.c")

with open(src_file) as f:
    content = f.read()

# Make all species use palette 0
def fix_indices(match):
    lines = match.group(0).split('\n')
    new_lines = []
    for line in lines:
        if "SPECIES_" in line:
            # Change any digit at the end to 0
            line = re.sub(r'(\d)(\s*,)', r'0\2', line)
        new_lines.append(line)
    return '\n'.join(new_lines)

new_content = re.sub(r'const u8 gMonIconPaletteIndices\[\] = \{.*?\};', fix_indices, content, flags=re.DOTALL)

if new_content != content:
    with open(src_file, 'w') as f:
        f.write(new_content)
    print("Patched gMonIconPaletteIndices to all use palette 0")

