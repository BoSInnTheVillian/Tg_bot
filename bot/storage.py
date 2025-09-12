import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import time
from config.config import Config


class Storage:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.products_path = self.base_dir / "data" / "products.json"
        self.carts_path = self.base_dir / "data" / "carts.json"
        self.history_path = self.base_dir / "data" / "chat_history.json"
        self.antispam_path = self.base_dir / "data" / "antispam.json"
        self._init_storage()

    def _init_storage(self):
        """Инициализация файлов данных"""
        (self.base_dir / "data").mkdir(exist_ok=True)

        default_data = {
            self.products_path: [],
            self.carts_path: {},
            self.history_path: {},
            self.antispam_path: {}
        }

        for path, default in default_data.items():
            if not path.exists():
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(default, f, indent=2, ensure_ascii=False)

    # --- Товары ---
    def get_products(self, category: Optional[str] = None) -> List[Dict]:
        """Получить товары (опционально по категории)"""
        with open(self.products_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        if category:
            return [p for p in products if p.get("category") == category]
        return products

    def verify_prices(self, response: str) -> bool:
        """Проверяет точность цен в ответе AI"""
        products = self.get_products()
        for p in products:
            if f'«{p["name"]}»' in response and f'{p["price"]}₽' not in response:
                return False
        return True

    def get_product(self, product_id: int) -> Optional[Dict]:
        """Получить товар по ID"""
        products = self.get_products()
        return next((p for p in products if p["id"] == product_id), None)

    def get_products_in_budget(self, max_price: int) -> list:
        """Возвращает товары в указанном бюджете"""
        return [p for p in self.get_products() if p["price"] <= max_price]

    # --- Корзины ---
    def get_categories(self) -> list:
        """Добавьте этот метод"""
        with open('data/products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
            categories = {p["category"] for p in products}
            return [{"id": i, "name": name} for i, name in enumerate(categories)]

    def get_cart(self, user_id: int) -> Dict:
        """Получить корзину пользователя"""
        with open(self.carts_path, "r", encoding="utf-8") as f:
            carts = json.load(f)
            return carts.get(str(user_id), {"items": [], "created_at": time.time()})

    def save_cart(self, user_id: int, cart_data: Dict):
        """Сохранить корзину"""
        with open(self.carts_path, "r+", encoding="utf-8") as f:
            carts = json.load(f)
            carts[str(user_id)] = cart_data
            f.seek(0)
            json.dump(carts, f, indent=2, ensure_ascii=False)
            f.truncate()

    def add_to_cart(self, user_id: int, item_id: int):
        """Добавить товар в корзину"""
        cart = self.get_cart(user_id)
        if item_id not in cart["items"]:
            cart["items"].append(item_id)
            self.save_cart(user_id, cart)

    def remove_from_cart(self, user_id: int, item_id: int):
        """Удалить товар из корзины"""
        cart = self.get_cart(user_id)
        if item_id in cart["items"]:
            cart["items"].remove(item_id)
            self.save_cart(user_id, cart)

    def clear_cart(self, user_id: int):
        """Очистить корзину"""
        self.save_cart(user_id, {"items": [], "created_at": time.time()})

    # --- История диалогов ---
    def save_chat_history(self, user_id: int, message_data: Dict):
        """Сохранить сообщение в историю"""
        message_data["timestamp"] = time.time()

        with open(self.history_path, "r+", encoding="utf-8") as f:
            history = json.load(f)

            if str(user_id) not in history:
                history[str(user_id)] = []

            history[str(user_id)].append(message_data)
            f.seek(0)
            json.dump(history, f, indent=2, ensure_ascii=False)
            f.truncate()

    def get_chat_history(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Получить историю диалога"""
        with open(self.history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
            user_history = history.get(str(user_id), [])
            return sorted(user_history, key=lambda x: x["timestamp"], reverse=True)[:limit]

    # --- Анти-спам ---
    def get_last_request_time(self, user_id: int) -> Union[float, None]:
        """Получить время последнего запроса"""
        with open(self.antispam_path, "r", encoding="utf-8") as f:
            antispam = json.load(f)
            return antispam.get(str(user_id))

    def save_last_request_time(self, user_id: int, timestamp: float):
        """Обновить время последнего запроса"""
        with open(self.antispam_path, "r+", encoding="utf-8") as f:
            antispam = json.load(f)
            antispam[str(user_id)] = timestamp
            f.seek(0)
            json.dump(antispam, f, indent=2, ensure_ascii=False)
            f.truncate()

    def is_too_frequent(self, user_id: int, interval_sec: int = 30) -> bool:
        """Проверить частоту запросов"""
        last_time = self.get_last_request_time(user_id)
        return last_time and (time.time() - last_time) < interval_sec

    # --- Для SberCloud API ---
    def format_products_for_prompt(self) -> str:
        """Форматирует товары для промпта"""
        products = self.get_products()
        return "\n".join(
            f"ID: {p['id']} | «{p['name']}» ({p['price']}₽) | Категория: {p.get('category', 'без категории')}"
            for p in products
        )