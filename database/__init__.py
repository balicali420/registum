# -*- coding: utf-8 -*-
# Useful functions to handle the database
import psycopg2, psycopg2.extras as psycopg2extras
import logging
import urllib.parse as urlparse
import settings

logger = logging.getLogger(__name__)

_cursor_class = psycopg2extras.DictCursor

# Database info
urlparse.uses_netloc.append('postgres')
_parsed = urlparse.urlparse(settings.database_url)
_conn_string = "host='{}' port='{}' user='{}' password='{}' dbname='{}'".format(_parsed.hostname, _parsed.port, _parsed.username, _parsed.password, _parsed.path[1:])


class Database:
    def __init__(self):
        self.connection = self._connect()
        self.initialized = True

    def __del__(self):
        self.connection.close()

    def _connect(self, connstr=_conn_string):
        # Creates a connection to the database using the given connection string
        return psycopg2.connect(connstr)

    def _write(self, sql, args=tuple()):
        # Executes a query which modifies the database
        if not self.initialized: return []
        try:
            with self.connection.cursor(cursor_factory=_cursor_class) as cursor:
                cursor.execute(sql, args)
            self.connection.commit()
        except Exception as ex:
            logger.error(str(ex))

    def _read(self, sql):
        # Executes a query which doesn't modify the database but returns data
        if not self.initialized: return []
        result = None
        try:
            with self.connection.cursor(cursor_factory=_cursor_class) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception as ex:
            logger.error(str(ex))
        return result
