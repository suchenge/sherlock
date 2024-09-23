import pymysql

from pymysql.cursors import SSDictCursor

from modules.service.download.picture.saver.base import BaseSaver
from modules.service.download.picture.image import Image


class DatabaseSaver(BaseSaver):
    def __init__(self):
        self.__connect__ = {
            "host": 'localhost',
            "port": 3306,
            "user": 'root',
            "passwd": 'meiyoumima',
            "db": 'scm_global'
        }

    def __get_connection__(self):
        return pymysql.connect(host=self.__connect__["host"],
                               user=self.__connect__["user"],
                               passwd=self.__connect__["passwd"],
                               port=self.__connect__["port"],
                               db=self.__connect__['db'])

    def query(self, main_url) -> list[Image]:
        sql = f"select url, file_name, main_url, main_title, sub_url, sub_title from picture where main_url = '{main_url}'"

        with self.__get_connection__() as connection:
            with connection.cursor(SSDictCursor) as cursor:
                cursor.execute(sql)
                content = cursor.fetchall()
                return [Image.build(x) for x in content]

    def insert_by_batch(self, images: list[Image]):
        sql = "insert into picture(url, file_name, main_url, main_title, sub_url, sub_title)"
        sql += " value "

        index = 0
        for image in images:
            sql += f"('{image.url}', '{image.file_name}', '{image.main_url}', '{image.main_title}', '{image.sub_url}')"

            if index < len(images):
                sql += ", "
            else:
                sql += "; "

            index += 1

        with self.__get_connection__() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()

