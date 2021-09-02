import pymysql

# DB 테이블 칼럼대로 만든 객체
class Corporatons:
    def __init__(self, parent=None):
        self.conn = parent.conn

    def corporations(self):
        """
        기업리스트 가져오기
        :return:
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, code, investing_comp_name, common_stocks from corporations where status = 0"
                curs.execute(sql)

                rs = curs.fetchall()
                return rs
        except Exception as e:
            print('I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise
        # finally:
        #     return rs

    def corporation(self, code):
        """
        기업정보 가져오기
        :return:
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select common_stocks from corporations where code=%s"
                curs.execute(sql, (code))

                rs = curs.fetchone()
                return rs
        except Exception as e:
            print('I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise
        # finally:
        #     pass

    def updateCorpStockPrice(self, id, price):
        """
        당일 종가 업데이트
        :param id:
        :param price:
        :return: Null
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'stock_price=%s ' \
                      'where id=%s'
                curs.execute(sql, (price, id))
                self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateCorpTotalShares(self, code, shares):
        """
        총주식수 업데이트 (보통주)
        :param code:
        :param shares:
        :return: Null
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'common_stocks=%s ' \
                      'where code=%s'
                curs.execute(sql, (
                    shares, code))
                self.conn.commit()
        except Exception as e:
            print('[updateCorpTotalShares] I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise
        finally:
            print('updateCorpTotalShares updated')
            pass

    def updateInvestingCompname(self, id, eng):

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'UPDATE  corporations ' \
                      'SET     investing_comp_name = %s ' \
                      'WHERE   id = %s'

                curs.execute(sql, (eng, id))
                self.conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    # def updateCorpRecom(self, code, df):
    #
    #     """
    #     Deprecated
    #     투자의견 및 목표주가
    #     :param code:
    #     :param df:
    #     :return:
    #     """
    #     df = keyCheck(df, ['투자의견', '목표주가', '추정기관수', 'EPS', 'PER'])
    #     recom_cd = df['투자의견'][0]
    #     avg_prc = df['목표주가'][0]
    #     recom_cnt = df['추정기관수'][0]
    #     # eps = df['EPS'][0] # 추정치이므로 의미없음
    #     # per = df['PER'][0]
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = 'update corporations set ' \
    #                   'recom_cd=%s, ' \
    #                   'avg_prc=%s, ' \
    #                   'recom_cnt=%s ' \
    #                   'where code=%s'
    #             curs.execute(sql, (
    #                 recom_cd, avg_prc, recom_cnt, code))
    #             self.conn.commit()
    #     except Exception as e:
    #         print('[updateCorpRecom] I got a Exception  - reason "%s"' % str(e))
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         print('updateCorpRecom updated')
    #         pass

    # def updateCorpSrim(self, id, s_rim):
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'update corporations set ' \
    #                   's_rim=%s ' \
    #                   'where id=%s'
    #             curs.execute(sql, (s_rim, id))
    #             self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    # def updateSrim(self, id, price):
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'update corporations set ' \
    #                   's_rim=%s ' \
    #                   'where id=%s'
    #             curs.execute(sql, (price, id))
    #             self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass