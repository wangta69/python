import time
from datetime import date
import pandas as pd
from pykrx import stock
from stock_crawler.database.connMysql import Mysql

class Krx():
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()


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

if __name__ == "__main__":
    krx = Krx()
    # 매 시장 close시
    # naver.updatePrice()  # 단순가격만 업데이트(@deprecated)
    # krx.get_market_trading_volume_by_date('20210901', '20210907', '005930')  # 시가종가등 모든 가격을 업데이트
    # krx.get_market_trading_volume_by_date('20210901', '20210907', '002420')
    krx.get_market_trading_volume_by_date('20210901', '20210907')
    # krx.updateCorp()

