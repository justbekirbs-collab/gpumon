import os

filepath = "src/data/items.h"
with open(filepath, "r") as f:
    content = f.read()

find_str = "extern void FieldUseFunc_OakStopsYou(u8);"
insert_str = """
extern void FieldUseFunc_SkipMtMoon(u8);
extern void FieldUseFunc_PcAccess(u8);
"""

content = content.replace(find_str, find_str + "\n" + insert_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched items.h declarations")
