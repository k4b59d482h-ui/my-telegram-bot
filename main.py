import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Налаштування логів
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "7294244249:AAEy5wK6_vXpPlpB4_n8eO6-uV7O8f7O8f0"
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
    
    # ТЕСТОВИЙ ЧАС: 13:20 за сервером = 16:20 за Києвом
    scheduler.add_job(send_daily_poll, "cron", hour=13, minute=20)
    
    scheduler.start()
    logging.info("Планувальник успішно запущено!")
    
    # Запуск бота в режимі постійного опитування сервера
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
