safe_shop.py:
python
Copy code
# safe_shop.py

import requests
import hashlib

class SafeShop:
    def __init__(self):
        self.blacklist_urls = ["sitefraude.com", "scammerstore.net"]
        self.threshold_discount = 0.5 # 50% de desconto como limite

    def verify_website(self, url):
        if any(blacklisted_url in url for blacklisted_url in self.blacklist_urls):
            return False
        else:
            return True

    def analyze_offer(self, price, original_price):
        discount = (original_price - price) / original_price
        if discount > self.threshold_discount:
            return False
        else:
            return True

    def check_fraud_alert(self, url, price, original_price):
        if not self.verify_website(url):
            print("ALERTA: Site suspeito encontrado - possibilidade de fraude.")
        elif not self.analyze_offer(price, original_price):
            print("ALERTA: Oferta suspeita - possível fraude de preço.")
        else:
            print("Nenhuma suspeita de fraude detectada.")
database.py:
python
Copy code
# database.py

import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('safeshop.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT)''')
        self.conn.commit()

    def register_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()

    def authenticate_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        return user is not None
auth.py:
python
Copy code
# auth.py

from database import Database

class Authentication:
    def __init__(self):
        self.db = Database()

    def register(self, username, password):
        self.db.register_user(username, password)

    def login(self, username, password):
        return self.db.authenticate_user(username, password)
main.py:
python
Copy code
# main.py

from safe_shop import SafeShop
from auth import Authentication

def main():
    safe_shop = SafeShop()
    auth = Authentication()

    # Exemplo de registro e login de usuário
    auth.register("usuario1", "senha123")
    logged_in = auth.login("usuario1", "senha123")
    if logged_in:
        print("Usuário autenticado com sucesso!")
    else:
        print("Falha na autenticação.")

    # Exemplo de verificação de site e análise de oferta
    url = "https://example.com"
    price = 100.0
    original_price = 200.0
    safe_shop.check_fraud_alert(url, price, original_price)

if __name__ == "__main__":
    main()

