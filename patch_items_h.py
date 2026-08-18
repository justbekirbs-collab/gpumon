import os

filepath = "src/data/items.h"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace(".battleUseFunc = BattleUseFunc_DownloadTrillium", ".battleUseFunc = BattleUseFunc_PokeFlute")
content = content.replace(".battleUseFunc = BattleUseFunc_DownloadH100", ".battleUseFunc = BattleUseFunc_PokeFlute")
content = content.replace(".battleUseFunc = BattleUseFunc_DownloadA100", ".battleUseFunc = BattleUseFunc_PokeFlute")

# Also replace EFFECT_ITEM_INCREASE_STAT with 2
content = content.replace(".battleUsage = EFFECT_ITEM_INCREASE_STAT", ".battleUsage = 2")
content = content.replace(".battleUsage = EFFECT_ITEM_RESTORE_HP", ".battleUsage = 2")

with open(filepath, "w") as f:
    f.write(content)
print("Patched items.h")
