import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# Твій токен
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функція створення опитування з новими годинами
async def send_poll_to_chat(chat_id):
    try:
        # Оновлений список часу без зайвих слів
        options = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "Не йду"]
        await bot.send_poll(
            chat_id=chat_id,
            question="Гулять",
            options=options,
            is_anonymous=False,
            allows_multiple_answers=True
        )
        logging.info("Опитування з годинами успішно надіслано!")
        return True
    except Exception as e:
        logging.error(f"Помилка відправки опитування: {e}")
        return False

# Реагуємо на команду /poll або /go
@dp.message(Command("poll", "go"))
async def handle_poll_command(message: types.Message):
    # Надсилаємо нове опитування
    poll_sent = await send_poll_to_chat(message.chat.id)
    
    # Видаляємо команду користувача для чистоти чату
    if poll_sent:
        try:
            await message.delete()
            logging.info(f"Команда /poll видалена з чату.")
        except Exception as e:
            logging.error(f"Бот не зміг видалити повідомлення. Перевір права на видалення! {e}")

async def main():
    logging.info("Бот запущений із новим списком годин і чекає на /poll...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
