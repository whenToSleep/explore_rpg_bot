from aiogram import Router
from handlers.start import router as start_router
from handlers.location import router as location_router
from handlers.exploring import router as exploring_router

router = Router()

# Подключаем роутеры из других модулей
router.include_router(start_router)
router.include_router(location_router)
router.include_router(exploring_router)

print("Все роутеры из start.py, location.py и exploring.py подключены")