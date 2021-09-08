import os

import pymysql
from dotenv import load_dotenv
from .querie.corporations import Corporatons
from .querie.market_prices import MarketPrices
from .querie.financeinfos_fnguide import Fnguide
from .querie.financeinfos_naver import Naver
from .querie.concensus_estimate import Concensus
from .querie.earings import Earnings
from .querie.trading_volume_sector import VolumeSector
# import numpy as np
# from stock_crawler.utils import *

# DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        self.conn_corporatons = Corporatons(self)
        self.conn_market_prices = MarketPrices(self)
        self.conn_fnguide = Fnguide(self)
        self.conn_naver = Naver(self)
        self.conn_concensus = Concensus(self)
        self.conn_earings = Earnings(self)
        self.conn_tr_volume = VolumeSector(self)

    def corporations(self):
        """
        기업리스트 가져오기
        :return: rows
        """
        return self.conn_corporatons.corporations()

    def corporation(self, code):
        """
        기업정보 가져오기
        :return: row
        """
        return self.conn_corporatons.corporation(code)

    def updateCorpStockPrice(self, id, price):
        """
        당일 종가 업데이트
        :param id:
        :param price:
        :return: None
        """
        return self.conn_corporatons.updateCorpStockPrice(id, price)

    # fnguide 의 데이타를 이용해서 처리
    def updateCorpTotalShares(self, code, shares):
        """
        총주식수 업데이트 (보통주)
        :param code:
        :param shares:
        :return: None
        """
        return self.conn_corporatons.updateCorpTotalShares(code, shares)

    def updateMomentum(self, code, momentum):
        """
        총주식수 업데이트 (보통주)
        :param code:
        :return: None
        """
        return self.conn_corporatons.updateMomentum(code, momentum)

    def updateMovingAverage(self, code, average):
        """
        총주식수 업데이트 (보통주)
        :param code:
        :return: None
        """
        return self.conn_corporatons.updateMovingAverage(code, average)




    def updateFinancialStatements(self, code, yyyymm, dataSet):
        return self.conn_fnguide.updateFinancialStatements(code, yyyymm, dataSet)



    def deleteConsensusEstimate(self, code):
        self.conn_concensus.deleteConsensusEstimate(code)

    def updateConsensusEstimate(self, code, row):
        self.conn_concensus.updateConsensusEstimate(code, row)

    def financeinfoFnguideFinancial(self, code, idx, column):
        return  self.conn_fnguide.financeinfoFnguideFinancial(code, idx, column)

    def updateFinancialRatio(self, code, yyyymm, dataSet):
        return  self.conn_fnguide.updateFinancialRatio(code, yyyymm, dataSet)

    # srim 관련 데이타 가져오기
    def getControllingShareholder(self, code, yyyymm):
        """
        지배주주지분 가져오기
        :return:
        """
        return  self.conn_fnguide.getControllingShareholder(code, yyyymm)

    def get3yearRoe(self, code, yyyymm):
        """
        3년간 roe가져오기
        :return:
        """
        return  self.conn_fnguide.get3yearRoe(code, yyyymm)

    # def updateSrim(self, id, price):
    #     return self.conn_corporatons.updateSrim(id, price)


    def financeinfoNaver(self, code, idx, column):
        """
        네이버 금융정보 업데이트
        :param code:
        :param idx:
        :param column:
        :return: Null
        """
        self.conn_naver.financeinfoNaver(code, idx, column)


    # Investing 관련
    def earnings(self, code, data):
        self.conn_earings.earnings(code, data)

    def updateInvestingCompname(self, id, eng):
        return self.conn_corporatons.updateInvestingCompname(id, eng)

    def updateMarketPrices(self, code, yyyymm, close, open, high, low, trade_qty):
        return self.conn_market_prices.updateMarketPrices(code, yyyymm, close, open, high, low, trade_qty)

    def prices(self, code, limit):
        return self.conn_market_prices.prices(code, limit)

    def updateStochastic(self, code, yyyymm, fast_k, slow_k, slow_d):
        self.conn_market_prices.updateStochastic(code, yyyymm, fast_k, slow_k, slow_d)


    def updateVolumeSector(self, code, yyyymm, row):
        corp = row['기관합계']
        corp_etc = row['기타법인']
        private = row['개인']
        foreigner = row['외국인합계']
        print('yyyymm', yyyymm.strftime("%Y-%m-%d"))
        self.conn_tr_volume.updateVolumeSector(code, yyyymm.strftime("%Y-%m-%d"), corp, corp_etc, private, foreigner)

    def isNaN(self, string):
        return string != string

    def close(self):
        self.conn.close()

    # def updateCorpRecom(self, code, df):
    #
    #     """
    #     Deprecated
    #     투자의견 및 목표주가
    #     :param code:
    #     :param df:
    #     :return:
    #     """
    #     return self.conn_corporatons.updateCorpRecom(code, df)

    # def updateCorpSrim(self, id, s_rim):
    #     return self.conn_corporatons.updateCorpSrim(id, s_rim)

    # def updateInvestmentIndiators(self, code, yyyymm, dataSet):
    #
    #     yyyymm = yyyymm.replace('/', '')
    #
    #     per = dataSet['PER'] if ~np.isnan(dataSet['PER']) else None
    #     pcr = dataSet['PCR'] if ~np.isnan(dataSet['PCR']) else None
    #     psr = dataSet['PSR'] if ~np.isnan(dataSet['PSR']) else None
    #     pbr = dataSet['PBR'] if ~np.isnan(dataSet['PBR']) else None
    #     total_cashflow = dataSet['총현금흐름'] if ~np.isnan(dataSet['총현금흐름']) else None
    #
    #     # print('update start', code, yyyymm, per, pcr, psr, pbr, total_cashflow)
    #
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select code from financeinfos where code=%s and yyyymm=%s limit 0, 1"
    #             curs.execute(sql, (code, yyyymm))
    #             # rs = curs.fetchall()
    #             rs = curs.fetchone()
    #
    #             if rs == None:  # 값이 없을 경우 현재 값 입력
    #                 print('None')
    #                 sql = 'insert into financeinfos ' \
    #                       '(code, yyyymm, per, pcr, psr, pbr, total_cashflow) ' \
    #                       'values(%s, %s, %s, %s, %s, %s, %s)'
    #                 curs.execute(sql, (code, yyyymm, per, pcr, psr, pbr, total_cashflow))
    #
    #                 self.conn.commit()
    #             else:
    #                 print('UPDATE')
    #                 sql = 'update financeinfos set ' \
    #                       'per=%s, ' \
    #                       'pcr=%s, ' \
    #                       'psr=%s, ' \
    #                       'pbr=%s, ' \
    #                       'total_cashflow=%s ' \
    #                       'where code=%s and yyyymm=%s'
    #                 curs.execute(sql, (per, pcr, psr, pbr, total_cashflow, code, yyyymm))
    #                 self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #         # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
    #     finally:
    #         pass

    # def updateOrder(self, yyyymm, setField, orderItem):
    #
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'update financeinfos target ' \
    #                   'join ' \
    #                   '(' \
    #                   'select id, (@rownumber := @rownumber + 1) as rownum ' \
    #                   'from financeinfos ' \
    #                   'cross join (select @rownumber := 0) r ' \
    #                   ' where yyyymm = %s and {} is not null ' \
    #                   'order by {} asc ' \
    #                   ') source on target.id = source.id ' \
    #                   'set {} = rownum'
    #
    #             curs.execute(sql.format(orderItem, orderItem, setField), (yyyymm))
    #             self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    # def updateScore(self, yyyymm):
    #     """
    #     설정 조건 충족시 1점, 미충족시 0점
    #     당기순이익이 0이상인가?
    #     영업현금흐름이 0이상인가?
    #     ROA가 전년 대비 증가했는가?
    #     영업현금흐름이 순이익보다 높은가?
    #     부채비율이 전년 대비 감소했는가?
    #     유동비율이 전년 대비 증가했는가?
    #     당해 신규주식 발행을 하지 않았는가?
    #     매출총이익이 전년 대비 증가했는가?
    #     자산회전율이 전년 대비 증가했는가?
    #     """
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'UPDATE  financeinfos ' \
    #                   'SET     score_net_income = IF(net_income > 0, 1, 0), ' \
    #                   '        score_cashflow_operating = IF(cashflow_operating  > 0, 1, 0), ' \
    #                   '        score_diff = IF(cashflow_operating >  net_income, 1, 0), ' \
    #                   '        score_total = score_net_income +  score_cashflow_operating + score_diff ' \
    #                   'WHERE   yyyymm = %s'
    #
    #             curs.execute(sql, (yyyymm))
    #             self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass