import os

filepath = "src/pokemon.c"
with open(filepath, "r") as f:
    content = f.read()

old_str = """    // === GIVE SPECIAL ITEMS ===
    AddBagItem(ITEM_FAME_CHECKER, 1);
    AddBagItem(ITEM_VS_SEEKER, 1);
    AddBagItem(ITEM_TEACHY_TV, 1);
    AddBagItem(ITEM_TRI_PASS, 1);
    AddBagItem(ITEM_RAINBOW_PASS, 1);"""

new_str = """    // === GIVE SPECIAL ITEMS ===
    AddBagItem(ITEM_PC_ACCESS, 1);
    AddBagItem(ITEM_SKIP_MT_MOON, 1);
    AddBagItem(ITEM_RIG_DOWNLOADER, 1);"""

content = content.replace(old_str, new_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched pokemon.c")
