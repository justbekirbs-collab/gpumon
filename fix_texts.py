import os
import re
from pathlib import Path

BASE_DIR = '/Users/bekirkarakose/Documents/ProjectAlascatra'

def main():
    # Load mapping
    species_names_file = os.path.join(BASE_DIR, 'src/data/text/species_names.h')
    with open(species_names_file, 'r') as f:
        content = f.read()
    
    pattern = r'\[SPECIES_([A-Z0-9_]+)\] = _\("([^"]+)"\)'
    matches = re.findall(pattern, content)
    
    mapping = {}
    for original_species, gpu_name in matches:
        if original_species == 'NONE': continue
        # Nidoran variants have special characters in text sometimes, but they are stored as NIDORAN_F
        sp = original_species.replace('_', ' ')
        mapping[sp] = gpu_name

    # Replace safely in all .inc files
    for filepath in Path(os.path.join(BASE_DIR, 'data')).rglob('*.inc'):
        with open(filepath, 'r') as f:
            content = f.read()
        changed = False
        
        # We only want to replace inside .string directives to be absolutely safe
        def replacer(match):
            string_content = match.group(1)
            for old_sp, new_sp in mapping.items():
                # whole word replacement
                string_content = re.sub(rf'\b{old_sp}\b', new_sp, string_content)
            return f'.string "{string_content}"'
            
        new_content = re.sub(r'\.string\s+"([^"]+)"', replacer, content)
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)

if __name__ == '__main__':
    main()
