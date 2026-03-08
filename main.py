import asyncio
import logging
import os
from aiogram.client.default import DefaultBotProperties

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import common


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Загружаем переменные окружения из .env файла
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        logging.error("Ошибка: не найден BOT_TOKEN в .env файле.")
        return

    # Инициализация бота и диспетчера
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры из папки handlers
    dp.include_router(common.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())