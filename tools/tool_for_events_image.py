import json
import os

JSON_PATH = "/data/events.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

data["default_image"] = data["default_image"].replace("assets/", "assets/optimized/")
for events in data["common_events"].values():
    if "image" in events:
        events["image"] = events["image"].replace("assets/", "assets/optimized/")
for sector_events in data["sector_events"].values():
    for event in sector_events:
        if "image" in event and event["image"]:
            event["image"] = event["image"].replace("assets/", "assets/optimized/")

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Пути в events.json обновлены!")