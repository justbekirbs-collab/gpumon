import os
filepath = "src/item_use.c"
with open(filepath, "r") as f: content = f.read()

new_code = """
// OVERWRITE MT MOON STUFF
#include "script.h"
#include "constants/maps.h"
#include "overworld.h"

static const u8 sScript_SkipMtMoon[] = {
    0x27, // warp
    MAP_NUM(ROUTE4), MAP_GROUP(ROUTE4),
    0xFF, // warp id
    0x0B, 0x00, // x = 11
    0x0D, 0x00, // y = 13
    0x02, // end
};

static void UseSkipMtMoon(void)
{
    ScriptContext1_SetupScript(sScript_SkipMtMoon);
}

void FieldUseFunc_SkipMtMoon(u8 taskId)
{
    ItemMenu_SetExitCallback(UseSkipMtMoon);
    ItemMenu_StartFadeToExitCallback(taskId);
}
"""
if "UseSkipMtMoon" not in content:
    with open(filepath, "a") as f: f.write(new_code)
