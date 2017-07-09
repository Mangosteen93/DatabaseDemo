#!/usr/bin/envutils
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-07-02

import six
import time
import json
import mysql.connector

from libs import utils
from database.base.userdb import UserDB as BaseUserDB
from database.basedb import BaseDB
from database.mysql.mysqlbase import MySQLMixin


class UserDB(MySQLMixin, BaseUserDB, BaseDB):
    __tablename__ = 'user'

    def __init__(self, host='localhost', port=3306, database='userdb',
                 user='watcher', passwd=None):
        self.database_name = database
        self.conn = mysql.connector.connect(user=user, password=passwd,
                                            host=host, port=port, autocommit=True)
        if database not in [x[0] for x in self._execute('show databases')]:
            self._execute('CREATE DATABASE %s' % self.escape(database))
        self.conn.database = database

        tablename = self.__tablename__
        if tablename not  in [x[0] for x in self._execute('show tables')]:
            self._execute('''CREATE TABLE IF NOT EXISTS %s (
                `id` varchar(64) PRIMARY KEY,
                `name` varchar(64),
                `age` int(2),
                `job` varchar(64),
                `email` TEXT,
                `school` TEXT,
                `createtime` double(16, 4),
                `updatetime` double(16, 4)
                ) ENGINE=InnoDB CHARSET=utf8''' % self.escape(tablename))

    def _parse(self, data):
        for key, value in list(six.iteritems(data)):
            if isinstance(value, (bytearray, six.binary_type)):
                data[key] = utils.text(value)
        for each in ('email', 'school'):
            if each in data:
                if data[each]:
                    data[each] = json.loads(data[each])
                else:
                    data[each] = {}
        return data

    def _stringify(self, data):
        for each in ('email', 'school'):
            if each in data:
                data[each] = json.dumps(data[each])
        return data

    def get_user(self, name, fields=None):
        where = "`name` = %s" % self.placeholder
        tablename = self.__tablename__
        for each in self._select2dic(tablename, what=fields, where=where,
                where_values=(name, )):
            return self._parse(each)
        return None

    def insert(self, name, obj={}):
        obj = dict(obj)
        obj['name'] = name
        obj['updatetime'] = time.time()
        tablename = self.__tablename__
        return self._insert(tablename, **self._stringify(obj))

    def update(self, name, obj={}, **kwargs):
        tablename = self.__tablename__
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()
        return self._update(
            tablename,
            where="`name` = %s" % self.placeholder,
            where_values=(name, ),
            **self._stringify(obj)
        )
