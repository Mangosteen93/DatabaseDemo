#!/usr/bin/env python
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# -*- encoding : utf-8  -*-
# Author: Watcher
# Created on 2017-07-12


import six
import time
import json
import redis
import itertools

from libs import utils
from database.base.userdb import UserDB as BaseUserDB

import logging
import logging.config
CONF = 'logging.conf'
logging.config.fileConfig(CONF)
logger = logging.getLogger('database')

class UserDB(BaseUserDB):
    
    __prefix__ = 'user'
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        try:
            self.redis.scan(count=1)
            self.scan_available = True
        except Exception as e:
            logging.debug("redis_scan disabled:%r",e)
            self.scan_available = False

    def _gen_key(self, name):
        return "%s_%s" % (self.__prefix__, name)

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
        if fields:
            obj = self.redis.hmget(self._gen_key(name), fields)
            if all(x is None for x in obj):
                return None
            obj = dict(zip(fields, obj))
        else:
            obj = self.redis.hgetall(self._gen_key(name))
            
        if not obj:
            return None   
        return self._parse(obj)


    def insert(self, name, obj={}):
        obj = dict(obj)
        obj['name'] = name
        obj['updatetime'] = time.time()
        user_key = self._gen_key(name)

        pipe = self.redis.pipeline(transaction = False)
        pipe.sadd('users', name)
        pipe.hmset(user_key, self._stringify(obj))
        pipe.execute()

    def update(self, name, obj={}, **kwargs):
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()
        user_key = self._gen_key(name)

        pipe = self.redis.pipeline(transaction = False)
        pipe.hmset(user_key, self._stringify(obj))
        pipe.execute()

    def drop(self, name):
        self.redis.srem('users', name)

        if self.scan_available:
            scan_method = self.redis.scan_iter
        else:
            scan_method = self.redis.keys

        for each in itertools.tee(scan_method("%s_*" % self.__prefix__), 100):
            each = list(each)
            if each:
                self.redis.delete(*each)
