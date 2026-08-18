import os

filepath = "src/item_use.c"
with open(filepath, "r") as f:
    content = f.read()

new_code = """

// === CUSTOM ITEM FUNCS ===

extern void ShowPokemonStorageSystemPC(void);
extern void CB2_ReturnToField(void);

static void UsePcAccessFromBag(void)
{
    ShowPokemonStorageSystemPC(); // This might need a proper task or CB2
}

void FieldUseFunc_PcAccess(u8 taskId)
{
    // Close bag and open PC
    ItemMenu_SetExitCallback(ShowPokemonStorageSystemPC);
    ItemMenu_StartFadeToExitCallback(taskId);
}

void FieldUseFunc_SkipMtMoon(u8 taskId)
{
    // Warp to Route 4 (outside Mt Moon)
    // Map group 3 (MAP_GROUP_ROUTE4), Map num 14 (MAP_NUM_ROUTE4)
    // Actually, setting warp and exiting bag
    // It's easier to just use an event script.
}

"""

if "FieldUseFunc_PcAccess" not in content:
    with open(filepath, "a") as f:
        f.write(new_code)
    print("Patched item_use.c")

