#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Watcher
# Created on 2017-06-17

from six.moves.urllib.parse import urlparse, parse_qs

def connect_database(url):
    """
    create database object by url

    mysql:
        mysql+type://user:passwd@host:port/database
    redis:
        redis+taskdb://host:port/db
    mongodb:
        mongodb+type://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        more: http://docs.mongodb.org/manual/reference/connection-string/

    type:
        user
    """

    db = _connect_database(url)
    db.copy = lambda: _connect_database(url)
    return db

def _connect_database(url):
    parsed = urlparse(url)

    scheme = parsed.scheme.split('+')
    if len(scheme) == 1:
        raise Exception('wrong scheme format: %s', parsed.scheme)
    else:
        engine, dbtype = scheme[0], scheme[-1]
        other_scheme = "+".join(scheme[1:-1])

    dbtypes = ('user', )
    if dbtype not in dbtypes:
        raise LookupError('unknown database type: %s', dbtype)
    if engine == 'mysql':
        params = {}
        if parsed.username:
            params['user'] = parsed.username
        if parsed.password:
            params['passwd'] = parsed.password
        if parsed.hostname:
            params['host'] = parsed.hostname
        if parsed.port:
            params['port'] = parsed.port
        if parsed.path.strip('/'):
            params['database'] = parsed.path.strip('/')

        if dbtype == 'user':
            from database.mysql.userdb import UserDB
            return UserDB(**params)
        else:
            raise LookupError
    elif engine == 'redis':
        from database.redis.userdb import UserDB
        return UserDB(parsed.hostname, parsed.port, int(parsed.path.strip('/') or 0))
    elif engine == 'mongodb':
        url = url.replace(parsed.scheme, 'mongodb')
        params = {}
	if parsed.username:
	    params['user'] = parsed.username
	if parsed.password:
	    params['passwd'] = parsed.password
        if parsed.path.strip('/'):
            params['database'] = parsed.path.strip('/')

        from database.mongodb.userdb import UserDB
        return UserDB(url, **params)
    else:
        raise Exception('unknown engine: %s' % engine)
