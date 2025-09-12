from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ContextTypes
from bot.storage import Storage
from bot.keyboards import main_menu_keyboard

db = Storage()

async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    cart = db.get_cart(user_id)
    products = db.get_products()

    # Группируем товары по ID с количеством
    items_count = {}
    for item_id in cart["items"]:
        items_count[item_id] = items_count.get(item_id, 0) + 1

    # Формируем данные для отображения
    cart_items = []
    total = 0
    for item_id, count in items_count.items():
        product = next((p for p in products if p["id"] == item_id), None)
        if product:
            sum_price = product["price"] * count
            cart_items.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "count": count,
                "sum": sum_price
            })
            total += sum_price

    # Форматируем текст сообщения
    text = "🛒 <b>Ваша корзина</b>\n━━━━━━━━━━━━━━\n"
    if not cart_items:
        text += "\n🎈 <i>Корзина пуста</i>\n"
    else:
        for item in cart_items:
            text += (
                f"\n<b>{item['name']}</b>\n"
                f"│\n"
                f"├ Цена: <code>{item['price']}₽</code>\n"
                f"├ Количество: <b>{item['count']}</b>\n"
                f"└ Сумма: <code>{item['sum']}₽</code>\n"
            )
    text += "━━━━━━━━━━━━━━\n"
    text += f"💳 <b>Итого: <code>{total}₽</code></b>"

    # Создаем клавиатуру с кнопками +/-
    keyboard = []
    for item in cart_items:
        keyboard.append([
            InlineKeyboardButton("➖", callback_data=f"decrease_{item['id']}"),
            InlineKeyboardButton(f"{item['name'][:20]}", callback_data=f"item_{item['id']}"),
            InlineKeyboardButton("➕", callback_data=f"increase_{item['id']}")
        ])

    # Добавляем управляющие кнопки
    keyboard.append([
        InlineKeyboardButton("🗑 Очистить корзину", callback_data="clear_cart"),
        InlineKeyboardButton("🛍️ В каталог", callback_data="catalog")
    ])

    keyboard.append([
        InlineKeyboardButton("💳 Оформить заказ", callback_data="checkout")
    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def change_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action, item_id = query.data.split('_')
    item_id = int(item_id)
    user_id = query.from_user.id

    cart = db.get_cart(user_id)

    if action == "increase":
        cart["items"].append(item_id)
        await query.answer(f"Добавлен 1 товар")
    elif action == "decrease":
        for i, cart_item_id in enumerate(cart["items"]):
            if cart_item_id == item_id:
                cart["items"].pop(i)
                await query.answer(f"Удалён 1 товар")
                break

    db.save_cart(user_id, cart)
    await view_cart(update, context)

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    db.save_cart(user_id, {"items": []})
    await update.callback_query.answer("Корзина очищена!")
    await view_cart(update, context)

cart_handlers = [
        CallbackQueryHandler(view_cart, pattern="^view_cart$"),
        CallbackQueryHandler(change_quantity, pattern="^(increase|decrease)_"),
        CallbackQueryHandler(clear_cart, pattern="^clear_cart$")
    ]