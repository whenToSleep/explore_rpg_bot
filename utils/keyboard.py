import os
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
LOCATIONS_PATH = os.path.join(DATA_DIR, "locations.json")
EVENTS_PATH = os.path.join(DATA_DIR, "events.json")

with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
    LOCATIONS = json.load(f)

with open(EVENTS_PATH, "r", encoding="utf-8") as f:
    EVENTS = json.load(f)

def get_intro_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Что это за место?")]],
        resize_keyboard=True
    )
    print(f"Сформирована клавиатура intro: {[[btn.text for btn in row] for row in keyboard.keyboard]}")
    return keyboard

def get_location_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать исследования")]],
        resize_keyboard=True
    )
    print(f"Сформирована клавиатура location: {[[btn.text for btn in row] for row in keyboard.keyboard]}")
    return keyboard

def get_sector_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Исследовать")],
            [KeyboardButton(text="Карта")]
        ],
        resize_keyboard=True
    )
    print(f"Сформирована клавиатура сектора: {[[btn.text for btn in row] for row in keyboard.keyboard]}")
    return keyboard

def get_map_keyboard(current_sector):
    adjacent_sectors = LOCATIONS["sectors"][current_sector]["adjacent"]
    keyboard = [[KeyboardButton(text=LOCATIONS["sectors"][sector]["name"])] for sector in adjacent_sectors]
    keyboard.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )