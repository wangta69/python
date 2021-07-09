import os
import pymysql
import time
from dotenv import load_dotenv

class Mysql:
    def __init__(self):
        print('My SQL Initialize....')
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')

    def selectTableList(self, _id):
        cur = self.conn.cursor()
        sql = "SELECT id, name, subject, content, created_at FROM bbs WHERE id = %s"
        cur.execute(sql, (str(_id)))

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def selectTableList(self):
        cur = self.conn.cursor()
        sql = "SELECT id, name, subject, content, created_at FROM bbs ORDER BY id desc"
        cur.execute(sql)

        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
        return rows

    def insertTable(self, _name, _subject, _content):
        cur = self.conn.cursor()
        sql = "INSERT INTO bbs (name, subject, content, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (
            _name,
            _subject,
            _content,
            time.strftime('%Y-%m-%d %H:%M:%S'),
            time.strftime('%Y-%m-%d %H:%M:%S')
        ))
        self.conn.commit()
        # cur.close()
        # self.conn.close()

    def updateTable(self, _id, _name, _subject, _content):
        cur = self.conn.cursor()
        sql = """UPDATE bbs SET name = %s, subject = %s, content = %s, updated_at = %s  WHERE id = %s"""
        cur.execute(sql, (_name, _subject, _content, time.strftime('%Y-%m-%d %H:%M:%S'), int(_id)))
        self.conn.commit()

    def deleteTable(self, _id):
        cur = self.conn.cursor()
        sql = """DELETE from bbs WHERE id = %s"""
        cur.execute(sql, str(_id))
        self.conn.commit()

    def selectTableCount(self):
        cur = self.conn.cursor()
        sql = """SELECT count(*) FROM bbs"""
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows[0])
        return rows[0]
