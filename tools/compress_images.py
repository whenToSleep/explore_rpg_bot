from PIL import Image
import os

# Пути к папкам
INPUT_DIR = "/assets/"  # Исходная папка с изображениями
OUTPUT_DIR = "/assets/optimized/"  # Папка для сжатых изображений

# Параметры сжатия
MAX_SIZE = (800, 600)  # Максимальный размер (ширина, высота)
QUALITY = 80  # Качество для JPEG (0-100)

# Создаём папку для оптимизированных изображений, если её нет
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Поддерживаемые форматы
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png")

# Обработка всех файлов в папке и подпапках
for root, _, files in os.walk(INPUT_DIR):
    for filename in files:
        if filename.lower().endswith(SUPPORTED_FORMATS):
            input_path = os.path.join(root, filename)
            # Сохраняем структуру подпапок
            relative_path = os.path.relpath(input_path, INPUT_DIR)
            output_path = os.path.join(OUTPUT_DIR, relative_path)

            # Создаём подпапки в OUTPUT_DIR, если их нет
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Открываем изображение
            with Image.open(input_path) as img:
                # Конвертируем в RGB, если это PNG с прозрачностью
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                # Уменьшаем размер
                img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                # Сохраняем с оптимизацией в формате JPEG
                img.save(output_path, "JPEG", quality=QUALITY, optimize=True)

            # Выводим информацию о сжатии
            original_size = os.path.getsize(input_path) / 1024  # Размер в КБ
            compressed_size = os.path.getsize(output_path) / 1024  # Размер в КБ
            print(f"Сжато: {relative_path}, {original_size:.2f} КБ → {compressed_size:.2f} КБ")

print("Сжатие всех изображений завершено!")