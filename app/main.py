import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from app.settings import settings
from app.conversations import work_with_user_conversation, distribution_conversation
from app import actions


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await actions.send_main_menu(update)


if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.telegram_bot_token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(work_with_user_conversation.conversation_handler)
    application.add_handler(distribution_conversation.conversation_handler)

    application.run_polling()
