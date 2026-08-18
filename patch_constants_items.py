import os

filepath = "include/constants/items.h"
with open(filepath, "r") as f:
    content = f.read()

find_str = """#define ITEM_SAPPHIRE 374

#define ITEMS_COUNT 375"""
insert_str = """#define ITEM_SAPPHIRE 374
#define ITEM_PC_ACCESS 375
#define ITEM_SKIP_MT_MOON 376
#define ITEM_RIG_DOWNLOADER 377

#define ITEMS_COUNT 378"""

content = content.replace(find_str, insert_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched include/constants/items.h")
