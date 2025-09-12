import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GIGACHAT_MODEL = "GigaChat-max"  # Используем максимальную модель
    GIGACHAT_TEMPERATURE = 0.3  # Контроль креативности (0-1)
    GIGACHAT_MAX_TOKENS = 2048
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    GIGACHAT_AUTH = os.getenv("GIGACHAT_AUTH")
    GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
    GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE")