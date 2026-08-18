import re

def main():
    path = 'src/data/text/species_names.h'
    with open(path, 'r') as f:
        content = f.read()

    # We want:
    # SPECIES_MEWTWO -> BLACKWELL
    # SPECIES_HO_OH -> H100
    # SPECIES_LUGIA -> A100
    
    # First, let's find who currently has BLACKWELL (or B200), H100, A100 and swap them with the legendaries
    
    mapping = {
        'SPECIES_MEWTWO': 'BLACKWELL',
        'SPECIES_HO_OH': 'H100',
        'SPECIES_LUGIA': 'A100'
    }
    
    for spec, name in mapping.items():
        content = re.sub(rf'\[{spec}\] = _\("[^"]+"\)', f'[{spec}] = _("{name}")', content)
        
    with open(path, 'w') as f:
        f.write(content)
        
if __name__ == '__main__':
    main()
