import os

filepath = "src/pokemon.c"
with open(filepath, "r") as f: content = f.read()

# Add to Cheat_GiveTopGPUs
new_pc = """
    // Add 14 GPUs to PC
    struct Pokemon pcMon;
    u16 tpuSpecies[] = {SPECIES_ARTICUNO, SPECIES_ZAPDOS, SPECIES_MOLTRES, SPECIES_DRAGONITE, SPECIES_MEW, 
                        SPECIES_ENTEI, SPECIES_RAIKOU, SPECIES_SUICUNE, SPECIES_TYRANITAR, SPECIES_CELEBI,
                        SPECIES_REGIROCK, SPECIES_REGICE, SPECIES_REGISTEEL, SPECIES_METAGROSS};
    
    for (int i = 0; i < 14; i++) {
        CreateMon(&pcMon, tpuSpecies[i], 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
        SetMonData(&pcMon, MON_DATA_MOVE1, &move1);
        SendMonToPC(&pcMon);
    }
"""

content = content.replace("// Custom GPU Items", new_pc + "\n    // Custom GPU Items")

with open(filepath, "w") as f: f.write(content)
