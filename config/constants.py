from enum import Enum

class BotState(Enum):
    MAIN_MENU = 0
    CATALOG = 1
    CART = 2

class Categories(str, Enum):
    SOFAS = "Диваны"
    BEDS = "Кровати"
    TABLES = "Столы"