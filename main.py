import asyncio
import logging
import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

# Змінна для запам'ятовування групи
target_chat_id = None

async def get_weather_text():
    url = "https://api.open-meteo.com/v1/forecast?latitude=49.8825&longitude=32.2274&current_weather=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            curr = data.get("current_weather", {})
            temp = round(curr.get("temperature", 0))
            code = curr.get("weathercode", 0)
            emoji = "☀️" if code == 0 else "🌧" if code > 50 else "🌤"
            return f"📍 Золотоношка\n{emoji}\n🌡 {temp}°C"

# Завдання для розкладу
async def daily_weather():
    global target_chat_id
    if target_chat_id:
        text = await get_weather_text()
        await bot.send_message(chat_id=target_chat_id, text=f"☀️ Доброго ранку!\n{text}")

@dp.message(Command("pogoda"))
async def handle_weather(message: types.Message):
    global target_chat_id
    # Запам'ятовуємо ID групи, де викликали команду
    target_chat_id = message.chat.id
    text = await get_weather_text()
    await message.answer(f"📍 Погода за запитом:\n{text}")

@dp.message(Command("poll"))
async def handle_poll(message: types.Message):
    options = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "Не йду"]
    await bot.send_poll(chat_id=message.chat.id, question="Гулять", options=options, is_anonymous=False)

async def handle(request):
    return web.Response(text="Бот активний")

async def main():
    # Запуск веб-сервера
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Планувальник (надсилати щодня о 09:00)
    scheduler.add_job(daily_weather, 'cron', hour=9, minute=0)
    scheduler.start()

    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
