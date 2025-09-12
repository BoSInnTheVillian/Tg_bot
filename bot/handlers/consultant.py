from telegram import Update
from bot.gigachat import GigaChatAPI
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,  # Добавляем этот импорт
    MessageHandler,
    filters,
    ConversationHandler
)

#from bot.handlers.calculator import CALCULATING, start_calculation
from bot.keyboards import consultant_products_keyboard, calculation_keyboard
from bot.session import is_first_message

giga = GigaChatAPI()  # Инициализация здесь!


async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    if not update.message or not update.message.text:
        return

    chat_id = update.message.chat_id
    user_message = update.message.text

    try:
        response, products = await giga.get_response_with_products(
            user_message=user_message,
            is_first=is_first_message(chat_id)
        )
        await update.message.reply_text(
            text=response,
            parse_mode="HTML",
            reply_markup=consultant_products_keyboard(products)
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")






# Явно экспортируем обработчики
consultant_handlers = [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)]