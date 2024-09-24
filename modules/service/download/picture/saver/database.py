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
            "db": 'sea'
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
                result = [Image.build(x) for x in content]
                return list(result)

    def delete(self, image_url: str):
        sql = f"delete from picture where url = '{image_url}'"

        with self.__get_connection__() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()

    def delete_batch(self, image_urls: list[str]):
        urls = ''
        for url in image_urls:
            urls += f"'{url}',"

        urls = urls.strip(',')

        sql = f"delete from picture where url in ({urls})"

        with self.__get_connection__() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()

    def __build_insert_sql__(self):
        sql = 'insert into picture(url, file_name, main_url, main_title, sub_url, sub_title) '
        sql += "select %s, %s, %s, %s, %s, %s "
        sql += "from dual where not exists (select 1 from picture where url = %s) "

        return sql

    def insert(self, image: Image):
        sql = self.__build_insert_sql__()

        with self.__get_connection__() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, image)
            connection.commit()

    def insert_by_batch(self, images: list[Image]):
        """
        sql = ''
        for image in images:
            sql += self.__build_insert_sql__(image)
        """
        with self.__get_connection__() as connection:
            with connection.cursor() as cursor:
                cursor.executemany(self.__build_insert_sql__(), [(x.url, x.file_name, x.main_url, x.main_title, x.sub_url, x.sub_title, x.url) for x in images])
            connection.commit()

        print("写入图片信息到数据库")


