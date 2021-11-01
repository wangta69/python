import pymysql
import time
from stock_crawler.utils import *

# DB 테이블 칼럼대로 만든 객체
class Corporatons:
    def __init__(self, parent):
        self.parent = parent

    def corporations(self):
        """
        기업리스트 가져오기
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, code, code_krx, investing_comp_name, common_stocks from corporations where status = 0"
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
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, code, code_krx, common_stocks, investing_comp_name from corporations where code=%s"
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
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'stock_price=%s ' \
                      'where id=%s'
                curs.execute(sql, (price, id))
                conn.commit()
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
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'common_stocks=%s ' \
                      'where code=%s'
                curs.execute(sql, (
                    shares, code))
                conn.commit()
        except Exception as e:
            print('[updateCorpTotalShares] I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise
        finally:
            print('updateCorpTotalShares updated')
            pass

    def updateInvestingCompname(self, id, eng):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'UPDATE  corporations ' \
                      'SET     investing_comp_name = %s ' \
                      'WHERE   id = %s'

                curs.execute(sql, (eng, id))
                conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateKrxCode(self, code, code_krx):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'UPDATE  corporations ' \
                      'SET     code_krx = %s ' \
                      'WHERE   code = %s'

                curs.execute(sql, (code_krx, code))
                conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateMomentum(self, code, momentum):
        if isNaN(momentum):
            momentum = 0
        print('updateMomentum', code, momentum)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'UPDATE  corporations ' \
                      'SET     momentum = %s ' \
                      'WHERE   code = %s'

                curs.execute(sql, (momentum, code))
                conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateMovingAverage(self, code, average):
        if isNaN(average):
            average = 0
        print('updateMovingAverrage', code, average)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'UPDATE  corporations ' \
                      'SET     moving_average_60 = %s ' \
                      'WHERE   code = %s'

                curs.execute(sql, (average, code))
                conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateCorporations(self, market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
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

                    conn.commit()
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
                    conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateSrim(self, id, price):
        print('updateSrim', id, price)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:

                sql = 'update corporations set ' \
                      's_rim=%s ' \
                      'where id=%s'
                curs.execute(sql, (price, id))
                conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass