from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler


async def handle_product_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("product_"):
        product_id = query.data.split("_")[1]
        await query.edit_message_text(
            text=f"Выбран товар ID: {product_id}",
            reply_markup=None
        )
    elif query.data == "open_catalog":
        await query.edit_message_text("📂 Открываю каталог...")
    elif query.data == "back":
        await query.edit_message_text("Возвращаемся...")


callbacks_handlers = [CallbackQueryHandler(handle_product_selection)]