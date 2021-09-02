import pymysql

# DB 테이블 칼럼대로 만든 객체
class MarketPrices:
    def __init__(self, parent=None):
        self.conn = parent.conn

    def updateMarketPrices(self, code, yyyymm, close, open, high, low, trade_qty):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from market_prices where code=%s and yyyymmdd=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into market_prices ' \
                          '(code, yyyymmdd, close, open, high, low, trade_qty) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                        code, yyyymm, close, open, high, low, trade_qty
                    ))

                    self.conn.commit()
                else:
                    sql = 'update market_prices set ' \
                          'close=%s, ' \
                          'open=%s, ' \
                          'high=%s, ' \
                          'low=%s, ' \
                          'trade_qty=%s ' \
                          'where id=%s'
                    curs.execute(sql, (
                        close, open, high, low, trade_qty, rs['id']
                    ))
                    self.conn.commit()

                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass