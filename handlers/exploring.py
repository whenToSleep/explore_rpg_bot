import asyncio
import random
import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from utils.keyboard import get_sector_keyboard, LOCATIONS, EVENTS
from handlers.start import UserState

router = Router()

@router.message(F.text == "Исследовать", UserState.in_sector)
async def handle_explore(message: Message, state: FSMContext):
    user_data = await state.get_data()
    current_sector = user_data.get("current_sector")
    sector_data = LOCATIONS["sectors"][current_sector]

    sector_events_met_dict = user_data.get("sector_events_met_dict", {})
    sector_events_met = sector_events_met_dict.get(current_sector, set())
    common_events_met = user_data.get("common_events_met", set())

    sector_events_count = len(EVENTS["sector_events"].get(current_sector, []))
    location_events_count = len(EVENTS["common_events"])

    exploring_info = (
        f"*Локация:* {LOCATIONS['location']['name']}\n"
        f"*Сектор:* {sector_data['name']}\n\n"
        f"*События сектора:* {len(sector_events_met)}/{sector_events_count}\n"
        f"*События локации:* {len(common_events_met)}/{location_events_count}\n\n"
        "Исследование началось..."
    )
    await asyncio.sleep(1)  # Задержка перед началом исследования
    await message.answer(exploring_info, parse_mode="Markdown")
    await state.set_state(UserState.exploring)

    await asyncio.sleep(0)  # Основная задержка исследования

    available_sector_events = [e for i, e in enumerate(EVENTS["sector_events"].get(current_sector, [])) if i not in sector_events_met]
    available_common_events = [e for i, e in enumerate(EVENTS["common_events"].values()) if i not in common_events_met]
    event_pool = available_sector_events + available_common_events

    if not event_pool:
        await asyncio.sleep(1)  # Задержка перед сообщением
        await message.answer("Все события в этом секторе и локации уже встречены!")
        await state.set_state(UserState.in_sector)
        return

    event = random.choice(event_pool)
    event_image_path = event.get("image") or EVENTS["default_image"]
    event_image_path = os.path.abspath(event_image_path)

    if not os.path.exists(event_image_path):
        await asyncio.sleep(0)  # Задержка перед ошибкой
        await message.answer(f"Ошибка: файл {event_image_path} не найден!")
        return

    if event in EVENTS["sector_events"].get(current_sector, []):
        event_index = EVENTS["sector_events"][current_sector].index(event)
        sector_events_met.add(event_index)
        sector_events_met_dict[current_sector] = sector_events_met
    else:
        event_index = list(EVENTS["common_events"].values()).index(event)
        common_events_met.add(event_index)

    await state.update_data(sector_events_met_dict=sector_events_met_dict, common_events_met=common_events_met)

    event_image = FSInputFile(event_image_path)
    await asyncio.sleep(0)  # Задержка перед отправкой события
    await message.answer_photo(
        photo=event_image,
        caption=event["description"],
        reply_markup=get_sector_keyboard()
    )
    await state.set_state(UserState.in_sector)

print("Импорт exploring.py завершён")