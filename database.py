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
        self._perma_conn.execute(sql, parameters)
        self._perma_conn.commit()

    @staticmethod
    def get_connection():
        return _DatabaseConnection()


database = _Database()
