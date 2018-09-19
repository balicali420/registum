# -*- coding: utf-8 -*-

from database import Database


class DbUsers(Database):
    """Some functions to work with users."""
    def get_single(self, user_id):
        sql = "SELECT * FROM users WHERE user_id = '{}'".format(user_id)
        user = self._read(sql)
        return None if len(user) == 0 else user

    def get_all(self):
        sql = "SELECT * FROM users;"
        users = self._read(sql)
        return list(users)

    def get_count(self):
        sql = "SELECT COUNT(*) FROM users;"
        count_users = self._read(sql)
        users_count = []
        for user in count_users:
            users_count.append(user[0])
        return users_count[0]

    def add_new(self, user):
        sql = "INSERT INTO users(user_id, username, first_name, last_name) VALUES (%s, %s, %s, %s);"
        self._write(sql, (int(user[0]), user[1], user[2], user[3]))
