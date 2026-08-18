import os

filepath = "src/pokemon.c"
with open(filepath, "r") as f:
    content = f.read()

# Find the start of Cheat_GiveTopGPUs
start_idx = content.find("void Cheat_GiveTopGPUs(void)")
if start_idx != -1:
    end_idx = content.find("}", start_idx) + 1
    
    new_func = """void Cheat_GiveTopGPUs(void)
{
    u16 move1 = 1; // 1 to 4 are guaranteed to be tech moves now since we expanded 90
    u16 move2 = 2;
    u16 move3 = 3;
    u16 move4 = 4;
    u32 shinyPersonality = 0; // Or whatever for shiny
    
    // MEWTWO
    CreateMon(&gPlayerParty[0], SPECIES_MEWTWO, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[0], MON_DATA_MOVE1, &move1);
    SetMonData(&gPlayerParty[0], MON_DATA_MOVE2, &move2);
    SetMonData(&gPlayerParty[0], MON_DATA_MOVE3, &move3);
    SetMonData(&gPlayerParty[0], MON_DATA_MOVE4, &move4);
    
    // HO_OH
    CreateMon(&gPlayerParty[1], SPECIES_HO_OH, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[1], MON_DATA_MOVE1, &move1);
    SetMonData(&gPlayerParty[1], MON_DATA_MOVE2, &move2);
    SetMonData(&gPlayerParty[1], MON_DATA_MOVE3, &move3);
    SetMonData(&gPlayerParty[1], MON_DATA_MOVE4, &move4);
    
    // LUGIA
    CreateMon(&gPlayerParty[2], SPECIES_LUGIA, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[2], MON_DATA_MOVE1, &move1);
    SetMonData(&gPlayerParty[2], MON_DATA_MOVE2, &move2);
    SetMonData(&gPlayerParty[2], MON_DATA_MOVE3, &move3);
    SetMonData(&gPlayerParty[2], MON_DATA_MOVE4, &move4);

    // RAYQUAZA
    CreateMon(&gPlayerParty[3], SPECIES_RAYQUAZA, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[3], MON_DATA_MOVE1, &move1);
    SetMonData(&gPlayerParty[3], MON_DATA_MOVE2, &move2);
    SetMonData(&gPlayerParty[3], MON_DATA_MOVE3, &move3);
    SetMonData(&gPlayerParty[3], MON_DATA_MOVE4, &move4);

    // DEOXYS
    CreateMon(&gPlayerParty[4], SPECIES_DEOXYS, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[4], MON_DATA_MOVE1, &move1);
    SetMonData(&gPlayerParty[4], MON_DATA_MOVE2, &move2);
    SetMonData(&gPlayerParty[4], MON_DATA_MOVE3, &move3);
    SetMonData(&gPlayerParty[4], MON_DATA_MOVE4, &move4);

    // GROUDON
    CreateMon(&gPlayerParty[5], SPECIES_GROUDON, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[5], MON_DATA_MOVE1, &move1);
    SetMonData(&gPlayerParty[5], MON_DATA_MOVE2, &move2);
    SetMonData(&gPlayerParty[5], MON_DATA_MOVE3, &move3);
    SetMonData(&gPlayerParty[5], MON_DATA_MOVE4, &move4);
    
    gPlayerPartyCount = 6;

    AddBagItem(1, 99);
    AddPCItem(1, 999);

    FlagSet(FLAG_BADGE01_GET);
    FlagSet(FLAG_BADGE02_GET);
    FlagSet(FLAG_BADGE03_GET);
    FlagSet(FLAG_BADGE04_GET);
    FlagSet(FLAG_BADGE05_GET);
    FlagSet(FLAG_BADGE06_GET);
    FlagSet(FLAG_BADGE07_GET);
    FlagSet(FLAG_BADGE08_GET);
}"""
    
    new_content = content[:start_idx] + new_func + content[end_idx:]
    with open(filepath, "w") as f:
        f.write(new_content)
    print("Patched Cheat_GiveTopGPUs")
