from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from app.core.repositories import users as user_repository
from app.core.services import excel
from app import actions


MENU, UPLOAD = range(2)


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите действие", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Наши подписчики")],
        [KeyboardButton("Загрузить пользователей")],
        [KeyboardButton("Главное меню")]
    ], resize_keyboard=True))

    return MENU


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Наши подписчики':
        users = user_repository.get_all_users()
        if len(users) != 0:
            excel_file_path = excel.generate_users_excel_file(users)
            await update.message.reply_document(open(excel_file_path, 'rb'))
            return MENU
        await update.message.reply_text("В базе ещё нет пользователей")
        return MENU

    if update.message.text == 'Загрузить пользователей':
        await update.message.reply_text("Отправьте excel-файл с пользователями", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Назад")]
        ]))
        return UPLOAD

    if update.message.text == 'Главное меню':
        await actions.send_main_menu(update)
        return ConversationHandler.END


async def process_upload_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text == 'Назад':
        await update.message.reply_text("Выберите действие", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Наши подписчики")],
            [KeyboardButton("Загрузить пользователей")],
            [KeyboardButton("Главное меню")]
        ], resize_keyboard=True))

        return MENU

    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл")
        return UPLOAD

    excel_file = update.message.document
    file = await excel_file.get_file()
    await file.download_to_memory(open('storage/downloaded_excel.xlsx', 'wb'))
    excel.import_excel_file('storage/downloaded_excel.xlsx')

    await update.message.reply_text("Выберите действие", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Наши подписчики")],
        [KeyboardButton("Загрузить пользователей")],
        [KeyboardButton("Главное меню")]
    ], resize_keyboard=True))

    return MENU


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Работа с пользователями"), start_conversation)
    ], states={
        MENU: [MessageHandler(filters.Regex("^(Наши подписчики|Главное меню|Загрузить пользователей)$"), menu)],
        UPLOAD: [MessageHandler(filters.ALL, process_upload_users)],
    },
    fallbacks=[MessageHandler(filters.ALL, fallback)]
)
