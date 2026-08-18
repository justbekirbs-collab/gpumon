import json

filepath = "src/data/items.json"
with open(filepath, "r") as f:
    data = json.load(f)

# Find ITEM_RIG_DOWNLOADER and change battleUsage
for item in data["items"]:
    if item["itemId"] == "ITEM_RIG_DOWNLOADER":
        item["battleUsage"] = 1

with open(filepath, "w") as f:
    json.dump(data, f, indent=4)

print("Fixed battleUsage for RIG DOWNLOADER")
