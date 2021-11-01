# -*- coding: utf-8 -*-
import time
# from stock_crawler.database.connMysql import Mysql
from stock_crawler.naver.crawler import Naver
from stock_crawler.technical_analysis.cal import Calculate
from stock_crawler.fnguide.crawler import Fnguide
from stock_crawler.investing.crawler import Investing
from stock_crawler.pykrx.crawler import Krx
from stock_crawler.fdr import Fdr

class Crawler():
    def __init__(self, parent=None):
        super().__init__()
        # self.mysql = Mysql()
        self.naver = Naver()
        self.fnguide = Fnguide()
        self.investing = Investing()
        self.krx = Krx()
        self.cal = Calculate()
        self.fdr = Fdr()  # FinanceDataReader 를 사용 (가격업데이트 별도 버젼)


        # self.daily()
        # time.sleep(1)
        self.weekly()
        # time.sleep(1)
        self.monthly()
        # time.sleep(1)
        self.yearly()


    def daily(self):
        print('daily')
        # self.naver.updateMarketPrice() # 현재가격 업데이트
        # # self.naver.updateMarketPrice('054040')
        # time.sleep(1)
        # self.fnguide.crawalSvdMain() # 발행주식수, 시가총액 | 증권사예측(EPS, PER) | ROA, EPS....
        # # self.fnguide.crawalSvdMain('023960')
        # time.sleep(1)
        # self.fnguide.crawlingConsensus() # 컨센서스 업데이트
        # # # self.fnguide.crawlingConsensus('005930')
        # time.sleep(1)
        # self.cal.calStochastic(15, 5, 3) # 스토케시틱 업데이트
        # # # # self.cal.calStochastic(15, 5, 3, '054040')
        # time.sleep(1)
        # self.cal.calMomentum()
        # # # # self.cal.calMomentum('207940')
        # time.sleep(1)
        # self.cal.movingAverage(60)  # 60일 이동평균선
        # time.sleep(1)
        # self.krx.get_market_trading_volume_by_date()  # 색터별 거래량
        # # self.krx.get_market_trading_volume_by_date('20210908', '20210909')  # 색터별 거래량
        self.krx.기간별_개별종목_공매도_종합정보()

    def weekly(self):
        print('weekly')
        self.investing.earnings()

    def monthly(self):
        print('monthly')
        self.krx.updateCorp() # 신규상장사 업데이트
        time.sleep(1)
        self.investing.updateInvestingCompName() # 상장사의 investing에서 사용하는 이름 가져오기
        time.sleep(1)
        self.fnguide.crawalFinancialRatio() # 유동비율, 부채비율, 영업이익율 roa, roic 등을 구함
        time.sleep(1)

        pass

    def yearly(self):
        print('yearly')
        self.fnguide.crawalFinance() # '매출액', '매출총이익', '영업이익', '당기순이익', '자산', '부채', '자본', '영업활동으로인한현금흐름'
        time.sleep(1)
        # self.cal.calSrim("202012")

    def temporary(self):
        pass
if __name__ == "__main__":
    crawler = Crawler()


