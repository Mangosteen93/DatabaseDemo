#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-06-17


if __name__ == "__main__":
    from database.basedb import BaseDB
    import sqlite3

    class DB(BaseDB):
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

    db = DB()
    assert db._insert(db.__tablename__, name = "Watcher", age = 24) == 1
    assert db._select(db.__tablename__, "name, age").next() == ("Watcher", 24)
    assert db._select2dic(db.__tablename__, "name, age").next()["name"] == "Watcher"
    assert db._select2dic(db.__tablename__, "name, age").next()["age"] == 24
    db._replace(db.__tablename__, id = 1, age = 25)
    assert db._select(db.__tablename__, "name, age").next() == (None, 25)
    db._update(db.__tablename__, "id = 1", age = 16)
    assert db._select(db.__tablename__, "name, age").next() == (None, 16)
    db._delete(db.__tablename__, "id = 1")
    assert [row for row in db._select(db.__tablename__)] == []
