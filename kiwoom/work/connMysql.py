import os
import pymysql
import time
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

    def update(self, jcode, name, q1, q2):
        print(jcode, name, q1, q2)
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, q1, q2 from financeinnfo where jcode=%s limit 0, 1"
                curs.execute(sql, (jcode))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None: # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinnfo (jcode, name, q1, q2, created_at, updated_at) values(%s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (jcode, name, q1, q2, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

                    self.conn.commit()
                else:
                    print('EXIST')
                    print(rs['q2'], q2)
                    if rs['q2'] == q2:
                        print('SKIP')
                    else:
                        print('UPDATE')
                        sql = 'update financeinnfo set q2=%s, updated_at=%s where id=%s'
                        curs.execute(sql, (q2, time.strftime('%Y-%m-%d %H:%M:%S'), rs['id']))
                        self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass
            # self.conn.close()

    def financeinfos(self):
        cur = self.conn.cursor()
        sql = "SELECT id, jcode, name, q1, q2, created_at, updated_at FROM financeinnfo ORDER BY id desc"
        cur.execute(sql)

        rows = cur.fetchall()
        return rows

    def updateCorporations(self, market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, code from corporations where code=%s limit 0, 1"
                curs.execute(sql, (code))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into corporations ' \
                          '(market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region, created_at, updated_at) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                    market, str(code), comp_name, industry, products, listed_at, sett_month, ceo, url, region,
                    time.strftime('%Y-%m-%d %H:%M:%S'),
                    time.strftime('%Y-%m-%d %H:%M:%S')))

                    self.conn.commit()
                else:
                    sql = 'update corporations set '\
                          'market=%s, '\
                          'comp_name=%s, '\
                          'industry=%s, '\
                          'products=%s, '\
                          'listed_at=%s, '\
                          'sett_month=%s, '\
                          'ceo=%s, '\
                          'url=%s, '\
                          'region=%s, '\
                          'updated_at=%s '\
                          'where id=%s'
                    curs.execute(sql, (
                        market, comp_name, industry, products, listed_at, sett_month, ceo, url, region, time.strftime('%Y-%m-%d %H:%M:%S'), rs['id']))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass



    def corporations(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code, comp_name from corporations"
                curs.execute(sql)

                rs = curs.fetchall()
                return rs
        finally:
            pass

    def codeFromCompName(self, comp_name):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                # sql = "select comp_name from corporations"
                # curs.execute(sql)
                sql = "select code from corporations where comp_name=%s limit 0, 1"
                curs.execute(sql, (comp_name))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    return ''
                else:
                    return rs['code']
        finally:
            pass

    def close(self):
        self.conn.close()
