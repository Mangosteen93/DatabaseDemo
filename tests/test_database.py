#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-07-02

import time
import unittest2 as unittest
import os

import database

class UserDBCase(object):
    sample_user = {
        'id': '1',
        'name': 'Watcher',
        'age': '24',
        'job': 'coder',
        'email': [
            "214461193@qq.com",
            "liubo214461193@gmail.com"
        ],
        'school': {
            'name': 'BIT',
            'address': u'北京市海淀区中关村南大街5号'
        },
        'createtime': time.time(),
        'updatetime': time.time(),
    }

    @classmethod
    def setUpClass(self):
        raise NotImplemented

    def test_10_insert(self):
        self.userdb.insert('Watcher', self.sample_user)

    def test_20_get_user(self):
        user = self.userdb.get_user('Watcher')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.sample_user)

    def test_30_update(self):
        self.userdb.update('Watcher', age = 25)

    def test_40_check_update(self):
        user = self.userdb.get_user('Watcher')
        self.assertIsNotNone(user)
        self.assertEqual(user['age'], 25)


@unittest.skipIf(os.environ.get('IGNORE_MYSQL') or os.environ.get('IGNORE_ALL'), 'no mysql server for test.')
class TestMysqlUserDB(UserDBCase, unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.userdb = database.connect_database('mysql+user://root:LiuBo678621@localhost:33306/databasedemo_test_userdb')

    @classmethod
    def tearDownClass(self):
        self.userdb._execute('DROP DATABASE databasedemo_test_userdb')


if __name__ == '__main__':
    unittest.main()
