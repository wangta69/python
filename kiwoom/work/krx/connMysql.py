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

    def close(self):
        self.conn.close()
