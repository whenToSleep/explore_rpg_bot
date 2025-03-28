import json
import os

# Путь к файлу locations.json
JSON_PATH = "/data/locations.json"

# Чтение текущего файла
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Функция для рекурсивного обновления путей
def update_paths(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ("image", "map_image") and isinstance(value, str):
                obj[key] = value.replace("assets/", "assets/optimized/")
            else:
                update_paths(value)
    elif isinstance(obj, list):
        for item in obj:
            update_paths(item)

# Обновляем все пути в данных
update_paths(data)

# Сохраняем обновлённый файл
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Пути в locations.json успешно обновлены на assets/optimized/!")