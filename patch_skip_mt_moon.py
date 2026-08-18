import os

filepath = "src/item_use.c"
with open(filepath, "r") as f:
    content = f.read()

old_func = """void FieldUseFunc_SkipMtMoon(u8 taskId)
{
    // Warp to Route 4 (outside Mt Moon)
    // Map group 3 (MAP_GROUP_ROUTE4), Map num 14 (MAP_NUM_ROUTE4)
    // Actually, setting warp and exiting bag
    // It's easier to just use an event script.
}"""

new_func = """extern void WarpIntoMap(void);
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
}"""

content = content.replace(old_func, new_func)

with open(filepath, "w") as f:
    f.write(content)
print("Patched SkipMtMoon")
