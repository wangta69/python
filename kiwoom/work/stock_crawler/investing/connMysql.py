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
                sql = "select id, code, comp_name, investing_comp_name from corporations where status = 0"
                curs.execute(sql)

                rs = curs.fetchall()
                return rs
        finally:
            pass

    def earnings(self, code, data):
        release_dt = data['발표일']
        period_end_dt = data['기말']
        eps = data['주당순이익'] if data['주당순이익'] != '--' else None
        eps_forcast = data['예측'] if data['예측'] != '--' else None
        revenue = data['매출'] if data['매출'] != '--' else None
        revenue_forcast = data['예측.1'] if data['예측.1'] != '--' else None
        print(release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from earnings where code=%s and period_end_dt=%s limit 0, 1"
                curs.execute(sql, (code, period_end_dt))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into earnings ' \
                          '(code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update earnings set ' \
                          'release_dt=%s, ' \
                          'eps=%s, ' \
                          'eps_forcast=%s, ' \
                          'revenue=%s, ' \
                          'revenue_forcast=%s ' \
                          'where id=%s'
                    curs.execute(sql, (release_dt, eps, eps_forcast, revenue, revenue_forcast, rs['id']))
                    self.conn.commit()
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateInvestingCompname(self, id, eng):

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:

                    sql =   'UPDATE  corporations ' \
                            'SET     investing_comp_name = %s ' \
                            'WHERE   id = %s'

                    curs.execute(sql, (eng, id))
                    self.conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    # def updateInvestingCompname(self, kor, eng):
    #
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'UPDATE  corporations ' \
    #                   'SET     investing_comp_name = %s ' \
    #                   'WHERE   comp_name = %s'
    #
    #             curs.execute(sql, (eng, kor))
    #             self.conn.commit()
    #     except:
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    def close(self):
        self.conn.close()



