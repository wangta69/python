import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from stock_crawler.connMysql import Mysql
import numpy as np
import math

class Naver():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def updatePrice(self):
        """
        당일 종가 업데이트
        :return:
        """
        rows = self.mysql.corporations()
        for row in rows:
            time.sleep(0.1)
            price = self.get_price(row['code'])
            self.mysql.updateCorpStockPrice(row['id'], price.replace(',', ''))

    def get_bs_obj(self, com_code):
        url = "https://finance.naver.com/item/main.nhn?code=" + com_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser") #html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
        return bs_obj

    def get_price(self, com_code):
        print('com_code', com_code)
        try:
            bs_obj = self.get_bs_obj(com_code)
            no_today = bs_obj.find("p", {"class":"no_today"})
            blind_now = no_today.find("span", {"class" : "blind"})
            return blind_now.text
        except:
            return '0'

    def get_exprice(self):
        rows = self.mysql.corporations()
        for row in rows:
            time.sleep(0.1)
            code = row['code']
            url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'

            # code = row['종목코드'].zfill(6)

            url = url_tmpl % (code)
            # tables = pd.read_html(url, encoding='euc-kr')
            # df = tables[3]
            try:
                tables = pd.read_html(url, encoding='euc-kr', match='주요재무정보')
                df = tables[0]

                temp_df = df.set_index(df.columns[0])
                temp_df = temp_df[temp_df.columns[:11]]
                for idx, column in temp_df.iteritems():
                    self.mysql.financeinfoNaver(code, idx, column)
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
            except:
                print('err', code)

    def get_exprice_test(self, code):

        url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'

        # code = row['종목코드'].zfill(6)

        url = url_tmpl % (code)

        try:
            tables = pd.read_html(url, encoding='euc-kr', match='주요재무정보')
            df = tables[0]

            temp_df = df.set_index(df.columns[0])
            temp_df = temp_df[temp_df.columns[:11]]
            # temp_df.fillna('--')
            # temp_df.replace(np.NaN, 0)
            for idx, column in temp_df.iteritems():
                column.fillna('--')
                column.replace(np.NaN, 0)
                self.mysql.financeinfoNaver(code, idx, column)
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
        except:
            print('err', code)
    def isNaN(self, string):
        return string != string
naver = Naver()
naver.updatePrice()
# naver.get_exprice_test('204210')
# naver.get_exprice_test('017180')

# naver.get_exprice()
