"""
This class is a set of helper methods for the SQLite database.
"""

import sqlite3

DATABASE_PATH = "database.db"


class _Database:

    @staticmethod
    def get_connection():
        return sqlite3.connect(DATABASE_PATH)

    @staticmethod
    def get_one_fetched_as_dict(cursor):
        desc = cursor.description
        row = cursor.fetchone()
        new_dict = {}

        if row is not None:
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
