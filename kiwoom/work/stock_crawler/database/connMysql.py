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
from .querie.shorting import Shorting
# import numpy as np
# from stock_crawler.utils import *

# DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        # host = os.getenv('DB_HOST')
        # user = os.getenv('DB_USER')
        # password = os.getenv('DB_PASSWORD')
        # db = os.getenv('DB_DATABASE')
        #
        # self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        self.conn = self.connect()
        self.conn_corporatons = Corporatons(self)
        self.conn_market_prices = MarketPrices(self)
        self.conn_fnguide = Fnguide(self)
        self.conn_naver = Naver(self)
        self.conn_concensus = Concensus(self)
        self.conn_earings = Earnings(self)
        self.conn_tr_volume = VolumeSector(self)
        self.conn_shorting = Shorting(self)

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

    def updateCorporations(self, market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region):
        """
        신규 기업정보 입력 및 업데이트
        :return: row
        """
        return self.conn_corporatons.updateCorporations(market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region)

    def updateCorpStockPrice(self, id, price):
        """
        당일 종가 업데이트
        :param id:
        :param price:
        :return: None
        """
        return self.conn_corporatons.updateCorpStockPrice(id, price)

    def updateSrim(self, id, price):
        return self.conn_corporatons.updateSrim(id, price)

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
        return self.conn_fnguide.get3yearRoe(code, yyyymm)

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

    def updateKrxCode(self, code, code_krx):
        return self.conn_corporatons.updateKrxCode(code, code_krx)

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

    def updateShortingStatus(self, code, ymd, volume, v_remain, tr_amount, remain_amount):
        self.conn_shorting.updateShortingStatus(code, ymd, volume, v_remain, tr_amount, remain_amount)

    def updateShortingVolume(self, code, dt, volume, v_buy, ratio):
        self.conn_shorting.updateShortingVolume(code, dt, volume, v_buy, ratio)

    def isNaN(self, string):
        return string != string

    def close(self):
        self.conn.close()

    def connect(self):
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')
        port = int(os.getenv('DB_PORT'))
        # print(host, port, user, password, db)
        return pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
