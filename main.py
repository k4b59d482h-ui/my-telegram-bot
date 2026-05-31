import asyncio
import logging
import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

# --- НАЛАШТУВАННЯ ---
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

target_chat_id = None

async def get_weather_text():
    # Актуальний API запит
    url = "https://api.open-meteo.com/v1/forecast?latitude=49.8825&longitude=32.2274&current=temperature_2m,weather_code"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                curr = data.get("current", {})
                temp = round(curr.get("temperature_2m", 0))
                code = curr.get("weather_code", 0)
                
                # Словник для точного опису погоди
                weather_map = {0: "☀️ Ясно", 1: "🌤 Мінлива хмарність", 2: "⛅️ Хмарно", 3: "☁️ Похмуро"}
                emoji = weather_map.get(code, "🌧 Опади/інше")
                return f"📍 Золотоношка\n{emoji}\n🌡 Температура: {temp}°C"
    except Exception as e:
        logging.error(f"Помилка API: {e}")
        return "⚠️ Не вдалося отримати актуальні дані про погоду."

# --- РОЗКЛАД ---
async def scheduled_weather():
    if target_chat_id:
        text = await get_weather_text()
        await bot.send_message(chat_id=target_chat_id, text=f"🕐 **Час гуляти!**\n\n{text}")

# --- КОМАНДИ ---
@dp.message(Command("pogoda"))
async def cmd_pogoda(message: types.Message):
    global target_chat_id
    target_chat_id = message.chat.id # Бот "запам'ятовує" групу
    await message.delete() # Видаляємо команду
    text = await get_weather_text()
    await message.answer(text)

@dp.message(Command("poll"))
async def cmd_poll(message: types.Message):
    await message.delete() # Видаляємо команду
    options = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "Не йду"]
    await bot.send_poll(chat_id=message.chat.id, question="Гуляємо?", options=options, is_anonymous=False)

# Веб-заглушка для Render
async def handle(request):
    return web.Response(text="Бот працює 24/7")

async def main():
    # Запуск сервера
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Планувальник (щодня о 13:00)
    scheduler.add_job(scheduled_weather, 'cron', hour=13, minute=0)
    scheduler.start()

    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
