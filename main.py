import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Налаштування логів
logging.basicConfig(level=logging.INFO)

# Новий токен твого бота
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"
CHAT_ID = -1001780467253

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_daily_poll():
    try:
        options = ["16:00", "17:00", "18:00", "19:00", "Швидше", "Пізніше", "Не йду"]
        await bot.send_poll(
            chat_id=CHAT_ID,
            question="Гулять",
            options=options,
            is_anonymous=False,
            allows_multiple_answers=True
        )
        logging.info("Опитування успішно надіслано!")
    except Exception as e:
        logging.error(f"Помилка відправки опитування: {e}")

async def main():
    scheduler = AsyncIOScheduler()
    
    # ТЕСТОВИЙ ЧАС: 13:25 за сервером = 16:25 за Києвом
    scheduler.add_job(send_daily_poll, "cron", hour=13, minute=25)
    
    scheduler.start()
    logging.info("Планувальник успішно запущено!")
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
