import os

filepath = "src/item_use.c"
with open(filepath, "r") as f:
    content = f.read()

find_str = "void FieldUseFunc_TownMap(u8 taskId)"
insert_str = """
extern void ShowPokemonStorageSystemPC(void);
void FieldUseFunc_PcAccess(u8 taskId)
{
    ItemMenu_SetExitCallback(ShowPokemonStorageSystemPC);
    ItemMenu_StartFadeToExitCallback(taskId);
}

extern void WarpIntoMap(void);
extern void SetWarpDestination(s8 mapGroup, s8 mapNum, s8 warpId, s8 x, s8 y);
static void ExitBagSkipMtMoon(void)
{
    SetWarpDestination(3, 14, -1, 15, 15);
    WarpIntoMap();
    SetMainCallback2(CB2_LoadMap);
}

void FieldUseFunc_SkipMtMoon(u8 taskId)
{
    ItemMenu_SetExitCallback(ExitBagSkipMtMoon);
    ItemMenu_StartFadeToExitCallback(taskId);
}

"""

content = content.replace(find_str, insert_str + find_str)

with open(filepath, "w") as f:
    f.write(content)
print("Patched item_use.c with FieldUseFuncs")
