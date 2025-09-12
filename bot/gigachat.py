from gigachat import GigaChat
from config.config import Config
from bot.storage import Storage
import re


class GigaChatAPI:
    def __init__(self):
        self.client = GigaChat(
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            auth_url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            credentials=Config.GIGACHAT_AUTH,
            client_id=Config.GIGACHAT_CLIENT_ID,
            scope=Config.GIGACHAT_SCOPE,
            verify_ssl_certs=False
        )
        self.db = Storage()

    async def get_response_with_products(self, user_message: str, is_first: bool) -> tuple[str, list]:
        try:
            products = self.db.get_products()
            if not products:
                return "Каталог товаров временно недоступен", []

            prompt = self._build_prompt(user_message, is_first, products)
            response = self.client.chat(prompt).choices[0].message.content
            return self._postprocess_response(response, products)
        except Exception as e:
            return f"Ошибка: {str(e)}", []

    def _build_prompt(self, user_message: str, is_first: bool, products: list) -> str:
        role = "Привратник" if is_first else "Консультант"

        return f"""
        Ты дружелюбный консультант в компании по разработке ботов. Правила:

        {"1. Первое сообщение: строго 'Добро пожаловать! Чем помочь?'" if is_first else ""}
        2. Отвечай естественно и дружелюбно, как живой человек:
           - Без технических комментариев в скобках
           - Без упоминания правил работы
        3. На запросы о товарах:
           - Сначала кратко представь варианты: "У нас есть несколько отличных решений:"
           - Затем перечисли варианты в формате: Ответ на вопрос «Название» (цена₽) - 1-2 преимущества
           - ТОЛЬКО товары из списка:
             {self._format_products(products)}
        4. В конце предложи помощь: "Какой вариант вас интересует?" или "Нужна помощь с выбором?"
        5. На другие вопросы - вежливый ответ по типу: "Извините, я специализируюсь на наших ботах. Могу помочь с выбором подходящего решения!"
        6. Если пользователь не знает, что ему нужно, попроси его описать его нужды.
        7. Запрещено:
           - Добавлять служебные заметки
           - Изобретать несуществующие товары

        Запрос: "{user_message}"
        """

    def _format_products(self, products: list) -> str:
        return "\n".join(f"- «{p['name']}» <code>({p['price']}₽)</code>" for p in products)

    def _postprocess_response(self, response: str, products: list) -> tuple[str, list]:
        if not response or not products:
            return "Не удалось обработать запрос", []

        try:
            clean_response = re.sub(r'\([^)]*\)', '', response).strip()
            clean_response = re.sub(r'\n\s*\n', '\n', clean_response)

            # Стильный заголовок с эмодзи
            styled_response = f"""
    <b>| КОНСУЛЬТАЦИЯ |</b>
    ────────────────
    {clean_response}
    """
            # Улучшенный поиск упомянутых услуг
            found_products = []
            for p in products:
                product_name = p['name']

                # Проверяем разные варианты написания
                if (product_name in clean_response or
                        product_name.lower() in clean_response.lower() or
                        f"«{product_name}»" in clean_response or
                        f"'{product_name}'" in clean_response):
                    found_products.append(p)

            # Добавляем услуги если есть
            if found_products:
                styled_response += "\n🔍 <b>Подходящие услуги:</b>\n"
                for product in found_products[:3]:
                    styled_response += f"│\n├  <b>{product['name']}</b>\n├ 💰 {product['price']}₽\n"


            styled_response += "────────────────"
            return styled_response, found_products[:3]  # Возвращаем стильный ответ

        except Exception as e:
            return f""" <b>| ОШИБКА |</b>
    ────────────────
    ⚠️ Произошла ошибка при обработке запроса
    ────────────────""", []
