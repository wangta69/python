import time
from datetime import date, timedelta
import pandas as pd
from pykrx import stock
from stock_crawler.database.connMysql import Mysql
from stock_crawler.pykrx.krx import KRXCrawler

class Krx():
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()
        self.krxcrawer = KRXCrawler()


    def get_market_trading_volume_by_date(self, from_dt=None, to_dt=None, code=None):
        """
        당일 종가 업데이트
        :return:
        """
        today = date.today()
        if from_dt == None:
            from_dt = today.strftime("%Y%m%d")

        if to_dt == None:
            to_dt = today.strftime("%Y%m%d")

        if code:
            try:
                df = stock.get_market_trading_volume_by_date(from_dt, to_dt, code)
                print(df)
                print('=======================================')
                for ymd, row in df.iterrows():
                    print('======================')
                    print('ymd', ymd)
                    print(row)
                    self.mysql.updateVolumeSector(code, ymd, row)
            except ValueError as e:
                print('I got a ValueError - reason "%s"' % str(e))
            finally:
                pass

            # self.mysql.updateCorpStockPrice(row['id'], price.replace(',', ''))
        else:
            rows = self.mysql.corporations()
            for row in rows:
                code = row['code']
                print('code', code)
                try:
                    df = stock.get_market_trading_volume_by_date(from_dt, to_dt, code)
                    print(df)
                    print('=======================================')
                    for ymd, row in df.iterrows():
                        self.mysql.updateVolumeSector(code, ymd, row)
                except ValueError as e:
                    print('I got a ValueError - reason "%s"' % str(e))
                finally:
                    pass
            # rows = self.mysql.corporations()
            # for row in rows:
            #     time.sleep(0.1)
            #     price = self.util.get_price(row['code'])
            #     self.mysql.updateCorpStockPrice(row['id'], price.replace(',', ''))

    def updateCorp(self):
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'  # 1

        kosdaq = pd.read_html(url + "?method=download&marketType=kosdaqMkt")[0]  # 2
        kospi = pd.read_html(url + "?method=download&marketType=stockMkt")[0]  # 3
        kosdaq.종목코드 = kosdaq.종목코드.astype(str).apply(lambda x: x.zfill(6))
        kospi.종목코드 = kospi.종목코드.astype(str).apply(lambda x: x.zfill(6))
        kosdaq['market'] = 'KQ'
        kospi['market'] = 'KS'

        stocks = kospi.append(kosdaq)  # kospi 뒤로 kosdaq dataframe을 합친다.
        stocks.sort_values(by="상장일", ascending=False)
        stocks = stocks.rename(
            columns={
                '회사명': 'comp_name',
                '종목코드': 'code',
                '업종': 'industry',
                '주요제품': 'products',
                '상장일': 'listed_at',
                '결산월': 'sett_month',
                '대표자명': 'ceo',
                '홈페이지': 'url',
                '지역': 'region'
            })

        stocks = stocks.where((pd.notnull(stocks)), None)

        for row in stocks.itertuples():
            # market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region
            print(row[10], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            self.mysql.updateCorporations(row[10], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

            # (야후금융에서는 코스피를 "KS", 코스닥을 "KQ"로 관리한다.)
    """
    공매도 API
    KRX는 (T+2)일 이후의 데이터를 제공합니다. 최근 영업일이 20190405라면 20190403일을 포함한 이전 데이터를 얻을 수 있습니다.
    """
    def get_shorting_status_by_date(self, from_dt=None, to_dt=None, code=None):

        today = date.today()
        if from_dt == None:
            from_dt = today.strftime("%Y%m%d") - timedelta(5)

        if to_dt == None:
            to_dt = today.strftime("%Y%m%d") - timedelta(2)

        if code:
            try:
                print(from_dt, to_dt, code)
                df = stock.get_shorting_status_by_date(from_dt, to_dt, code)
                print(df)
                for ymd, row in df.iterrows():
                    print('======================')
                    print('ymd', ymd)
                    print('거래량', row['거래량'])
                    print('잔고수량', row['잔고수량'])
                    print('거래대금', row['거래대금'])
                    print('잔고금액', row['잔고금액'])

                    volume = row['거래량']
                    v_remain = row['잔고수량']
                    tr_amount = row['거래대금']
                    remain_amount = row['잔고금액']

                    self.mysql.updateShortingStatus(code, ymd, volume, v_remain, tr_amount, remain_amount)
                    pass
            except ValueError as e:
                print('I got a ValueError - reason "%s"' % str(e))
            finally:
                pass

        else:
            rows = self.mysql.corporations()
            for row in rows:
                code = row['code']
                print('code', code)
                try:
                    df = stock.get_shorting_status_by_date(from_dt, to_dt, code)
                    for ymd, row in df.iterrows():
                        print('======================')
                        print('ymd', ymd)
                        print('거래량', row['거래량'])
                        print('잔고수량', row['잔고수량'])
                        print('거래대금', row['거래대금'])
                        print('잔고금액', row['잔고금액'])

                        volume = row['거래량']
                        v_remain = row['잔고수량']
                        tr_amount = row['거래대금']
                        remain_amount = row['잔고금액']

                        self.mysql.updateShortingStatus(code, ymd, volume, v_remain, tr_amount, remain_amount)
                except ValueError as e:
                    print('I got a ValueError - reason "%s"' % str(e))
                finally:
                    pass



        """
        종목별 공매도 현황
        공매도, 잔고, 공매도금액, 잔고금액을 확인
        :return: 
        """
        pass
    def get_shorting_volume_by_ticker(self, dt=None):
        """
        종목별 공매도 거래 정보(공매도 거래량 정보를 반환합니다.)
        공매도, 잔고, 공매도금액, 잔고금액을 확인
        하루전까지 조회가능
        :return:
        """
        # today = date.today()

        if dt == None:
            yesterday = date.today() - timedelta(1)
            dt = yesterday.strftime("%Y%m%d")
        print(dt)
        try:
            df = stock.get_shorting_volume_by_ticker(dt)
            for code, row in df.iterrows():
                # print('code', code)
                # print('공매도', row['공매도'])
                # print('매수', row['매수'])
                # print('비중', row['비중'])
                volume = row['공매도']
                v_buy = row['매수']
                ratio = row['비중']

                self.mysql.updateShortingVolume(code, dt, volume, v_buy, ratio)
        except ValueError as e:
            print('I got a ValueError - reason "%s"' % str(e))
        finally:
            pass
        # print(df.head(3))
        # print(df)
        # for code, row in df.iterrows():
        #     if code == '005930':
        #         print('code', code)
        #         print('row', row)
        #         # self.mysql.updateVolumeSector(ymd, row)

    def updateCorpCode(self):
        self.krxcrawer.readeCorp()
        pass

    def get_shorting(self, from_dt=None, to_dt=None, code=None):
        if code:
            row = self.mysql.corporation(code)
            print(row['code_krx'])
            if row['code_krx']:
                self.krxcrawer.getShorting(row['code_krx'], from_dt, to_dt)
                pass
        else:
            pass

        pass


if __name__ == "__main__":
    krx = Krx()
    # query를 위한 krx용 업체코드
    # krx.updateCorpCode()
    krx.get_shorting("20211001", "20211001", "005930")

    # 매 시장 close시
    # naver.updatePrice()  # 단순가격만 업데이트(@deprecated)
    # krx.get_market_trading_volume_by_date('20210901', '20210907', '005930')  # 시가종가등 모든 가격을 업데이트
    # krx.get_market_trading_volume_by_date('20210901', '20210907', '002420')
    # krx.get_market_trading_volume_by_date('20210901', '20210907')
    # krx.updateCorp()
    # krx.get_shorting_status_by_date("20211008", "20211013", "005930")
    # krx.get_shorting_status_by_date("20211012", "20211012", "004840")
    # krx.get_shorting_volume_by_ticker(20211013)

    # yesterday = date.today() - timedelta(1)
    # for i in range(10, 100):
    #    dt = date.today() - timedelta(i)
    #    krx.get_shorting_volume_by_ticker(dt.strftime("%Y%m%d"))

