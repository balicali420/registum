from database import Database
import logging

logger = logging.getLogger(__name__)


class DbForms(Database):
    """Some database functions to work with forms."""
    def create_form(self, form_info):
        sql = "INSERT INTO forms(name, geo, channel, posts_type, photo, verif_code, video, username, user_id) VALUES " \
              " ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            form_info[0], form_info[1], form_info[2], form_info[3], form_info[4], form_info[5], form_info[6], form_info[7],
        form_info[8])
        self._write(sql)

    def get_form(self, verif_code):
        sql = "SELECT * FROM forms WHERE verif_code = '{}'".format(verif_code)
        form_info = self._read(sql)
        return form_info

    def get_form_username(self, username):
        sql = "SELECT * FROM forms WHERE username = '{}'".format(username)
        form_info = self._read(sql)
        return form_info

    def get_form_by_id(self, user_id):
        sql = "SELECT * FROM forms WHERE user_id = '{}'".format(user_id)
        form_info = self._read(sql)
        return form_info

    def get_all_forms(self):
        sql = "SELECT * FROM forms"
        all_forms = self._read(sql)
        return all_forms

    def delete_form(self, username, verif_code):
        sql = "DELETE FROM forms WHERE username = '{}' and verif_code = '{}'".format(username, verif_code)
        self._write(sql)

# name, age, address, amount, photo, verif_code, video