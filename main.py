import asyncio
import logging
import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
import os

# --- НАЛАШТУВАННЯ ---
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"
PORT = int(os.environ.get("PORT", 8080)) # Порт, який дає Render

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ФУНКЦІЇ ---
async def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude=49.8825&longitude=32.2274&current_weather=true"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get("current_weather", {})
                    return round(current.get("temperature", 0)), round(current.get("windspeed", 0)), current.get("weathercode", 0)
    except Exception as e:
        logging.error(f"Помилка погоди: {e}")
    return None

# --- WEB ЗАГЛУШКА ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Бот працює!")

# --- ОСНОВНА ЛОГІКА БОТА ---
@dp.message(Command("poll", "go"))
async def handle_poll(message: types.Message):
    await message.delete()
    options = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "Не йду"]
    await bot.send_poll(
        chat_id=message.chat.id,
        question="Гулять",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

@dp.message(Command("pogoda", "hto"))
async def handle_weather(message: types.Message):
    await message.delete()
    data = await get_weather()
    if data:
        temp, wind, code = data
        # Спрощений вибір емодзі
        emoji = "☀️" if code == 0 else "🌧" if code > 50 else "🌤"
        text = f"📍 Золотоношка\n{emoji}\n🌡 {temp}°C\n💨 {wind} км/год"
        await message.answer(text)
    else:
        await message.answer("❌ Помилка отримання погоди.")

async def main():
    # Запуск веб-сервера (для Render)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Запуск бота
    await bot.set_my_commands([
        BotCommand(command="poll", description="Опитування"),
        BotCommand(command="pogoda", description="Погода")
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
