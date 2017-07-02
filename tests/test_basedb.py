#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-07-02

import unittest2 as unittest

from database.basedb import BaseDB
import sqlite3


class SQLiteDB(BaseDB):
    __tablename__ = "test"
    placeholder = "?"

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        cursor = self.conn.cursor()
        cursor.execute(
        '''CREATE TABLE `%s` (id INTEGER PRIMARY KEY
            AUTOINCREMENT, name, age)''' % self.__tablename__
        )


    @property
    def dbcur(self):
        return self.conn.cursor()

class TestBaseDB(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = SQLiteDB()

    @classmethod
    def tearDownClass(self):
        pass

    def test_10_insert(self):
        self.assertEqual(self.db._insert(self.db.__tablename__, name =
            "Watcher", age = 24), 1)
    
    def test_20_select(self):
        self.assertEqual(self.db._select(self.db.__tablename__, "name, \
            age").next(), ("Watcher", 24))

    def test_30_select2dic(self):
        self.assertEqual(self.db._select2dic(self.db.__tablename__, "name, \
            age").next()["name"], "Watcher")
        self.assertEqual(self.db._select2dic(self.db.__tablename__, "name, \
            age").next()["age"], 24)

    def test_40_replace(self):
        self.db._replace(self.db.__tablename__, id = 1, age = 25)
        self.assertEqual(self.db._select(self.db.__tablename__, "name, \
        age").next(), (None, 25))

    def test_50_update(self):
        self.db._update(self.db.__tablename__, "id = 1", age = 16)
        self.assertEqual(self.db._select(self.db.__tablename__, "name, \
        age").next(), (None, 16))

    def test_60_delete(self):
        self.db._delete(self.db.__tablename__, "id = 1")
        self.assertEqual([row for row in
            self.db._select(self.db.__tablename__)], [])

if __name__ == "__main__":
    unittest.main()
