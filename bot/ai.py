from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from config.gigachat_config import GigaChatConfig

class AIConsultant:
    def __init__(self):
        self.client = GigaChat(
            credentials=GigaChatConfig.AUTH_KEY,
            scope=GigaChatConfig.SCOPE,
            client_id=GigaChatConfig.CLIENT_ID,
            model=GigaChatConfig.MODEL,
            verify_ssl_certs=False
        )
        self._auth()

    def _auth(self):
        """Проверка подключения"""
        try:
            self.client.get_models()
            print("✅ GigaChat: Auth successful")
        except Exception as e:
            print(f"❌ GigaChat auth error: {e}")

    async def get_response(self, user_message: str, context: str = "") -> str:
        try:
            response = self.client.chat(
                Chat(
                    messages=[
                        Messages(
                            role=MessagesRole.SYSTEM,
                            content="Ты консультант мебельного магазина. Отвечай кратко и профессионально."
                        ),
                        Messages(
                            role=MessagesRole.USER,
                            content=f"Контекст: {context}\n\nВопрос: {user_message}"
                        )
                    ]
                )
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"GigaChat error: {e}")
            return "Извините, не могу получить ответ. Попробуйте позже."