import asyncio
from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# Импортируем нашу новую функцию
from utils.browser import check_site  # Assuming check_site is in utils/browser.py

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("hello")
    await message.answer("Чтобы запустить проверку сайта, используйте команду /check")
    await message.answer("Чтобы остановить проверку сайта, используйте команду /stop_check")


@router.message(Command("check"))
async def cmd_check(message: Message, state: FSMContext):
    # Сообщаем пользователю, что начали проверку
    await message.answer("Начинаю проверку сайта... Это может занять до минуты.")

    # Устанавливаем состояние, что проверка запущена
    await state.set_state("check_running")

    async def periodic_check():
        while await state.get_state() == "check_running":
            # Запускаем функцию проверки и получаем результат
            _success, result_text = await check_site()

            # Отправляем результат пользователю
            await message.answer(result_text)

            # Ждем 10 минут
            await asyncio.sleep(600)  # 600 секунд = 10 минут

    # Запускаем периодическую проверку в фоновом режиме
    asyncio.create_task(periodic_check())


@router.message(Command("stop_check"))
async def cmd_stop_check(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "check_running":
        # Останавливаем проверку
        await state.clear()
        await message.answer("Проверка сайта остановлена.")
    else:
        await message.answer("Проверка сайта не запущена.")