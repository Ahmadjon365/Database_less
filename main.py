# Transactions - bir nechta SQL so'rovlarini bajarish,
# ishlamay qolsa ROLLBACK bo'lishi.

# ACID - Atomicity, Consistency, Isolation, Durability
# Atomicity - bitta so'rovni bajarishda xatolik bo'lsa, barcha so'rovlarni bekor qilish - Bo'linmaslik.
# Consistency - transaksiyaning qoidalariga amal qilish - Moslik.
# Isolation - bir nechta so'rovlar bajarilayotgan paytda, boshqa so'rovlar bajarilmasligi - Izalatsiya.
# Durability - so'rovlar bajarilganidan keyin, o'zgarishlar saqlanishi - Doimiylik.

# Transactions - ACID prinsiplariga amal qiladi.

import sqlite3

connection = sqlite3.connect('transaction.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (from_user_id) REFERENCES users (id),
    FOREIGN KEY (to_user_id) REFERENCES users (id));
""")

# cursor.execute("INSERT INTO users (name, balance) VALUES ('Alice', 1320)")
# cursor.execute("INSERT INTO users (name, balance) VALUES ('Bob', 2130)")

try:
    cursor.execute("BEGIN transaction")
    cursor.execute("INSERT INTO transactions (from_user_id, to_user_id, amount) VALUES (1, 2, 100)")
    cursor.execute("UPDATE users SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE users SET balance = balance + 100 WHERE id = 2")
    # cursor.execute("END transaction")
    
    connection.commit()

except sqlite3.Error as error:
    print("Error:", error)
    connection.rollback()

cursor.close()
connection.close()
