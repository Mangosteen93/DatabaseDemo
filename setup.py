#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unxi fenc=utf8:
# Author: Watcher
# Created on 2017-06-17

from setuptools import setup, find_packages

setup(
    name = "databasedemo",
    version = "1.0",
    keywords = ("database", "demo", "mysql", "mongodb", "redis", "localfile",
        "sqlite", "elasticsearch", "sqlalchemy"),
    description = "a demo for connecting variable databaes using python",
    long_description = "a demo for connecting variable databases using python",
    license = "Apache License, Version 2.0",
    url = "",
    author = "Watcher",
    author_email = "",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    scripts = [],
    entry_points = {}
    #entry_points = {
    #    'console_scripts': [
    #    'test = test.help:main'
    #    ]
    #}
)
