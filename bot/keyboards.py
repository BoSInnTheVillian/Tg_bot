from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from random import choice

THEMES = {
    "main": ["🛋️", "🏠", "✨"],
    "catalog": ["🛒", "📦", "📌"],
    "cart": ["💰", "🛍️", "🧾"],
    "payment": ["💳", "💎", "🪙"]
}

def _random_emoji(section):
    return choice(THEMES[section])

def consultant_products_keyboard(products: list):
    """Клавиатура для товаров консультанта (3 кнопки + возврат)"""
    buttons = [
        [InlineKeyboardButton(
            f"📌 {p['name']} ({p['price']}₽)",
            callback_data=f"item_{p['id']}"
        )]
        for p in products[:3]  # Ограничиваем 3 товарами
    ]
    buttons.append([
        InlineKeyboardButton("🔙 В главное меню", callback_data="to_main_menu")
    ])
    return InlineKeyboardMarkup(buttons)

def main_menu_keyboard():
    emoji = _random_emoji("main")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🤖 Боты", callback_data="catalog")],
        [InlineKeyboardButton(f"➕ Дополнительные услуги", callback_data="options")],
        [InlineKeyboardButton(f"❔ Ваши вопросы", callback_data="ask_consultant")]
    ])

def back_to_menu_keyboard():
    """Клавиатура с кнопкой возврата в главное меню"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Главное меню", callback_data="to_main_menu")]
    ])
def calculation_keyboard():
    """Клавиатура с кнопкой возврата в главное меню"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Главное меню", callback_data="to_main_menu")]
    ])

def items_keyboard(items: list):
    buttons = [
        [InlineKeyboardButton(
            f" {item['name']} - 🟡{item['price']}₽🟡",

            callback_data=f"item_{item['id']}"
        )]
        for item in items
    ]
    buttons.extend([
        [InlineKeyboardButton("🔙 В главное меню", callback_data="to_main_menu")]
    ])
    return InlineKeyboardMarkup(buttons)

def product_keyboard(item_id: int):
    """ФИКС: Для клининга без категорий"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 В главное меню", callback_data="to_main_menu")]
    ])
def cart_keyboard(cart_items: list):
    buttons = []
    for item in cart_items:
        buttons.extend([
            [
                InlineKeyboardButton("➖", callback_data=f"decrease_{item['id']}"),
                InlineKeyboardButton(f"{item['name'][:15]}", callback_data=f"item_{item['id']}"),
                InlineKeyboardButton("➕", callback_data=f"increase_{item['id']}")
            ]
        ])

    buttons.extend([
        [
            InlineKeyboardButton("🗑 Очистить корзину", callback_data="clear_cart"),
            InlineKeyboardButton("🛍️ В каталог", callback_data="catalog")
        ],
        [InlineKeyboardButton("💳 Оформить заказ", callback_data="checkout")]
    ])
    return InlineKeyboardMarkup(buttons)