from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from bot.storage import Storage
from bot.keyboards import (
    items_keyboard,
    main_menu_keyboard,
    product_keyboard,
    back_to_menu_keyboard
)
from typing import Optional

db = Storage()

def end_of_word(time):
    value = time % 10
    if value == 1:
        word = 'день'

    elif value in (2, 3, 4):
        word = 'дня'
    elif value in (5, 6, 7, 8, 9, 0):
        word = 'дней'
    return word




async def show_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        item_id = int(query.data.split('_')[1])
        item = next((i for i in db.get_products() if i['id'] == item_id), None)
        print(item['type'])
        if not item:
            await query.edit_message_text("❌ Услуга не найдена")
            return

        # ФИКС: Для клининга убираем категории
        text = (
            f"🤖 <b>{item.get('name', 'Услуга')}</b>\n\n"
            f"💰 Цена: <code>{item['price']}₽</code>\n"
            f" Срок выполнения {item['time']} {end_of_word(item['time'])}\n"
            f"📝 {item.get('description', 'Нет описания')}"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=product_keyboard(item_id)  # ФИКС: без категории
        )

    except Exception as e:
        await query.edit_message_text(f"⚠️ Ошибка: {str(e)}")

# ФИКС: Убираем show_category так как нет категорий
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        all_items = db.get_products()
        bots = [item for item in all_items if item['type'] == 'товар']
        await query.edit_message_text(
            "🤖 Боты:",
            reply_markup=items_keyboard(bots)
        )
    except Exception as e:
        await query.edit_message_text(f"⚠️ Ошибка загрузки ботов: {str(e)}")

# ФИКС: Обновляем обработчики - убираем category_

async def show_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        all_items = db.get_products()
        options = [item for item in all_items if item['type'] == 'доп-услуга']
        await query.edit_message_text(
            " дополнительные услуги",
            reply_markup=items_keyboard(options)
        )
    except Exception as e:
        await query.edit_message_text(f"⚠️ Ошибка загрузки услуг: {str(e)}")



async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление товара в корзину"""
    query = update.callback_query
    await query.answer()

    try:
        item_id = int(query.data.split('_')[1])
        user_id = query.from_user.id

        db.add_to_cart(user_id, item_id)
        await query.answer("✅ Товар добавлен в корзину!")

        # Обновляем сообщение с товаром
        item = next(i for i in db.get_products() if i['id'] == item_id)
        await query.edit_message_reply_markup(
            reply_markup=product_keyboard(item_id, item['category'])
        )

    except Exception as e:
        await query.answer(f"❌ Ошибка: {str(e)}")

async def ask_consultant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки консультанта"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "💡 Задайте ваш вопрос консультанту...",
        reply_markup=back_to_menu_keyboard()
    )

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ товаров категории"""
    query = update.callback_query
    await query.answer()

    try:
        category = query.data.split('_', 1)[1]
        items = [i for i in db.get_products() if i.get('category') == category]

        if not items:
            await query.edit_message_text(
                f"😕 В категории '{category}' пока нет товаров",
                reply_markup=back_to_menu_keyboard()
            )
            return

        await query.edit_message_text(
            f"🏷️ Товары в категории '{category}':",
            reply_markup=items_keyboard(items)
        )

    except Exception as e:
        await query.edit_message_text(
            f"⚠️ Ошибка: {str(e)}",
            reply_markup=back_to_menu_keyboard()
        )




async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🏠 Главное меню:",
        reply_markup=main_menu_keyboard()
    )


catalog_handlers = [
        CallbackQueryHandler(show_catalog, pattern="^catalog$"),
        CallbackQueryHandler(show_category, pattern="^category_"),
        CallbackQueryHandler(back_to_main, pattern="^to_main_menu$"),
        CallbackQueryHandler(show_item, pattern="^item_"),
        CallbackQueryHandler(add_to_cart, pattern="^add_"),
        CallbackQueryHandler(show_item, pattern="^select_item_"),  # Добавлено
        CallbackQueryHandler(ask_consultant, pattern="^ask_consultant$"),
        CallbackQueryHandler(show_options, pattern="^options")
    ]