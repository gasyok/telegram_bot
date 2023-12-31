import sqlite3
import json


class Macros:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Macros, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "is_initialized"):
            self.db = "data/macros.db"
            self.initialize_db()
            self.is_initialized = True

    def initialize_db(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS macros (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                params TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def get_user_macro(self, user_id):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM macros WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def get_macros_code(self, user_id, name):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT code, params FROM macros WHERE user_id = ? AND name = ?",
            (user_id, name)
        )
        result = cursor.fetchall()
        code, params_json = result[0] if result else (None, None)
        conn.close()
        params = json.loads(params_json) if params_json else None
        return code, params

    def set_user_macro(self, user_id, name, code, params=None):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO macros (user_id, name, code, params) VALUES (?, ?, ?, ?)",
            (user_id, name, code, json.dumps(params)),
        )
        conn.commit()
        conn.close()

    def update_macro_code(self, user_id, name, new_code):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE macros SET code = ? WHERE user_id = ? AND name = ?",
            (new_code, user_id, name),
        )
        conn.commit()
        conn.close()

    def delete_macro(self, user_id, name):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM macros WHERE user_id = ? AND name = ?",
            (user_id, name),
        )
        conn.commit()
        conn.close()


macros = Macros()
