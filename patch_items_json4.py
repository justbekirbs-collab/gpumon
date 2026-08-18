import json

filepath = "src/data/items.json"
with open(filepath, "r") as f:
    data = json.load(f)

new_items = [
    {
        "english": "PC ACCESS",
        "itemId": "ITEM_PC_ACCESS",
        "price": 0,
        "holdEffect": "HOLD_EFFECT_NONE",
        "holdEffectParam": 0,
        "description_english": "A device to access the Pokemon\\nStorage System from anywhere.",
        "importance": 1,
        "registrability": 1,
        "pocket": "POCKET_KEY_ITEMS",
        "type": "ITEM_TYPE_BAG_MENU",
        "fieldUseFunc": "FieldUseFunc_PcAccess",
        "battleUsage": 0,
        "battleUseFunc": "NULL",
        "secondaryId": 0
    },
    {
        "english": "MT MOON SKIP",
        "itemId": "ITEM_SKIP_MT_MOON",
        "price": 0,
        "holdEffect": "HOLD_EFFECT_NONE",
        "holdEffectParam": 0,
        "description_english": "Instantly skip Mt. Moon\\nand get to Route 4.",
        "importance": 1,
        "registrability": 1,
        "pocket": "POCKET_KEY_ITEMS",
        "type": "ITEM_TYPE_FIELD",
        "fieldUseFunc": "FieldUseFunc_SkipMtMoon",
        "battleUsage": 0,
        "battleUseFunc": "NULL",
        "secondaryId": 0
    },
    {
        "english": "RIG DOWNLOAD",
        "itemId": "ITEM_RIG_DOWNLOADER",
        "price": 0,
        "holdEffect": "HOLD_EFFECT_NONE",
        "holdEffectParam": 0,
        "description_english": "Searches and downloads\\nany RIG into battle.",
        "importance": 1,
        "registrability": 1,
        "pocket": "POCKET_KEY_ITEMS",
        "type": "ITEM_TYPE_BATTLE",
        "fieldUseFunc": "FieldUseFunc_OakStopsYou",
        "battleUsage": 0,
        "battleUseFunc": "ItemUseInBattle_RigDownloader",
        "secondaryId": 0
    }
]

data["items"].extend(new_items)

with open(filepath, "w") as f:
    json.dump(data, f, indent=4)

print("Appended new items to src/data/items.json")
