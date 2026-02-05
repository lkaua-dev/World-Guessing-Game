import sqlite3 as sql
import os

class DatabaseManager:
    def __init__(self, db_name="paises_game.db"):
        self.db_name = db_name
        self.setup_database()

    def get_connection(self):
        return sql.connect(self.db_name)

    def setup_database(self):
        if os.path.exists(self.db_name):
            try:
                conn = self.get_connection()
                conn.execute("SELECT nome FROM paises LIMIT 1")
                conn.close()
            except:
                os.remove(self.db_name)

        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                capital TEXT,
                regiao TEXT,
                bandeira_url TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador TEXT,
                pontos INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def is_empty(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM paises")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0

    def add_country(self, nome, capital, regiao, bandeira_url):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paises (nome, capital, regiao, bandeira_url) VALUES (?, ?, ?, ?)",
            (nome, capital, regiao, bandeira_url),
        )
        conn.commit()
        conn.close()

    def get_random_country(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nome, capital, regiao, bandeira_url FROM paises ORDER BY RANDOM() LIMIT 1"
        )
        data = cursor.fetchone()
        conn.close()
        return data

    def save_score(self, jogador, pontos):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ranking (jogador, pontos) VALUES (?, ?)",
            (jogador, pontos),
        )
        conn.commit()
        conn.close()

    def get_top_ranking(self, limit=5):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT jogador, pontos FROM ranking ORDER BY pontos DESC LIMIT ?", (limit,))
        data = cursor.fetchall()
        conn.close()
        return data