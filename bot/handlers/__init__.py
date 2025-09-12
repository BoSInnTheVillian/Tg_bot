from .start import start_handlers
from .catalog import catalog_handlers
from .cart import cart_handlers
from .consultant import consultant_handlers

# Убедитесь, что это списки, а не функции
__all__ = ['start_handlers', 'catalog_handlers', 'cart_handlers', 'consultant_handlers']