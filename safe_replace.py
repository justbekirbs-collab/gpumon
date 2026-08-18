import re

def safe_replace(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    # Replace POKéMON -> GPU etc.
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

    if original != content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Replaced in {filepath}")

safe_replace('src/strings.c')
safe_replace('src/battle_message.c')

