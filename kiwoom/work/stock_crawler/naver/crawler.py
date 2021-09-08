import time
from stock_crawler.database.connMysql import Mysql
from util import Util
import numpy as np

class Naver():
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()
        self.util = Util()

    def updatePrice(self, code=None):
        """
        당일 종가 업데이트
        :return:
        """
        if code:
            row = self.mysql.corporation(code)
            price = self.util.get_price(row['code'])
            self.mysql.updateCorpStockPrice(row['id'], price.replace(',', ''))
        else:
            rows = self.mysql.corporations()
            for row in rows:
                time.sleep(0.1)
                price = self.util.get_price(row['code'])
                self.mysql.updateCorpStockPrice(row['id'], price.replace(',', ''))

    def updateMarketPrice(self, code=None):
        if code:
            # row = self.mysql.corporation(code)
            self.util.get_market_prices(code, 1)
            # self.mysql.updateCorpStockPrice(row['id'], price.replace(',', ''))
        else:
            rows = self.mysql.corporations()
            for row in rows:
                time.sleep(0.1)
                self.util.get_market_prices(row['code'], 1)



    #
    # def get_exprice(self):
    #     rows = self.mysql.corporations()
    #     for row in rows:
    #         time.sleep(0.1)
    #         code = row['code']
    #         url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
    #
    #         # code = row['종목코드'].zfill(6)
    #
    #         url = url_tmpl % (code)
    #         # tables = pd.read_html(url, encoding='euc-kr')
    #         # df = tables[3]
    #         try:
    #             tables = pd.read_html(url, encoding='euc-kr', match='주요재무정보')
    #             df = tables[0]
    #
    #             temp_df = df.set_index(df.columns[0])
    #             temp_df = temp_df[temp_df.columns[:11]]
    #             for idx, column in temp_df.iteritems():
    #                 self.mysql.financeinfoNaver(code, idx, column)
    #         except ValueError:
    #             print("Oops!  That was no valid number.  Try again...")
    #         except:
    #             print('err', code)
    #
    # def get_exprice_test(self, code):
    #
    #     url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
    #
    #     # code = row['종목코드'].zfill(6)
    #
    #     url = url_tmpl % (code)
    #
    #     try:
    #         tables = pd.read_html(url, encoding='euc-kr', match='주요재무정보')
    #         df = tables[0]
    #
    #         temp_df = df.set_index(df.columns[0])
    #         temp_df = temp_df[temp_df.columns[:11]]
    #         # temp_df.fillna('--')
    #         # temp_df.replace(np.NaN, 0)
    #         for idx, column in temp_df.iteritems():
    #             column.fillna('--')
    #             column.replace(np.NaN, 0)
    #             self.mysql.financeinfoNaver(code, idx, column)
    #     except ValueError:
    #         print("Oops!  That was no valid number.  Try again...")
    #     except:
    #         print('err', code)

    # def isNaN(self, string):
    #     return string != string
naver = Naver()
# 매 시장 close시
# naver.updatePrice()  # 단순가격만 업데이트(@deprecated)
naver.updateMarketPrice()  # 시가종가등 모든 가격을 업데이트
# naver.updateMarketPrice('005930')
# naver.get_exprice_test('204210')
# naver.get_exprice_test('017180')

# naver.get_exprice()
