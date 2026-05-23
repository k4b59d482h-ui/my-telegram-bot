import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO)

# Твій токен
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Координати Золотоношки
LATITUDE = 49.8825
LONGITUDE = 32.2274

# Функція погоди
async def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get("current_weather", {})
                    temp = round(current.get("temperature", 0))
                    wind = round(current.get("windspeed", 0))
                    code = current.get("weathercode", 0)
                    
                    if code in [0]: emoji = "☀️ Ясно"
                    elif code in [1, 2, 3]: emoji = "🌤 Мінлива хмарність"
                    elif code in [45, 48]: emoji = "🌫 Туман"
                    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: emoji = "🌧 Дощ"
                    elif code in [71, 73, 75, 77, 85, 86]: emoji = "❄️ Сніг"
                    elif code in [95, 96, 99]: emoji = "⛈ Гроза"
                    else: emoji = "☁️ Похмуро"
                    return temp, wind, emoji
    except Exception as e:
        logging.error(f"Помилка погоди: {e}")
    return None

# Функція опитування
async def send_poll_to_chat(chat_id):
    options = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "Не йду"]
    await bot.send_poll(
        chat_id=chat_id,
        question="Гулять",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

# Меню
async def set_main_menu(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="/poll", description="Опитування"),
        BotCommand(command="/pogoda", description="Погода в Золотоношці")
    ])

# Команда /poll
@dp.message(Command("poll", "go"))
async def handle_poll(message: types.Message):
    await message.delete()
    await send_poll_to_chat(message.chat.id)

# Команда /pogoda
@dp.message(Command("pogoda", "hto"))
async def handle_weather(message: types.Message):
    await message.delete()
    data = await get_weather()
    if data:
        temp, wind, emoji = data
        text = f"📍 Золотоношка\n{emoji}\n🌡 {temp}°C\n💨 {wind} км/год"
        await message.answer(text, parse_mode="Markdown")
    else:
        await message.answer("❌ Дані про погоду недоступні.")

async def main():
    await set_main_menu(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
