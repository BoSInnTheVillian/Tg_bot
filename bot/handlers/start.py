from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import main_menu_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать! Я бот-справочник, можешь написать мне любой вопрос, по поводу покупки ТГ-бота!",
        reply_markup=main_menu_keyboard()
    )

# Важно: должен быть список, а не функция!
start_handlers = [CommandHandler("start", start)]
