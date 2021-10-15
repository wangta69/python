import pymysql

# DB 테이블 칼럼대로 만든 객체
class Earnings:
    def __init__(self, parent):
        self.parent = parent

    def earnings(self, code, data):

        release_dt = data['발표일']
        period_end_dt = data['기말']
        eps = data['주당순이익'] if data['주당순이익'] != '--' else None

        eps_forcast = data['예측'] if data['예측'] != '--' else None
        revenue = data['매출'] if data['매출'] != '--' else None
        revenue_forcast = data['예측.1'] if data['예측.1'] != '--' else None

        # print(code, '발표일:' + release_dt, period_end_dt, 'eps:' + eps, 'eps(예상):' + eps_forcast, '매출:' + revenue, '매출(예상):' + revenue_forcast)
        print(code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast)
        # return
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from earnings where code=%s and period_end_dt=%s limit 0, 1"
                curs.execute(sql, (code, period_end_dt))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into earnings ' \
                          '(code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast))

                    conn.commit()
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
                    conn.commit()
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        except:
            print(curs._last_executed)
            raise
        finally:
            pass