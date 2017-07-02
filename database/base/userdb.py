#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-07-02


class UserDB(object):

    def get_user(self, name, fields=None):
        raise NotImplementedError

    def insert(self, name, obj={}):
        raise NotImplementedError

    def update(self, name, obj={}, **kwargs):
        raise NotImplementedError

    def drop(self, name):
        raise NotImplementedError

    def copy(self):
        '''
        database should be able to copy itself to create new connection

        it's implemented automatically by pyspider.database.connect_database
        if you are not create database connection via connect_database method,
        you should implement this
        '''
        raise NotImplementedError
