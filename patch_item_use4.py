import os

filepath = "src/item_use.c"
with open(filepath, "r") as f:
    content = f.read()

insert_str = """
#include "naming_screen.h"

extern u16 gRigDownloaderTargetSpecies;
extern void ReshowBattleScreenAfterMenu(void);
u8 gRigDownloaderTextBuffer[POKEMON_NAME_LENGTH + 1];

static void NamingScreenCallback_ReturnToBattle(void)
{
    // String matching
    u16 species = 0;
    int i;
    for (i = 1; i < NUM_SPECIES; i++)
    {
        if (StringCompareWithoutExtCtrlCodes(gRigDownloaderTextBuffer, gSpeciesNames[i]) == 0)
        {
            species = i;
            break;
        }
    }
    
    gRigDownloaderTargetSpecies = species; // 0 if not found
    
    // We must return to battle. But wait! The naming screen needs to fade out.
    // Actually, DoNamingScreen's return callback is called during a black screen transition.
    // So we can just set the battle screen reshow.
    SetMainCallback2(ReshowBattleScreenAfterMenu);
}

static void LaunchRigDownloaderScreen(void)
{
    int i;
    for(i=0; i<POKEMON_NAME_LENGTH + 1; i++) gRigDownloaderTextBuffer[i] = 0;
    // POKEMON_NAME_LENGTH is 10, plus terminator.
    // We use NAMING_SCREEN_PLAYER because it gives 7 letters. Wait! 
    // NAMING_SCREEN_POKEMON allows 10 letters!
    // But wait, DoNamingScreen doesn't have a direct "pokemon" length without a party index.
    // Actually, we can just use 0 (player) but it limits to 7. 
    // Let's use 2 (box) ? No, we need 10 characters.
    // 1 = Pokemon. Let's try 1.
    DoNamingScreen(1, gRigDownloaderTextBuffer, 0, 0, 0, NamingScreenCallback_ReturnToBattle);
}

void ItemUseInBattle_RigDownloader(u8 taskId)
{
    ItemMenu_SetExitCallback(LaunchRigDownloaderScreen);
    ItemMenu_StartFadeToExitCallback(taskId);
}

"""

content = content.replace('void FieldUseFunc_SkipMtMoon(u8 taskId)', insert_str + 'void FieldUseFunc_SkipMtMoon(u8 taskId)')

with open(filepath, "w") as f:
    f.write(content)
print("Patched item_use.c with rig downloader UI")
