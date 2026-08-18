import json

filepath = "src/data/items.json"
with open(filepath, "r") as f:
    data = json.load(f)

for item in data["items"]:
    if item["itemId"] == "ITEM_RIG_DOWNLOADER":
        item["type"] = "ITEM_TYPE_BAG_MENU"

with open(filepath, "w") as f:
    json.dump(data, f, indent=4)

print("Fixed type for RIG DOWNLOADER")
