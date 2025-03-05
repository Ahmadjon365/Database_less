import sqlite3
from contextlib import closing
from abc import ABC, abstractmethod

database_path = "sample-database (5).db"


def get_connection(database_path):
    return closing(sqlite3.connect(database_path))


def get_employee(database_path, employee_id):
    with get_connection(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
        return cursor.fetchone()


def create_employee(database_path, first_name, last_name, email):
    with get_connection(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employees (first_name, last_name,email) VALUES (?, ?,?)",
                       (first_name, last_name, email))
        connection.commit()
        return cursor.lastrowid


emp_id = create_employee(database_path, "Akmal", "Tohirov", "akmal@mail.ru")
print(emp_id)

#_____________________________________________________________________________________________________________

class BaseCRUD(ABC):
    def __init__(self, database_path, table_name):
        self.database_path = database_path
        self.table_name = table_name

    def get_connection(self):
        return closing(sqlite3.connect(self.database_path))

    def insert(self, **kwargs):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            columns = ', '.join(kwargs.keys())
            placeholders = ', '.join('?' for _ in kwargs)
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(kwargs.values()))
            connection.commit()
            return cursor.lastrowid

    def get(self, id, id_column="id"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE {id_column}=?"
            cursor.execute(query, (id,))
            return cursor.fetchone()

    def update(self, id, id_column="id", **kwargs):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            columns = ', '.join(f"{key}=?" for key in kwargs)
            query = f"UPDATE {self.table_name} SET {columns} WHERE {id_column}=?"
            cursor.execute(query, (*kwargs.values(), id))
            connection.commit()

    def delete(self, id, id_column="id"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE {id_column}=?"
            cursor.execute(query, (id,))
            connection.commit()


employee_crud = BaseCRUD("sample-database (5).db", "employees")
employee_id = employee_crud.insert(first_name="John", last_name="Doe", email="qwasar@mail.ru")
employee = employee_crud.get(id=101, id_column="employee_id")
print(employee)
# employee_crud.update(employee_id, bio="An updated bio")
# employee_crud.delete(employee_id)
