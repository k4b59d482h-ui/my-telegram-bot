import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# Налаштування логування для контролю роботи бота
logging.basicConfig(level=logging.INFO)

# Усі дані вже прописані та готові
BOT_TOKEN = "7294244249:AAEy5wK6_vXpPlpB4_n8eO6-uV7O8f7O8f0"  # Твій токен
CHAT_ID = -1001780467253                                      # ID твоєї супергрупи

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def send_daily_poll():
    try:
        await bot.send_poll(
            chat_id=CHAT_ID,
            question="Гулять",
            options=[
                "14.00",
                "15.00",
                "16.00",
                "17.00",
                "18.00",
                "19.00",
                "20.00",
                "21.00",
                "22.00"
            ],
            is_anonymous=False,            # Справжні імена (видно, хто голосує)
            allows_multiple_answers=True    # Можна обрати кілька варіантів часу
        )
        logging.info(f"Опитування успішно надіслано в групу о {datetime.now()}")
    except Exception as e:
        logging.error(f"Не вдалося надіслати опитування: {e}")

async def main():
    # Робимо запуск щодня рівно о 12:00
    scheduler.add_job(send_daily_poll, "cron", hour=12, minute=45)
    scheduler.start()
    
    logging.info("Бот запущенний. Опитування надходитиме щодня о 12:00 за часом сервера.")
    
    # Запускаємо постійну роботу бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
