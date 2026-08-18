import re
import os
from pathlib import Path

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'

def safe_replace(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    # We only want to replace inside .string directives to be absolutely safe
    def replacer(match):
        string_content = match.group(1)
        string_content = string_content.replace("POKéMON", "GPU")
        string_content = string_content.replace("POKEMON", "GPU")
        string_content = string_content.replace("Pokémon", "GPU")
        string_content = string_content.replace("Pokemon", "GPU")
        string_content = string_content.replace("POKé BALL", "RIG")
        string_content = string_content.replace("POKéBALL", "RIG")
        string_content = string_content.replace("Poké Ball", "Rig")
        string_content = string_content.replace("Pokéball", "Rig")
        return f'.string "{string_content}"'
        
    new_content = re.sub(r'\.string\s+"([^"]+)"', replacer, content)
    
    if original != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

count = 0
for ext in ['*.inc', '*.s']:
    for filepath in Path(os.path.join(BASE_DIR, 'data')).rglob(ext):
        if safe_replace(filepath):
            count += 1
print(f"Replaced in {count} files.")
