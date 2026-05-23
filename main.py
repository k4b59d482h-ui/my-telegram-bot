import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# Твій токен
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функція створення опитування
async def send_poll_to_chat(chat_id):
    try:
        # Варіанти без "Швидше"
        options = ["16:00", "17:00", "18:00", "19:00", "Пізніше", "Не йду"]
        await bot.send_poll(
            chat_id=chat_id,
            question="Гулять",
            options=options,
            is_anonymous=False,
            allows_multiple_answers=True
        )
        logging.info("Опитування успішно надіслано!")
        return True
    except Exception as e:
        logging.error(f"Помилка відправки опитування: {e}")
        return False

# Реагуємо на команду /poll або /go
@dp.message(Command("poll", "go"))
async def handle_poll_command(message: types.Message):
    # Спочатку надсилаємо опитування в цей чат
    poll_sent = await send_poll_to_chat(message.chat.id)
    
    # Якщо опитування успішно пішло, видаляємо команду користувача
    if poll_sent:
        try:
            await message.delete()
            logging.info(f"Команда /poll від користувача {message.from_user.id} видалена.")
        except Exception as e:
            logging.error(f"Не вдалося видалити повідомлення (можливо, бот не адмін): {e}")

async def main():
    logging.info("Бот запущений і чекає на команду /poll...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
