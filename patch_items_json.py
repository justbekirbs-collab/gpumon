import json

with open("src/data/items.json", "r") as f:
    data = json.load(f)

for item in data["items"]:
    # ITEM_FAME_CHECKER -> PC ACCESS
    if item["itemId"] == "ITEM_FAME_CHECKER":
        item["english"] = "PC ACCESS"
        item["description_english"] = "A device to access the Pokemon\nStorage System from anywhere."
        item["fieldUseFunc"] = "FieldUseFunc_PcAccess"
    
    # ITEM_VS_SEEKER -> SKIP MT MOON
    if item["itemId"] == "ITEM_VS_SEEKER":
        item["english"] = "SKIP MT MOON"
        item["description_english"] = "Instantly skip Mt. Moon\nand get to Route 4."
        item["fieldUseFunc"] = "FieldUseFunc_SkipMtMoon"

    # ITEM_TRI_PASS -> DOWNLOAD H100
    if item["itemId"] == "ITEM_TRI_PASS":
        item["english"] = "DOWNLD H100"
        item["description_english"] = "Downloads a H100 GPU\ndirectly into battle."
        item["battleUseFunc"] = "BattleUseFunc_DownloadH100"
        item["battleUsage"] = "EFFECT_ITEM_INCREASE_STAT"
        item["type"] = "ITEM_TYPE_PARTY_MENU"
        item["pocket"] = "POCKET_ITEMS"

    # ITEM_RAINBOW_PASS -> DOWNLOAD A100
    if item["itemId"] == "ITEM_RAINBOW_PASS":
        item["english"] = "DOWNLD A100"
        item["description_english"] = "Downloads an A100 GPU\ndirectly into battle."
        item["battleUseFunc"] = "BattleUseFunc_DownloadA100"
        item["battleUsage"] = "EFFECT_ITEM_INCREASE_STAT"
        item["type"] = "ITEM_TYPE_PARTY_MENU"
        item["pocket"] = "POCKET_ITEMS"
        
    # ITEM_TEACHY_TV -> DOWNLD TRILLIUM
    if item["itemId"] == "ITEM_TEACHY_TV":
        item["english"] = "DOWNLD TRILL"
        item["description_english"] = "Downloads a Trillium TPU\ndirectly into battle."
        item["battleUseFunc"] = "BattleUseFunc_DownloadTrillium"
        item["battleUsage"] = "EFFECT_ITEM_INCREASE_STAT"
        item["type"] = "ITEM_TYPE_PARTY_MENU"
        item["pocket"] = "POCKET_ITEMS"

with open("src/data/items.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated items.json")
