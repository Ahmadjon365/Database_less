import sqlite3
from contextlib import closing

database_path = "mini_payment.db"

def get_connection():
    return sqlite3.connect(database_path)

def setup_database():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          balance REAL NOT NULL DEFAULT 0)''')
        connection.commit()

def add_user(name):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", (name, 0.0))
        connection.commit()

def deposit(user_id, amount):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
        connection.commit()

def withdraw(user_id, amount):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()
        if balance and balance[0] >= amount:
            cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
            connection.commit()
        else:
            print("Mablag'lar yetarli emas.")

def transfer(from_id, to_id, amount):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE id = ?", (from_id,))
        balance = cursor.fetchone()
        if balance and balance[0] >= amount:
            cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, from_id))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, to_id))
            connection.commit()
        else:
            print("Mablag'lar yetarli emas.")

def display_users():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(user)

def main():
    setup_database()
    while True:
        print("\nMini Payment System Menu:")
        print("1. Foydalanuvchi qo'shish")
        print("2. Depozit qo'shish")
        print("3. Qaytarib olish")
        print("4. Transfer")
        print("5. Foydalanuvchilarni ko'rsatish")
        print("6. Chiqish")
        choice = input("Tanlovingizni kiriting: ")
        
        if choice == "1":
            name = input("Foydalanuvchi ismini kiriting: ")
            add_user(name)
        elif choice == "2":
            user_id = int(input("Foydalanuvchi IDsini kiriting: "))
            amount = float(input("Depozit uchun summani kiriting: "))
            deposit(user_id, amount)
        elif choice == "3":
            user_id = int(input("Foydalanuvchi IDsini kiriting:"))
            amount = float(input("Yechib olinadigan miqdorni kiriting: "))
            withdraw(user_id, amount)
        elif choice == "4":
            from_id = int(input("Yuboruvchi IDsini kiriting: "))
            to_id = int(input("Qabul qiluvchining IDsini kiriting: "))
            amount = float(input("O'tkazish uchun summani kiriting: "))
            transfer(from_id, to_id, amount)
        elif choice == "5":
            print(f"Foydalanuvchilar:\n{display_users()}")
        elif choice == "6":
            print("Chiqilmoqda...")
            break
        else:
            print("Yaroqsiz tanlov. Qayta urinib ko'ring.")

if __name__ == "__main__":
    main()
