import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

logging.basicConfig(level=logging.INFO)

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

# Веб-сторінка, яку шукає Render
async def handle(request):
    return web.Response(text="Бот працює успішно!")

async def main():
    scheduler = AsyncIOScheduler()
    
    # ТЕСТ НА 16:45 (16:45 - 3 години = 13:45)
    scheduler.add_job(send_daily_poll, "cron", hour=13, minute=45)
    
    scheduler.start()
    logging.info("Планувальк успішно запущено!")
    
    # Піднімаємо сервер на порту 10000 для Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
