import os
import logging
import asyncio
import pip
import telebot
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from keep_alive import keep_alive

keep_alive()


# Замените на ваш токен бота и ID группы
BOT_TOKEN = "7960166180:AAFXC25aFpd1QDPjh1RHM1Buh5d-cmZVocI"
GROUP_ID = -1002291091171  # Не забудь поставить -100 перед ID, если это супергруппа
ADMIN_ID = "1810342367"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Ку, скинь видос или идею.")


# Команда /social - отправляет ссылки на соцсети
@dp.message(Command("social"))
async def social_links(message: Message):
    text = ("📢 Соц. Сети:\n\n"
            "🔹 Telegram: https://t.me/nesamishi\n"
            "🔹 Discord: https://discord.gg/fN727fWYDC\n"
            "🔹 Twitch: https://www.twitch.tv/99samishi\n"
            "🔹 Music: https://band.link/nevermxre03\n"
            "🔹 Steam: https://steamcommunity.com/id/99samishi\n"
            "🔹 YouTube: https://www.youtube.com/@99samishi\n")
    await message.answer(text,
                         parse_mode="Markdown",
                         disable_web_page_preview=True)


# Пересылка сообщений от пользователя в группу
@dp.message(lambda message: not message.text.startswith("/"))
async def forward_to_group(message: Message):
    if message.chat.type == "private":  # Проверяем, что сообщение пришло от пользователя, а не из группы
        user = message.from_user
        username = f"@{user.username}" if user.username else user.full_name
        text = f"Сообщение от {username}\n⇓⇓⇓\n{message.text}"
        await bot.send_message(chat_id=GROUP_ID, text=text)
        await message.answer(
            "Ваше сообщение было отправлено!\nСпасибо за видео/идею")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
