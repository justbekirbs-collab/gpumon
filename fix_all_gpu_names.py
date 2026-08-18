import re
import random

MAX_LEN = 10

# Prefixes for generating fake GPU names
PREFIXES = ["RTX", "GTX", "Radeon", "RX", "HD", "Intel", "Arc", "Tesla", "Quadro", "Voodoo", "Matrox", "S3", "Riva"]
MODIFIERS = ["Ti", "Super", "XT", "Pro", "Max", "Ultra"]

def generate_gpu_name(index):
    # Special overrides for the legendary ones and a few starting ones
    if index == 150: return "BLACKWELL"  # Mewtwo
    if index == 250: return "H100"       # Ho-Oh
    if index == 249: return "A100"       # Lugia
    if index == 384: return "MI300X"     # Rayquaza
    if index == 386: return "TPU v5e"    # Deoxys
    if index == 383: return "GAUDI 3"    # Groudon
    
    # Generic names
    pref = random.choice(PREFIXES)
    num = str(random.randint(10, 99) * 100)
    mod = random.choice([""] * 3 + MODIFIERS)  # Higher chance of no modifier
    
    # Try combinations that fit in 10 chars
    name1 = f"{pref}{num}"
    name2 = f"{pref} {num}"
    name3 = f"{pref} {mod}"
    name4 = f"{pref[:2]}{num}{mod}"
    
    choices = [name1, name2, name3, name4]
    valid_choices = [c for c in choices if len(c) <= MAX_LEN and len(c) > 0]
    
    if valid_choices:
        name = random.choice(valid_choices)
    else:
        name = f"G-{num}"
        
    return name.upper()

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Match lines like: [SPECIES_BULBASAUR] = _("BULBASAUR"),
    pattern = re.compile(r'(\[SPECIES_([A-Z0-9_]+)\]\s*=\s*_)\("([^"]+)"\)(,?)')
    
    # We will use an index counter
    # But wait, species are not strictly sequential in the file, we can just keep a counter
    
    count = 1
    def replacer(match):
        nonlocal count
        prefix = match.group(1)
        species = match.group(2)
        suffix = match.group(4)
        
        if species == "NONE":
            return match.group(0) # Keep ??????????
            
        new_name = generate_gpu_name(count)
        # Pad with spaces? No, Pokemon names aren't padded.
        count += 1
        return f'{prefix}("{new_name}"){suffix}'

    new_content = pattern.sub(replacer, content)
    
    with open(filepath, "w") as f:
        f.write(new_content)
        
    print(f"Replaced {count-1} species names in {filepath}")

process_file("src/data/text/species_names.h")
