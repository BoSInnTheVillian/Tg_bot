from telegram.ext import Application
from config.config import Config
from bot.handlers import (
    start_handlers,
    catalog_handlers,
    cart_handlers,
    consultant_handlers
)


def main():
    app = Application.builder().token(Config.BOT_TOKEN).build()
    print("Типы:",
          type(start_handlers),
          type(catalog_handlers),
          type(cart_handlers),
          type(consultant_handlers))
    # Регистрируем все обработчики правильно
    app.add_handlers([
        *start_handlers,  # Распаковываем списки обработчиков
        *catalog_handlers,
        *cart_handlers,
        *consultant_handlers
    ])

    app.run_polling()


if __name__ == "__main__":
    main()