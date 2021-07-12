import math
import time
import os
import pymysql
from dotenv import load_dotenv
import pandas as pd

import threading
class Crawling(threading.Thread):
    def __init__(self):
        super().__init__()
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')

    def update(self, jcode, name, q1, q2):
        print(jcode, name, q1, q2)
        if q1 == '-':
            q1 = 0
        if q2 == '-':
            q2 = 0
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, q1, q2 from financeinnfo where jcode=%s limit 0, 1"
                curs.execute(sql, (jcode))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                if rs == None:  # 값이 없을 경우 현재 값 입력
                    sql = 'insert into financeinnfo (jcode, name, q1, q2, created_at, updated_at) values(%s, %s, %s, %s, %s, %s)'
                    print(sql)
                    curs.execute(sql, (
                    jcode, name, q1, q2, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

                    self.conn.commit()
                else:
                    if rs['q2'] == q2:
                        print('SKIP')
                    else:
                        print('UPDATE')
                        sql = 'update financeinnfo set q2=%s, updated_at=%s where id=%s'
                        curs.execute(sql, (q2, time.strftime('%Y-%m-%d %H:%M:%S'), rs['id']))
                        self.conn.commit()
                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            print('')
        #     self.conn.close()

    def run(self):
        df1 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

        df1 = df1[['회사명', '종목코드']]
        df1['종목코드'] = df1['종목코드'].astype(str)
        df1['종목코드'] = df1['종목코드'].apply(lambda x: '00' + str(x) if len(str(x)) == 4 else x)
        df1['종목코드'] = df1['종목코드'].apply(lambda x: '0' + str(x) if len(str(x)) == 5 else x)

        url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
        for i, row in df1.iterrows():
            # code = row['종목코드']
            # name = row['회사명']
            # print(row['회사명'], row['종목코드'], len(row['종목코드']))

            if len(row['종목코드']) == 6:
                url = url_tmpl % (row['종목코드'])
                tables = pd.read_html(url, encoding='euc-kr')
                df = tables[3]
                try:
                    gain = df.iloc[1, 10]
                    privious = df.iloc[1, 9]
                    # if gain != 'nan':
                    if isinstance(gain, float):
                        is_NAN = math.isnan(gain)
                        if not is_NAN:
                            print(row['회사명'], row['종목코드'])
                            print(privious, gain)
                            self.update(row['종목코드'], row['회사명'], privious, gain)
                except IndexError:
                    gain = 'nan'
            time.sleep(1)

