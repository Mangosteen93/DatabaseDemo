#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-07-12

import six
import json
import time
from pymongo import MongoClient
from database.base.userdb import UserDB as BaseUserDB


class UserDB(BaseUserDB):
    __collection_name__ = 'user'

    def __init__(self, url, database = 'userdb', user='watcher', passwd=None):
        
	self.conn = MongoClient(url)
        self.conn.admin.command("ismaster")
        self.database = self.conn[database]
        
	collection_name = self.__collection_name__
        self.database[collection_name].ensure_index('name')

    
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

    def get_user(self, name, fields = None):
        collection_name = self.__collection_name__
        ret = self.database[collection_name].find_one({'name': name}, fields)
        if not ret:
            return ret
        return self._parse(ret)


    def insert(self, name, obj={}):
        obj = dict(obj)
        obj['name'] = name
        obj['updatetime'] = time.time()

        return self.update(name, obj = obj)


    def update(self, name, obj={}, **kwargs):
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()

        collection_name = self.__collection_name__
        return self.database[collection_name].update(
            {'name': name},
            {"$set": self._stringify(obj)},
            upsert = True
        )

    def drop(self, name):
        collection_name = self.__collection_name__
        self.database[collection_name].remove({'name': name})
