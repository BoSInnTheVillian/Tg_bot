from typing import Set

_GREETED_CHATS: Set[int] = set()

def is_first_message(chat_id: int) -> bool:
    if chat_id not in _GREETED_CHATS:
        _GREETED_CHATS.add(chat_id)
        return True
    return False

def reset_session(chat_id: int) -> None:
    _GREETED_CHATS.discard(chat_id)