import os
import numpy as np
import pymysql
from dotenv import load_dotenv

#DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')

    def corporations(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, code from corporations"
                curs.execute(sql)

                rs = curs.fetchall()
                return rs
        finally:
            pass

    def updateCorporations(self, id, price):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:

                sql = 'update corporations set '\
                      'stock_price=%s '\
                      'where id=%s'
                curs.execute(sql, (price, id))
                self.conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass


    def close(self):
        self.conn.close()



