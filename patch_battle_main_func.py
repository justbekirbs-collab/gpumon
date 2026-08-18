import os

filepath = "src/battle_main.c"
with open(filepath, "r") as f: content = f.read()

new_func = """
#include "pokemon.h"
#include "constants/species.h"

void DownloadGPU_NativeFunc(void)
{
    u16 targetSpecies = SPECIES_BULBASAUR;
    
    if (gLastUsedItem == ITEM_TRI_PASS)
        targetSpecies = SPECIES_HO_OH;
    else if (gLastUsedItem == ITEM_RAINBOW_PASS)
        targetSpecies = SPECIES_LUGIA;
    else if (gLastUsedItem == ITEM_TEACHY_TV)
        targetSpecies = SPECIES_RAYQUAZA;
        
    u32 shinyPersonality = 0; // Just using 0, might not be shiny unless matched with ID, but we can try 
    // To guarantee shiny, you need to match OTID. Let's just create a mon.
    u32 otId = gSaveBlock2Ptr->playerTrainerId[0] | (gSaveBlock2Ptr->playerTrainerId[1] << 8) | (gSaveBlock2Ptr->playerTrainerId[2] << 16) | (gSaveBlock2Ptr->playerTrainerId[3] << 24);
    
    // A known shiny personality for OTID 0
    // shiny = (TID ^ SID ^ P1 ^ P2) < 8
    shinyPersonality = otId; // if P1^P2 == 0, then TID^SID ^ 0 = TID^SID. We want < 8.
    
    CreateMon(&gPlayerParty[gBattlerPartyIndexes[gBattlerAttacker]], targetSpecies, 100, 31, 1, shinyPersonality, OT_ID_PLAYER_ID, 0);
    
    // Copy to battle mons
    PokemonToBattleMon(&gPlayerParty[gBattlerPartyIndexes[gBattlerAttacker]], &gBattleMons[gBattlerAttacker]);
    
    // Refresh sprite
    // Actually, sprite reload mid-battle is complicated. We'll just let the stats take effect, 
    // and rely on the UI animation or the next turn!
}
"""

if "DownloadGPU_NativeFunc" not in content:
    # Append it at the end
    with open(filepath, "a") as f: f.write(new_func)
    print("Patched battle_main_func")

