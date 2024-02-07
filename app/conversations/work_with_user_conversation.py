from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters


DOWNLOAD, ENABLE_DISTRIBUTION, DISABLE_DISTRIBUTION = range(3)


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("")


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Работа с пользователями"), start_conversation)
    ], states={

    },
    fallbacks=[MessageHandler(filters.ALL, fallback)]
)
