import json

filepath = "src/data/items.json"
with open(filepath, "r") as f:
    data = json.load(f)

# The items array should be the root? Let's check format.
# Wait, let's load it and append.
new_items = [
    {
        "id": "ITEM_PC_ACCESS",
        "name": "PC ACCESS",
        "price": 0,
        "description": "A device to access the Pokemon\\nStorage System from anywhere.",
        "pocket": "POCKET_KEY_ITEMS",
        "type": "ITEM_TYPE_BAG_MENU",
        "field_use_func": "FieldUseFunc_PcAccess",
        "battle_usage": "0",
        "battle_use_func": "NULL",
        "secondary_id": 0,
        "importance": 1,
        "registrability": 1
    },
    {
        "id": "ITEM_SKIP_MT_MOON",
        "name": "MT MOON SKIP",
        "price": 0,
        "description": "Instantly skip Mt. Moon\\nand get to Route 4.",
        "pocket": "POCKET_KEY_ITEMS",
        "type": "ITEM_TYPE_FIELD",
        "field_use_func": "FieldUseFunc_SkipMtMoon",
        "battle_usage": "0",
        "battle_use_func": "NULL",
        "secondary_id": 0,
        "importance": 1,
        "registrability": 1
    },
    {
        "id": "ITEM_RIG_DOWNLOADER",
        "name": "RIG DOWNLOAD",
        "price": 0,
        "description": "Searches and downloads\\nany RIG into battle.",
        "pocket": "POCKET_KEY_ITEMS",
        "type": "ITEM_TYPE_BATTLE",
        "field_use_func": "FieldUseFunc_OakStopsYou",
        "battle_usage": "0",
        "battle_use_func": "ItemUseInBattle_RigDownloader",
        "secondary_id": 0,
        "importance": 1,
        "registrability": 1
    }
]

data.extend(new_items)

with open(filepath, "w") as f:
    json.dump(data, f, indent=4)

print("Appended new items to src/data/items.json")
