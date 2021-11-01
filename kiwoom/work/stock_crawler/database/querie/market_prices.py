import pymysql

# DB 테이블 칼럼대로 만든 객체
class MarketPrices:
    def __init__(self, parent):
        self.parent = parent

    def prices(self, code, limit):
        """
        업체별 가격 리스트를 가져온다.
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select ymd, open, high, low, close from market_prices where code = %s order by ymd desc limit 0, %s"
                curs.execute(sql, (code, limit))

                rs = curs.fetchall()
                return rs
        except Exception as e:
            print('I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise

    def price(self, code, ymd):
        """
        업체별 가격 리스트를 가져온다.
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select close, trade_qty from market_prices where code = %s and ymd = %s"
                curs.execute(sql, (code, ymd))

                rs = curs.fetchone()
                return rs
        except Exception as e:
            print('I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise

    def updateMarketPrices(self, code, ymd, close, open, high, low, trade_qty):

        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from market_prices where code=%s and ymd=%s limit 0, 1"
                curs.execute(sql, (code, ymd))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into market_prices ' \
                          '(code, ymd, close, open, high, low, trade_qty) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                        code, ymd, close, open, high, low, trade_qty
                    ))

                    conn.commit()
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
                    conn.commit()

                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass

    def updateStochastic(self, code, ymd, fast_k, slow_k, slow_d):
        print('updateStochastic', code, ymd, fast_k, slow_k, slow_d)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from market_prices where code=%s and ymd=%s limit 0, 1"
                curs.execute(sql, (code, ymd))
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
                conn.commit()
        finally:
            pass