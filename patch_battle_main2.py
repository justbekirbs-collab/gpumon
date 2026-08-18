import os

filepath = "src/battle_main.c"
with open(filepath, "r") as f:
    content = f.read()

old_str = """    else if (gLastUsedItem == ITEM_TRI_PASS || gLastUsedItem == ITEM_RAINBOW_PASS || gLastUsedItem == ITEM_TEACHY_TV)
    {
        extern const u8 BattleScript_DownloadGPU[];
        gBattlescriptCurrInstr = BattleScript_DownloadGPU;
    }"""

new_str = """    else if (gLastUsedItem == ITEM_TRI_PASS || gLastUsedItem == ITEM_RAINBOW_PASS || gLastUsedItem == ITEM_TEACHY_TV)
    {
        extern const u8 BattleScript_DownloadGPU[];
        DownloadGPU_NativeFunc();
        gBattlescriptCurrInstr = BattleScript_DownloadGPU;
    }"""

content = content.replace(old_str, new_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched battle_main.c")
