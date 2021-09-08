import pymysql

# DB 테이블 칼럼대로 만든 객체
class MarketPrices:
    def __init__(self, parent=None):
        self.conn = parent.conn

    def prices(self, code, limit):
        """
        업체별 가격 리스트를 가져온다.
        :return:
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select yyyymmdd, open, high, low, close from market_prices where code = %s order by yyyymmdd desc limit 0, %s"
                curs.execute(sql, (code, limit))

                rs = curs.fetchall()
                return rs
        except Exception as e:
            print('I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise

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

    def updateStochastic(self, code, yyyymm, fast_k, slow_k, slow_d):
        print('updateStochastic', code, yyyymm, fast_k, slow_k, slow_d)
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from market_prices where code=%s and yyyymmdd=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                sql = 'update market_prices set ' \
                      'fast_k=%s, ' \
                      'slow_k=%s, ' \
                      'slow_d=%s ' \
                      'where id=%s'
                curs.execute(sql, (
                    fast_k, slow_k, slow_d, rs['id']
                ))
                self.conn.commit()


        finally:
            pass