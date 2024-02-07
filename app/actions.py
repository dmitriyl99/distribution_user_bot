from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


async def send_main_menu(update: Update):
    await update.message.reply_text("Главное меню", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Работа с пользователями")],
        [KeyboardButton("Рассылка")],
        [KeyboardButton("Настройки")]
    ], resize_keyboard=True))
