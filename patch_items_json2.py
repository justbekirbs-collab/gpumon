import json
with open("src/data/items.json", "r") as f: data = json.load(f)
for item in data["items"]:
    if "description_english" in item:
        item["description_english"] = item["description_english"].replace("\n", "\\n")
with open("src/data/items.json", "w") as f: json.dump(data, f, indent=2)
