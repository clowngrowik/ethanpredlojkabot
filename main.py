import logging
import asyncio
import re
import gspread
import yt_dlp
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.utils.markdown import hlink




# Замените на ваш токен бота и ID группы
BOT_TOKEN = "7960166180:AAFXC25aFpd1QDPjh1RHM1Buh5d-cmZVocI"
GROUP_ID = -1002291091171  # Не забудь поставить -100 перед ID, если это супергруппа
ADMIN_ID = "1810342367"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем инлайн-клавиатуру с кнопками
menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить видео", callback_data="send_message")],
        [InlineKeyboardButton(text="📢 Соц. сети", callback_data="social"),
         InlineKeyboardButton(text="📝 Заявка", callback_data="request"),
         InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]]
)

# Регулярное выражение для проверки ссылки
url_pattern = re.compile(r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(/.*)?$', re.IGNORECASE)

# Установка подключения к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("../../home/botbb/valued-road-451914-q7-ea6029d14a3b.json", scope)  # Укажите путь к вашему JSON-файлу
client = gspread.authorize(creds)
sheet = client.open("Video").sheet1  # Укажите название таблицы

# Функция для извлечения названия видео с YouTube
def get_video_title(url):
    ydl_opts = {
        'quiet': True,  # Отключаем лишний вывод
        'extract_flat': True  # Извлекаем только метаданные
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            # Получаем название видео
            return result.get('title', 'Название не найдено')
    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        return None


# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    # Отправляем главное меню при старте
    await message.answer("📋 Главное меню:\n\nВыбери нужный пункт:", reply_markup=menu_keyboard)


# Команда /social - отправляет ссылки на соцсети
@dp.message(Command("social"))
async def social_links(message: Message):
    await send_social_links(message)

# Обработчик кнопки "📢 Соц. сети"
@dp.callback_query(lambda c: c.data == "social")
async def social_callback_handler(callback_query: CallbackQuery):
    await edit_message_with_social_links(callback_query.message)
    await callback_query.answer()

async def edit_message_with_social_links(message: Message):
    text = ("📢 Соц. Сети:\n\n"
            "🔹 Telegram: https://t.me/nesamishi\n"
            "🔹 Discord: https://discord.gg/fN727fWYDC\n"
            "🔹 Twitch: https://www.twitch.tv/99samishi\n"
            "🔹 Music: https://band.link/nevermxre03\n"
            "🔹 Steam: https://steamcommunity.com/id/99samishi\n"
            "🔹 YouTube: https://www.youtube.com/@99samishi\n")
    await message.edit_text(text, reply_markup=back_button)


# Обработчик кнопки "ℹ️ О боте"
@dp.callback_query(lambda c: c.data == "about_bot")
async def about_bot_callback_handler(callback_query: CallbackQuery):
    text=("Этот бот для связи со стримером 99samishi")
    await callback_query.message.edit_text(text, reply_markup=back_button)
    await callback_query.answer()



# Обработчик кнопки "Заявка"
@dp.callback_query(lambda c: c.data == "request")
async def request_button_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()  # Удаляем предыдущее сообщение
    
    # Создаем инлайн клавиатуру с кнопкой, ведущей на Google Форму
    form_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к Google Форме", url="https://docs.google.com/forms/d/e/1FAIpQLSet7zCD4iA0_L3Gp3JjvLXIMiuyJl092iiza_VfPbBj8neFtQ/viewform?usp=dialog")]
    ])
    
    # Отправляем сообщение с ссылкой на Google Форму
    message = await callback_query.message.answer(
        "Пожалуйста, заполните заявку по следующей ссылке:",
        reply_markup=form_keyboard
    )
    
    # Удаляем это сообщение через несколько секунд, чтобы оно не висело
    await asyncio.sleep(5)  # Удаляем через 5 секунд
    await message.delete()  # Удаляем сообщение с ссылкой

    # Создаем главное меню с кнопками
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить сообщение", callback_data="send_message")],
        [InlineKeyboardButton(text="📢 Соц. сети", callback_data="social"),
         InlineKeyboardButton(text="📝 Заявка", callback_data="request"),
         InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")]
    ])


# Обработчик кнопки "📨 Отправить сообщение"
@dp.callback_query(lambda c: c.data == "send_message")
async def send_message_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Пожалуйста, отправьте ссылку на видео (YouTube only).",
                                           reply_markup=back_button)
    await callback_query.answer()


# Обработчик кнопки "⬅️ Назад"
@dp.callback_query(lambda c: c.data == "back")
async def back_button_handler(callback_query: CallbackQuery):
    # Заменяем сообщение на главное меню
    await callback_query.message.edit_text("📋 Главное меню:\n\nВыбери нужный пункт:", reply_markup=menu_keyboard)
    await callback_query.answer()

# Функция для проверки наличия ссылки в Google Sheets
def is_link_in_table(link):
    links = sheet.col_values(2)  # Получаем все ссылки из второго столбца
    return link in links


# Пересылка сообщений от пользователя в группу с извлечением названия видео и записью в таблицу
@dp.message(lambda message: not message.text.startswith("/"))
async def forward_to_group(message: Message):
    if message.chat.type == "private":  # Проверяем, что сообщение пришло от пользователя, а не из группы
        user = message.from_user
        username = f"@{user.username}" if user.username else user.full_name
        text = message.text.strip()

        # Проверка, является ли сообщение ссылкой на YouTube
        if "youtube.com" not in text and "youtu.be" not in text:
            await message.answer("Ошибка! Пожалуйста, отправьте ссылку на YouTube.")
            return

        # Проверяем, есть ли ссылка уже в таблице
        if is_link_in_table(text):
            await message.answer("Эта ссылка уже есть в базе данных. Отправьте другую!")
            return

        # Извлекаем название видео с YouTube
        video_title = get_video_title(text)
        if video_title:
            # Форматируем текст для сообщения в группу
            formatted_text = f"Сообщение от {username}\n⇓⇓⇓\nНазвание видео: {video_title}\nСсылка: [смотреть на YouTube]({text})"
            
            # Запись информации о видео в Google Таблицу
            sheet.append_row([video_title, text])  # Записываем название видео и ссылку
            
            # Отправка сообщения в группу с кликабельной ссылкой на YouTube
            sent_message = await bot.send_message(chat_id=GROUP_ID, text=formatted_text, parse_mode="Markdown")
            
            # Ответ пользователю
            await message.answer("Ваша ссылка с названием видео была отправлена!", reply_markup=back_button)
        else:
            await message.answer("Не удалось извлечь название видео. Попробуйте другую ссылку.")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
