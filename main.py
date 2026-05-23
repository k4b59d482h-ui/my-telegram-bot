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

# Координати Києва для погоди
LATITUDE = 50.4501
LONGITUDE = 30.5234

# Функція отримання погоди через API
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
                    
                    # Підбираємо емодзі під код погоди
                    if code in [0]:
                        emoji = "☀️ Ясно"
                    elif code in [1, 2, 3]:
                        emoji = "🌤 Мінлива хмарність"
                    elif code in [45, 48]:
                        emoji = "🌫 Туман"
                    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
                        emoji = "🌧 Дощ"
                    elif code in [71, 73, 75, 77, 85, 86]:
                        emoji = "❄️ Сніг"
                    elif code in [95, 96, 99]:
                        emoji = "⛈ Гроза"
                    else:
                        emoji = "☁️ Похмуро"
                        
                    return temp, wind, emoji
    except Exception as e:
        logging.error(f"Помилка отримання погоди: {e}")
    return None

# Функція створення опитування
async def send_poll_to_chat(chat_id):
    try:
        options = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "Не йду"]
        await bot.send_poll(
            chat_id=chat_id,
            question="Гулять",
            options=options,
            is_anonymous=False,
            allows_multiple_answers=True
        )
        return True
    except Exception as e:
        logging.error(f"Помилка відправки опитування: {e}")
        return False

# Реєстрація команд у меню Телеграма
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/poll", description="Створити опитування для прогулянки"),
        BotCommand(command="/pogoda", description="Яка погода сьогодні")
    ]
    await bot.set_my_commands(main_menu_commands)

# Реагуємо на команду /poll або /go
@dp.message(Command("poll", "go"))
async def handle_poll_command(message: types.Message):
    poll_sent = await send_poll_to_chat(message.chat.id)
    if poll_sent:
        try:
            await message.delete()
        except Exception as e:
            logging.error(f"Не вдалося видалити команду: {e}")

# Реагуємо на команду /pogoda або /hto
@dp.message(Command("pogoda", "hto"))
async def handle_weather_command(message: types.Message):
    # Видаляємо команду від користувача для чистоти
    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо погоду
    weather_data = await get_weather()
    
    if weather_data:
        temp, wind, emoji = weather_data
        text = (
            f"🌳 *ПРОГНОЗ ПОГОДИ ДЛЯ ПРОГУЛЯНКИ* 🌳\n\n"
            f"Зараз на вулиці: {emoji}\n"
            f"🌡 Температура: *{temp}°C*\n"
            f"💨 Вітер: *{wind} км/год*\n\n"
            f"Думайте, збирайтеся і тикайте `/poll` для зборів! 😉"
        )
    else:
        text = "❌ Не вдалося підтягнути погоду, визирніть у вікно! 😅"
        
    await message.answer(text, parse_mode="Markdown")

async def main():
    await set_main_menu(bot)
    logging.info("Бот запущений і чекає на команди...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
