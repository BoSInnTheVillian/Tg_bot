from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from bot.storage import Storage

db = Storage()

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(
        "⏳ Платежная система в разработке...",
        show_alert=True
    )

def payment_handlers():
    return [CallbackQueryHandler(checkout, pattern="^checkout$")]