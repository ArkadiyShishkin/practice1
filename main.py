import asyncio
import os
import logging

# Для работы необходима библиотека aiogram

# Библиотеки для работы с Telegram (aiogram 3.x)
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Импорт логики из bot_logic.py
from bot_logic import SevmashBotLogic

# Загрузка токена из файла bot-token.env
# В файле bot-token.env нет настоящего токена! Я создал его для примера.
# Токен можно получить у @BotFather в телеграме. Можно вписать его прямо в код, но лучше хранить отдельно.
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Проверка, что токен нашелся
if not TOKEN:
    print("Ошибка: Токен не найден! Убедитесь, что файл .env создан и содержит BOT_TOKEN.")
    exit()

# Инициализация объектов
# Включаем логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
sevmash_brain = SevmashBotLogic() # Создаем экземпляр логики

# Обработчики событий

# Обработка команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Получаем ответ на приветствие из логики
    response = sevmash_brain.get_response("старт")
    await message.answer(response)

# Обработка любых текстовых сообщений
@dp.message(F.text)
async def handle_text(message: types.Message):
    user_text = message.text
    # Отправляем текст в "мозги" и получаем ответ
    bot_response = sevmash_brain.get_response(user_text)
    await message.answer(bot_response)

#Функция запуска
async def main():
    print("--- Бот АО «ПО «Севмаш» запущен и готов к работе ---")
    # Удаляем вебхуки и запускаем опрос (polling)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")