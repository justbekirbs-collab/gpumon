import os

filepath = "src/battle_main.c"
with open(filepath, "r") as f:
    content = f.read()

find_str = "void DownloadGPU_NativeFunc(void);\n"
content = content.replace(find_str, "")

find_str2 = '#include "battle_main.h"'
insert_str2 = '#include "battle_main.h"\nvoid DownloadGPU_NativeFunc(void);'

content = content.replace(find_str2, insert_str2)

with open(filepath, "w") as f:
    f.write(content)
print("Patched battle_main.c decl properly")
