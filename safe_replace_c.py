import re

def safe_replace(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    
    # We want to replace inside double quotes ONLY.
    # We can split the file by '"'. The even indices (0, 2, 4) are OUTSIDE strings.
    # The odd indices (1, 3, 5) are INSIDE strings.
    # This assumes no escaped quotes like `\"` which exist but are rare in these strings.
    # Actually, pokeemerald strings use `""` or no quotes, wait.
    # In C, `\"` is possible. Let's just use regex for string literals.
    
    def replacer(match):
        string_content = match.group(0) # Includes the quotes
        string_content = string_content.replace("POKéMON", "GPU")
        string_content = string_content.replace("POKEMON", "GPU")
        string_content = string_content.replace("Pokémon", "GPU")
        string_content = string_content.replace("Pokemon", "GPU")
        string_content = string_content.replace("POKé BALL", "RIG")
        string_content = string_content.replace("POKéBALL", "RIG")
        string_content = string_content.replace("Poké Ball", "Rig")
        string_content = string_content.replace("Pokéball", "Rig")
        return string_content

    # Regex for C string literals (handles escaped quotes)
    new_content = re.sub(r'"([^"\\]|\\.)*"', replacer, content)

    if original != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Replaced in {filepath}")

safe_replace('src/strings.c')
safe_replace('src/battle_message.c')
