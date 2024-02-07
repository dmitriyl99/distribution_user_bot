from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from app.core.repositories import users as user_repository
from app.core.services import excel
from app import actions


MENU = range(1)


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите действие", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Наши подписчики")],
        [KeyboardButton("Главное меню")]
    ], resize_keyboard=True))

    return MENU


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("menu")
    if update.message.text == 'Наши подписчики':
        users = user_repository.get_all_users()
        if len(users) != 0:
            excel_file_path = excel.generate_users_excel_file(users)
            await update.message.reply_document(open(excel_file_path, 'rb'))
            return MENU
        await update.message.reply_text("В базе ещё нет пользователей")
        return MENU

    if update.message == 'Главное меню':
        await actions.send_main_menu(update)
        return ConversationHandler.END


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Работа с пользователями"), start_conversation)
    ], states={
        MENU: [MessageHandler(filters.Regex("Наши подписчики"), menu)]
    },
    fallbacks=[MessageHandler(filters.ALL, fallback)]
)
