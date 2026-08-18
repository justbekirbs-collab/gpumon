import os

filepath = "data/battle_scripts_2.s"
with open(filepath, "r") as f:
    content = f.read()

old_str = """
.globl BattleScript_DownloadGPU
BattleScript_DownloadGPU::
	playse SE_PC_LOGIN
	waitse
	playanimation gBattlerAttacker, B_ANIM_STATS_SQUARES, 0
	return
"""

new_str = """
.globl BattleScript_DownloadGPU
BattleScript_DownloadGPU::
	playse SE_PC_LOGIN
	playanimation gBattlerAttacker, B_ANIM_STATS_SQUARES, 0
	return
"""

content = content.replace(old_str.strip(), new_str.strip())

with open(filepath, "w") as f:
    f.write(content)
print("Patched battle_scripts_2.s to remove waitse")
