import os
import random
import asyncio  # Добавляем asyncio для sleep
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from utils.keyboard import get_location_keyboard, get_sector_keyboard, get_map_keyboard, LOCATIONS, EVENTS
from handlers.start import UserState

router = Router()

TRANSITION_IMAGE_PATH = "assets/optimized/transition.jpg"


@router.message(F.text == "Что это за место?", UserState.intro)
async def handle_show_location(message: Message, state: FSMContext):
    location_data = LOCATIONS["location"]
    location_path = os.path.abspath(location_data["image"])

    if not os.path.exists(location_path):
        await asyncio.sleep(2)  # Задержка перед ошибкой
        await message.answer(f"Ошибка: файл {location_path} не найден!")
        return

    location_image = FSInputFile(location_path)
    await asyncio.sleep(1)  # Задержка перед отправкой
    await message.answer_photo(
        photo=location_image,
        caption=location_data["description"],
        reply_markup=get_location_keyboard()
    )
    await state.set_state(UserState.location)


@router.message(F.text == "Начать исследования", UserState.location)
async def handle_start_exploration(message: Message, state: FSMContext):
    start_sectors = LOCATIONS["start_sectors"]
    current_sector = random.choice(start_sectors)
    await state.update_data(current_sector=current_sector, sector_events_met_dict={}, common_events_met=set())
    await state.set_state(UserState.in_sector)
    await show_current_sector(message, state)


async def show_current_sector(message: Message, state: FSMContext):
    user_data = await state.get_data()
    current_sector = user_data.get("current_sector")
    sector_data = LOCATIONS["sectors"][current_sector]
    sector_path = os.path.abspath(sector_data["image"])

    if not os.path.exists(sector_path):
        await asyncio.sleep(0)  # Задержка перед ошибкой
        await message.answer(f"Ошибка: файл {sector_path} не найден!")
        return

    sector_events_count = len(EVENTS["sector_events"].get(current_sector, []))
    location_events_count = len(EVENTS["common_events"])
    sector_events_met_dict = user_data.get("sector_events_met_dict", {})
    sector_events_met = len(sector_events_met_dict.get(current_sector, set()))
    common_events_met = len(user_data.get("common_events_met", set()))

    sector_info = (
        f"*Текущая локация:* {LOCATIONS['location']['name']}\n"
        f"*Название текущего сектора:* {sector_data['name']}\n\n"
        f"*Описание сектора:* {sector_data['description']}\n\n"
        f"*Встречено событий сектора:* {sector_events_met}/{sector_events_count}\n"
        f"*Встречено событий локации:* {common_events_met}/{location_events_count}"
    )

    sector_image = FSInputFile(sector_path)
    await asyncio.sleep(1)  # Задержка перед отправкой
    await message.answer_photo(
        photo=sector_image,
        caption=sector_info,
        parse_mode="Markdown",
        reply_markup=get_sector_keyboard()
    )


@router.message(F.text == "Карта", UserState.in_sector)
async def handle_show_map(message: Message, state: FSMContext):
    user_data = await state.get_data()
    current_sector = user_data.get("current_sector")
    sector_data = LOCATIONS["sectors"][current_sector]
    map_path = os.path.abspath(sector_data["map_image"])

    if not os.path.exists(map_path):
        await asyncio.sleep(0)  # Задержка перед ошибкой
        await message.answer(f"Ошибка: файл {map_path} не найден!")
        return

    map_image = FSInputFile(map_path)
    await asyncio.sleep(1)  # Задержка перед отправкой
    await message.answer_photo(
        photo=map_image,
        caption=f"Карта сектора: {sector_data['name']}",
        reply_markup=get_map_keyboard(current_sector)
    )


@router.message(F.text == "Назад", UserState.in_sector)
async def handle_back_to_sector(message: Message, state: FSMContext):
    await show_current_sector(message, state)


@router.message(F.text.in_({sector["name"] for sector in LOCATIONS["sectors"].values()}), UserState.in_sector)
async def handle_move_to_sector(message: Message, state: FSMContext):
    user_data = await state.get_data()
    current_sector = user_data.get("current_sector")
    new_sector_name = message.text
    new_sector_key = next(key for key, value in LOCATIONS["sectors"].items() if value["name"] == new_sector_name)

    if new_sector_key not in LOCATIONS["sectors"][current_sector]["adjacent"]:
        await asyncio.sleep(0)  # Задержка перед ошибкой
        await message.answer("Вы не можете перейти в этот сектор отсюда!")
        return

    total_events = sum(len(EVENTS["sector_events"].get(sector, [])) for sector in LOCATIONS["sectors"]) + len(
        EVENTS["common_events"])
    total_events_met_dict = user_data.get("sector_events_met_dict", {})
    total_sector_events_met = sum(len(events) for events in total_events_met_dict.values())
    total_events_met = total_sector_events_met + len(user_data.get("common_events_met", set()))

    transition_info = (
        f"*Переход в сектор:* {new_sector_name}\n"
        f"*Встречено событий:* {total_events_met}/{total_events}"
    )

    transition_path = os.path.abspath(TRANSITION_IMAGE_PATH)
    if not os.path.exists(transition_path):
        await asyncio.sleep(0)  # Задержка перед ошибкой
        await message.answer(f"Ошибка: файл {transition_path} не найден!")
        return

    transition_image = FSInputFile(transition_path)
    await asyncio.sleep(1)  # Задержка перед отправкой
    await message.answer_photo(
        photo=transition_image,
        caption=transition_info,
        parse_mode="Markdown"
    )
    await state.update_data(current_sector=new_sector_key)
    await show_current_sector(message, state)


print("Импорт location.py завершён")