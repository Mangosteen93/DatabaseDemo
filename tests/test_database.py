#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from __future__ import unicode_literals, division

import os
import six
import time
import unittest2 as unittest


class TaskDBCase(object):
    sample_task = {
        'taskid': 'taskid',
        'project': 'project',
        'url': 'www.baidu.com/',
        'status': TaskDB.FAILED,
        'schedule': {
            'priority': 1,
            'retries': 3,
            'exetime': 0,
            'age': 3600,
            'itag': 'itag',
            'recrawl': 5,
        },
        'fetch': {
            'method': 'GET'
            'headers': {
                'Cookie': 'a=b'
            },
            'data': 'a=b&c=d',
            'timeout': 60,
        },
        'process': {
            'callback': 'callback',
            'save': [1, 2, 3],
        },
        'track': {
            'fetch': {
                'ok': True,
                'time': 300,
                'status_code': 200,
                'headers': {
                    'Content-Type': 'plain/html',
                },
                'encoding': 'utf8',
                # 'content': 'asdfasdfasdf',
            },
            'process': {
                'ok': False,
                'time': 10,
                'follows': 3,
                'outputs': 5,
                'exception': u"中文",
            },
        },
        'lastcrawltime': time.time(),
        'updatetime': time.time(),
    }

    @classmethod
    def setUpClass(self):
        raise NotImplementedError

    # this test not works for mongodb
    # def test_10_create_project(self):
        # with self.assertRaises(AssertionError):
            # self.taskdb._create_project('abc.abc')
            # self.taskdb._create_project('abc')
            # self.taskdb._list_project()
            # self.assertEqual(len(self.taskdb.projects), 1)
            # self.assertIn('abc', self.taskdb.projects)

    def test_20_insert(self):
        self.taskdb.insert('project', 'taskid', self.sample_task)
        self.taskdb.insert('project', 'taskid2', self.sample_task)

    def test_25_get_task(self):
        task = self.taskdb.get_task('project', 'taskid2')
        self.assertEqual(task['taskid'], 'taskid2')
        self.assertEqual(task['project'], self.sample_task['project'])
        self.assertEqual(task['url'], self.sample_task['url'])
        self.assertEqual(task['status'], self.taskdb.FAILED)
        self.assertEqual(task['schedule'], self.sample_task['schedule'])
        self.assertEqual(task['fetch'], self.sample_task['fetch'])
        self.assertEqual(task['process'], self.sample_task['process'])
        self.assertEqual(task['track'], self.sample_task['track'])

        task = self.taskdb.get_task('project', 'taskid1', fields = ['status'])
        self.assertIsNone(task)

        task = self.taskdb.get_task('project', 'taskid', fields = ['taskid',
            'track', ])
        self.assertIn('track', task)
        self.assertNotIn('project', task)

    def test_30_status_count(self):
        status = self.taskdb.status_count('abc')
        self.assertEqual(status, {})
        status = self.taskdb.status_count('project')
        self.assertEqual(status, {self.taskdb.FAILED: 2})

    def test_40_update_and_status_count(self):
        self.taskdb.update('project', 'taskid', status = self.taskdb.ACTIVE)
        status = self.taskdb.status_count('project')
        self.assertEqual(status, {self.taskdb.ACTIVE: 1, self.taskdb.FAILED: 1})

        self.taskdb.update('project', 'taskid', track = {})
        task = self.taskdb.get_task('project', 'taskid', fields = {'taskid',
            'track'})
        self.assertIn('track', task)
        self.assertEqual(task['track'], {})

    def test_50_load_tasks(self):
        tasks = list(self.taskdb.load_tasks(self.taskdb.ACTIVE))
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        self.assertIn('taskid', task, task)
        self.assertEqual(task['taskid'], 'taskid', task)
        self.assertEqual(task['schedule'], self.sample_task['schedule'])
        self.assertEqual(task['fetch'], self.sample_task['fetch'])
        self.assertEqual(task['process'], self.sample_task['process'])
        self.assertEqual(task['track'], {})

        tasks = list(self.taskdb.load_tasks(self.taskdb.ACTIVE, project =
            'project', fields = ['taskid']))
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['taskid'], 'taskid')
        self.assertNotIn('project', tasks[0])

    def test_60_relist_projects(self):
        if hasattr(self.taskdb, '_list_project'):
            self.taskdb._list_project()
            self.assertNotIn('system.indexes', self.taskdb.projects)

    def test_z10_drop(self):
        self.taskdb.insert('drop_project2', 'taskid', self.sample_task)
        self.taskdb.insert('drop_project3', 'taskid', self.sample_task)
        self.taskdb.drop('drop_project3')
        self.assertIsNotNone(self.taskdb.get_task('drop_project2', 'taskid'),
                None)
        self.assertIsNone(self.taskdb.get_task('drop_project3', 'taskid'), None)

    def test_z20_drop(self):
        saved = getattr(self.taskdb, 'UPDATE_PROJECTS_TIME', None)
        self.taskdb.UPDATE_PROJECTS_TIME = 0.1
        time.sleep(0.2)
        self.assertIn('drop_project2', self.taskdb.projects)
        self.assertNotIn('drop_project3', self.taskdb.projects)
        self.taskdb.UPDATE_PROJECTS_TIME = saved


@unitttest.skipIf(os.environ.get('IGNORE_REDIS') or
        os.environ.get('IGNORE_ALL'), 'no redis server for test.')
class TestRedisTaskDB(TaskDBCase, unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.taskdb =
        database.connect_database('redis+taskdb://localhost:6379/15')
        self.taskdb.__prefix__ = 'testtaskdb_'

    @classmethod
    def tearDownClass(self):
        for project in self.taskdb.projects:
            self.taskdb.drop(project)
