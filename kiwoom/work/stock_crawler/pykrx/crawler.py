import time
from pykrx import stock
from stock_crawler.database.connMysql import Mysql



class Krx():
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()


    def get_market_trading_volume_by_date(self, from_dt, to_dt, code=None):
        """
        당일 종가 업데이트
        :return:
        """
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


krx = Krx()
# 매 시장 close시
# naver.updatePrice()  # 단순가격만 업데이트(@deprecated)
# krx.get_market_trading_volume_by_date('20210901', '20210907', '005930')  # 시가종가등 모든 가격을 업데이트
# krx.get_market_trading_volume_by_date('20210901', '20210907', '002420')
krx.get_market_trading_volume_by_date('20210901', '20210907')

