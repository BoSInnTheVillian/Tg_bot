import sqlite3

from bot.database import Database

db = Database()

sample_items = [
    (1, "Диван 'Премиум'", "Диваны", 45000, 5, "Угловой диван с механизмом еврокнижка"),
    (2, "Кровать 'Королевская'", "Кровати", 32000, 3, "Двуспальная кровать с ортопедическим основанием")
]

with sqlite3.connect(db.db_path) as conn:
    conn.executemany(
        "INSERT OR REPLACE INTO items VALUES (?, ?, ?, ?, ?, ?)",
        sample_items
    )
    conn.commit()

print("База данных успешно инициализирована!")