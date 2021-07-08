import os
import pymysql
import time
from dotenv import load_dotenv, dotenv_values

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
            self.conn.close()



if __name__ == "__main__":
    test = Mysql()
    test.update('445623', 'sload', 44.23, 12345.45)
    pass