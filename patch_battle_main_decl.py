import os

filepath = "src/battle_main.c"
with open(filepath, "r") as f:
    content = f.read()

find_str = "extern const u8 gBattlescriptsForRunningByItem[];"
insert_str = "void DownloadGPU_NativeFunc(void);\n"

content = content.replace(find_str, insert_str + find_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched battle_main.c with decl")
