import os

filepath = "src/battle_main.c"
with open(filepath, "r") as f:
    content = f.read()

# I will find the first PokemonToBattleMon block (lines 10-44 roughly)
# and the second one (lines 4533-4565 roughly)
import re
content = re.sub(r'static void PokemonToBattleMon\(struct Pokemon \*src, struct BattlePokemon \*dst\)\s*\{.*?\n\}\n', '', content, flags=re.DOTALL)

# Now insert it exactly once, with MON_DATA_ABILITY_NUM, string copy, and before DownloadGPU_NativeFunc
insert_str = """
static void PokemonToBattleMon(struct Pokemon *src, struct BattlePokemon *dst)
{
    int i;
    u8 nickname[POKEMON_NAME_LENGTH + 1];
    dst->species = GetMonData(src, MON_DATA_SPECIES);
    dst->item = GetMonData(src, MON_DATA_HELD_ITEM);
    for (i = 0; i < MAX_MON_MOVES; ++i)
    {
        dst->moves[i] = GetMonData(src, MON_DATA_MOVE1 + i);
        dst->pp[i] = GetMonData(src, MON_DATA_PP1 + i);
    }
    dst->ppBonuses = GetMonData(src, MON_DATA_PP_BONUSES);
    dst->friendship = GetMonData(src, MON_DATA_FRIENDSHIP);
    dst->experience = GetMonData(src, MON_DATA_EXP);
    dst->hpIV = GetMonData(src, MON_DATA_HP_IV);
    dst->attackIV = GetMonData(src, MON_DATA_ATK_IV);
    dst->defenseIV = GetMonData(src, MON_DATA_DEF_IV);
    dst->speedIV = GetMonData(src, MON_DATA_SPEED_IV);
    dst->spAttackIV = GetMonData(src, MON_DATA_SPATK_IV);
    dst->spDefenseIV = GetMonData(src, MON_DATA_SPDEF_IV);
    dst->personality = GetMonData(src, MON_DATA_PERSONALITY);
    dst->status1 = GetMonData(src, MON_DATA_STATUS);
    dst->level = GetMonData(src, MON_DATA_LEVEL);
    dst->hp = GetMonData(src, MON_DATA_HP);
    dst->maxHP = GetMonData(src, MON_DATA_MAX_HP);
    dst->attack = GetMonData(src, MON_DATA_ATK);
    dst->defense = GetMonData(src, MON_DATA_DEF);
    dst->speed = GetMonData(src, MON_DATA_SPEED);
    dst->spAttack = GetMonData(src, MON_DATA_SPATK);
    dst->spDefense = GetMonData(src, MON_DATA_SPDEF);
    dst->isEgg = GetMonData(src, MON_DATA_IS_EGG);
    dst->abilityNum = GetMonData(src, MON_DATA_ABILITY_NUM);
    dst->otId = GetMonData(src, MON_DATA_OT_ID);
    dst->type1 = gSpeciesInfo[dst->species].types[0];
    dst->type2 = gSpeciesInfo[dst->species].types[1];
    dst->ability = GetAbilityBySpecies(dst->species, dst->abilityNum);
    GetMonData(src, MON_DATA_NICKNAME, nickname);
    StringCopy_Nickname(dst->nickname, nickname);
    GetMonData(src, MON_DATA_OT_NAME, dst->otName);
}

"""

find_str = "void DownloadGPU_NativeFunc(void)"
content = content.replace(find_str, insert_str + find_str)

with open(filepath, "w") as f:
    f.write(content)
print("Fixed PokemonToBattleMon definition properly")
