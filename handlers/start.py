import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from utils.keyboard import get_intro_keyboard, LOCATIONS

router = Router()


class UserState(StatesGroup):
    intro = State()
    location = State()
    in_sector = State()
    exploring = State()


@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    intro_data = LOCATIONS["intro"]
    intro_path = os.path.abspath(intro_data["image"])

    if not os.path.exists(intro_path):
        await message.answer(f"Ошибка: файл {intro_path} не найден!")
        return

    intro_image = FSInputFile(intro_path)
    await message.answer_photo(
        photo=intro_image,
        caption=intro_data["description"],
        reply_markup=get_intro_keyboard()
    )
    await state.set_state(UserState.intro)


print("Импорт start.py завершён")