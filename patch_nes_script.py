import os

filepath = "/Users/bekirkarakose/Documents/ProjectAlascatra/data/maps/PalletTown_PlayersHouse_2F/scripts.inc"
with open(filepath, "r") as f:
    content = f.read()

# Replace NES event to give GPUs and also show a message
new_nes_script = """PalletTown_PlayersHouse_2F_EventScript_NES::
	callnative Cheat_GiveTopGPUs
	msgbox PalletTown_PlayersHouse_2F_Text_PlayedWithNES, MSGBOX_SIGN
	end"""

content = content.replace(
    "PalletTown_PlayersHouse_2F_EventScript_NES::\n\tmsgbox PalletTown_PlayersHouse_2F_Text_PlayedWithNES, MSGBOX_SIGN\n\tend",
    new_nes_script
)

with open(filepath, "w") as f:
    f.write(content)
print("Patched NES script successfully!")
