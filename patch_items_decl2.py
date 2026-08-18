import os

filepath = "src/data/items.h"
with open(filepath, "r") as f:
    content = f.read()

# Make sure to put the declarations right before const struct Item gItems[] = {
find_str = "const struct Item gItems[] = {"
insert_str = """
extern void FieldUseFunc_SkipMtMoon(u8);
extern void FieldUseFunc_PcAccess(u8);
"""

content = content.replace(find_str, insert_str + find_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched items.h declarations for real")
