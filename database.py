"""
This class is an interface with the SQLite database.
"""

import sqlite3


class _Database:

    def __init__(self):
        self.conn = sqlite3.connect("database.db")

    def execute_and_commit(self, sql: str, parameters: iter):
        self.conn.execute(sql, parameters)
        self.conn.commit()


database = _Database()
