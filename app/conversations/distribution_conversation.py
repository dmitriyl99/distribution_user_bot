from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from app import actions
from app.core.repositories import distributions

MENU, NAME, DISTRIBUTION_TYPE, INTERVAL_MEASURE, INTERVAL_NUMBER, INTERVAL_COUNT, TEXT = range(7)


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню рассылок", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Список рассылок")],
        [KeyboardButton("Создать рассылку")],
        [KeyboardButton("Включить рассылку"), KeyboardButton("Отключить рассылку")],
        [KeyboardButton("На главную")]
    ], resize_keyboard=True))

    return MENU


async def process_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Создать рассылку':
        context.user_data['new_distribution'] = {}
        await update.message.reply_text("Отправьте название шаблона", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Назад")]
        ], resize_keyboard=True))
        return NAME

    if update.message.text == 'Список рассылок':
        distributions_list = distributions.get_all_distributions()
        measure_mapper = {
            'hour': 'часов',
            'week': 'неделю',
            'day': 'день'
        }
        for distribution in distributions_list:
            if distribution.interval_measure:
                await update.message.reply_html(f"Шаблон <b>{distribution.name}</b>\n\n"
                                                f"Настройки: {distribution.interval_count} раз каждые "
                                                f"{distribution.interval_number} {measure_mapper[distribution.interval_measure]}")
            else:
                await update.message.reply_html(f"Шаблон <b>{distribution.name}</b>\n\n"
                                                f"Рассылка будет отправлена только один раз")

        return MENU

    if update.message.text == 'На главную':
        await actions.send_main_menu(update)
        return ConversationHandler.END

    return MENU


async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Назад':
        await update.message.reply_text("Меню рассылок", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Создать рассылку")],
            [KeyboardButton("Включить рассылку"), KeyboardButton("Отключить рассылку")],
            [KeyboardButton("На главную")]
        ], resize_keyboard=True))

        return MENU

    context.user_data['new_distribution']['name'] = update.message.text

    await update.message.reply_text("Выберите тип рассылки", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Обычная рассылка")],
        [KeyboardButton("Рассылка с повтором")],
        [KeyboardButton("Назад")]
    ], resize_keyboard=True))
    return DISTRIBUTION_TYPE


async def process_distribution_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Обычная рассылка':
        await update.message.reply_text("Отправьте сообщение для рассылки", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Назад")]
        ], resize_keyboard=True))
        return TEXT
    if update.message.text == 'Рассылка с повтором':
        await update.message.reply_text("Выберите время для интервала рассылки", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Час")],
            [KeyboardButton("День")],
            [KeyboardButton("Неделя")],
            [KeyboardButton("Назад")]
        ], resize_keyboard=True))

        return INTERVAL_MEASURE
    if update.message.text == "Назад":
        del context.user_data['new_distribution']
        await update.message.reply_text("Меню рассылок", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Создать рассылку")],
            [KeyboardButton("Включить рассылку"), KeyboardButton("Отключить рассылку")],
            [KeyboardButton("На главную")]
        ], resize_keyboard=True))

        return MENU

    return DISTRIBUTION_TYPE


async def process_interval_measure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text not in ['Час', 'День', 'Неделя', 'Назад']:
        await update.message.reply_text("Выберите корректное действие")
        return INTERVAL_MEASURE
    if update.message.text == 'Назад':
        await update.message.reply_text("Выберите тип рассылки", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Обычная рассылка")],
            [KeyboardButton("Рассылка с повтором")],
            [KeyboardButton("Назад")]
        ], resize_keyboard=True))
        return DISTRIBUTION_TYPE

    measure_mapper = {
        'Час': 'hour',
        'День': 'day',
        'Неделя': 'week',
    }
    context.user_data['new_distribution']['interval_measure'] = measure_mapper[update.message.text]

    await update.message.reply_text("Отправьте нужный интервал времени", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('Назад')]
    ], resize_keyboard=True))

    return INTERVAL_NUMBER


async def process_interval_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Назад':
        await update.message.reply_text("Выберите время для интервала рассылки", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Час")],
            [KeyboardButton("День")],
            [KeyboardButton("Неделя")],
            [KeyboardButton("Назад")]
        ]))

        return INTERVAL_MEASURE
    if not update.message.text.isdigit():
        await update.message.reply_text("Введите корректное число")
        return INTERVAL_NUMBER
    context.user_data['new_distribution']['interval_number'] = int(update.message.text)

    await update.message.reply_text("Отправьте количество повторной рассылки", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('Назад')]
    ], resize_keyboard=True))

    return INTERVAL_COUNT


async def process_interval_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Назад':
        await update.message.reply_text("Отправьте нужный интервал времени", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('Назад')]
        ], resize_keyboard=True))

        return INTERVAL_NUMBER

    if not update.message.text.isdigit():
        await update.message.reply_text("Введите корректное число")

        return INTERVAL_COUNT

    context.user_data['new_distribution']['interval_count'] = int(update.message.text)
    await update.message.reply_text("Отправьте сообщение для рассылки", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Назад")]
    ], resize_keyboard=True))
    return TEXT


async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Назад':
        await update.message.reply_text("Отправьте количество повторной рассылки", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('Назад')]
        ], resize_keyboard=True))

        return INTERVAL_COUNT
    distribution_text = update.message.text
    distribution = distributions.create_distribution(
        context.user_data['new_distribution']['name'],
        context.user_data['new_distribution']['interval_measure'] if 'interval_measure' in context.user_data[
            'new_distribution'] else None,
        context.user_data['new_distribution']['interval_number'] if 'interval_number' in context.user_data[
            'new_distribution'] else None,
        context.user_data['new_distribution']['interval_count'] if 'interval_count' in context.user_data[
            'new_distribution'] else None,
        distribution_text
    )

    measure_mapper = {
        'hour': 'часов',
        'week': 'неделю',
        'day': 'день'
    }

    if distribution.interval_measure:
        await update.message.reply_html(f"Шаблон <b>{distribution.name}</b> создан!\n\n"
                                        f"Настройки: {distribution.interval_count} раз каждые "
                                        f"{distribution.interval_number} {measure_mapper[distribution.interval_measure]}")
    else:
        await update.message.reply_html(f"Шаблон <b>{distribution.name}</b> создан!\n\n"
                                        f"Рассылка будет отправлена только один раз")
    await actions.send_main_menu(update)

    return ConversationHandler.END


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Рассылка'), start_conversation)],
    states={
        MENU: [MessageHandler(filters.TEXT, process_menu)],
        NAME: [MessageHandler(filters.TEXT, process_name)],
        DISTRIBUTION_TYPE: [MessageHandler(filters.TEXT, process_distribution_type)],
        INTERVAL_MEASURE: [MessageHandler(filters.TEXT, process_interval_measure)],
        INTERVAL_NUMBER: [MessageHandler(filters.TEXT, process_interval_number)],
        INTERVAL_COUNT: [MessageHandler(filters.TEXT, process_interval_count)],
        TEXT: [MessageHandler(filters.TEXT, process_text)]
    },
    fallbacks=[MessageHandler(filters.ALL, fallback)]
)
