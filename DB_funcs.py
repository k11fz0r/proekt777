import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("accountstg.db")
        self.cursor = self.conn.cursor()

    def user_find(self, user_id: int):
        result = self.cursor.execute('SELECT id FROM users WHERE user_id = ?', (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id: int):
        self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        self.conn.commit()

    def search_city(self, user_id: int):
        result = self.cursor.execute('SELECT City FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()

    def change_city(self, user_id: int, city: str):
        self.cursor.execute('UPDATE users SET City = ? WHERE user_id = ?', (city, user_id))
        self.conn.commit()

    def find_pharmacy(self, user_id: int):
        result = self.cursor.execute('SELECT Apteka FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()

    def change_pharmacy(self, user_id: int, Apteka: str):
        self.cursor.execute('UPDATE users SET Apteka = ? WHERE user_id = ?', (Apteka, user_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

