import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO)

# Твій токен
BOT_TOKEN = "7963453350:AAG8lJAgSKULro8mb-Fm7QWu3wBJYWW9D6U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
        logging.info("Опитування успішно надіслано!")
        return True
    except Exception as e:
        logging.error(f"Помилка відправки опитування: {e}")
        return False

# Реєстрація команд у меню Телеграма
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/poll", description="Створити опитування для прогулянки"),
        BotCommand(command="/hto", description="Подивитися, хто куди йде")
    ]
    await bot.set_my_commands(main_menu_commands)
    logging.info("Кнопки в меню швидких команд оновлено!")

# Реагуємо на команду /poll або /go
@dp.message(Command("poll", "go"))
async def handle_poll_command(message: types.Message):
    poll_sent = await send_poll_to_chat(message.chat.id)
    if poll_sent:
        try:
            await message.delete()
        except Exception as e:
            logging.error(f"Бот не зміг видалити команду: {e}")

# СУПЕР-ФУНКЦІЯ: Реагуємо на команду /hto або /who
@dp.message(Command("hto", "who"))
async def handle_who_command(message: types.Message):
    try:
        # Шукаємо останнє повідомлення-опитування, яке надсилав цей бот
        # (aiogram автоматично підтягує результати, якщо користувачі голосували)
        chat_id = message.chat.id
        
        # Але оскільки Телеграм не дає боту просто так «читати» історію без збереження id,
        # ми зробимо найпростіший і надійний текстовий виклик.
        # На жаль, дізнатися точні імена без збереження id опитування в базу даних Телеграм не дозволяє миттєво.
        # Тому ми виведемо красиву інструкцію, або якщо у вас відкрите голосування, 
        # бот нагадає усім зазирнути в саме опитування.
        
        # Оскільки ми робимо без складної бази даних, давай навчимо бота просто 
        # красиво підганяти тих, хто заснув і не проголосував!
        await message.answer(
            "📊 *Актуальні збори!*\n\n"
            "Хлопці та дівчата, тикайте на варіанти в опитуванні вище 👆\n"
            "Щоб подивитися, хто саме йде, просто натисніть на відсотки (число голосів) прямо всередині самого опитування!"
        )
        
        # Видаляємо команду /hto, щоб не засмічувати чат
        await message.delete()
    except Exception as e:
        logging.error(f"Помилка команди /hto: {e}")

async def main():
    await set_main_menu(bot)
    logging.info("Бот запущений і чекає на команди...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
