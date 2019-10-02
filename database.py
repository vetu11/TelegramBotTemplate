"""
This class is an interface with the SQLite database.
"""

import sqlite3

DATABASE_PATH = "database.db"


class _DatabaseConnection:

    def __init__(self, path=DATABASE_PATH):
        self.conn = sqlite3.connect(path)

    def __del__(self):
        self.conn.close()


class _Database:

    def __init__(self):
        self._perma_conn = sqlite3.connect(DATABASE_PATH)

    def execute_and_commit(self, sql: str, parameters: iter):
        cursor = self._perma_conn.execute(sql, parameters)
        self._perma_conn.commit()
        return cursor

    @staticmethod
    def get_connection():
        return _DatabaseConnection()

    @staticmethod
    def get_one_fetched_as_dict(cursor):
        desc = cursor.description
        row = cursor.fetchone()
        new_dict = {}

        for i in range(len(row)):
            new_dict[desc[i][0]] = row[i]
        return new_dict

    @staticmethod
    def get_all_fetched_as_dict(cursor):
        desc = cursor.description
        lst = cursor.fetchall()
        fetched = []

        for row in lst:
            new_dict = {}
            for i in range(len(row)):
                new_dict[desc[i][0]] = row[i]
            fetched.append(new_dict)

        return fetched


database = _Database()
