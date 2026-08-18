import os

filepath = "src/pokemon.c"
with open(filepath, "r") as f:
    content = f.read()

find_str = "    // === HM CUT + HM SURF in bag ==="
insert_str = """
    // === GIVE SPECIAL ITEMS ===
    AddBagItem(ITEM_FAME_CHECKER, 1);
    AddBagItem(ITEM_VS_SEEKER, 1);
    AddBagItem(ITEM_TEACHY_TV, 1);
    AddBagItem(ITEM_TRI_PASS, 1);
    AddBagItem(ITEM_RAINBOW_PASS, 1);
"""

content = content.replace(find_str, insert_str + "\n" + find_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched Cheat_GiveTopGPUs to give items")
