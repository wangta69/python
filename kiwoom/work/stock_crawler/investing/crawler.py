import xlrd
import operator
import pandas as pd
import numpy as np
import requests
import bs4
import time
import html
from bs4 import BeautifulSoup
from connMysql import Mysql
from utils.extra import random_user_agent
import investpy
import re
from datetime import datetime
from stock_crawler.database.connMysql import Mysql

class Investing():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def getInvestingCompName(self, code):
        """
        기존 테이블에 investing 용 사이트 명을 넣어 둔다.
        :param code:
        :return:
        """
        try:
            result = investpy.stocks.get_stock_company_profile(code, 'south korea', 'en')
            # result = investpy.stocks.get_stock_company_profile(code, 'KOSDAQ', 'en')

            segment = result['url'].split('/')
            comp_name = segment[4].replace('-company-profile', "")

            return comp_name
        except:
            return None
            raise
        finally:
            pass

    def updateInvestingCompName(self):
        rows = self.mysql.corporations()
        for row in rows:

            if row['investing_comp_name'] == None:
                time.sleep(0.1)
                # print('code', row['code'])
                # en_name = self.getInvestingCompName(row['code'])
                # print('en_name', en_name)
                # if en_name:
                #     self.mysql.updateInvestingCompname(row['id'], en_name)
                try:
                    search_results = investpy.search_quotes(text=row['code'], products=['stocks'],
                                                            countries=['south korea'], n_results=5)
                    for search_result in search_results:
                        en_name = search_result.tag.replace('/equities/', "")
                    if en_name:
                        print(en_name)
                        self.mysql.updateInvestingCompname(row['id'], en_name)
                except:
                     pass



    def earnings(self):
        """
        earnings 를 가져와서 처리한다.
        :return:
        """
        rows = self.mysql.corporations()
        for row in rows:
            time.sleep(0.1)
            if row['investing_comp_name']:
                headers = {
                    "User-Agent": random_user_agent(),
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "text/html",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                }
                params = {

                }

                try:
                    url = 'https://kr.investing.com/equities/' + row['investing_comp_name'] + '-earnings'
                    page = requests.get(url, headers=headers, data=params)
                    df = pd.read_html(page.text)
                    df[0].columns = df[0].columns.str.replace('[/,\s]', '', regex=True)
                    for idx, r in df[0].iterrows():
                        try:
                            # row['예측'] = row['예측'].replace('/', '')
                            r['주당순이익'] = re.sub('[/,\s,\,]', '', str(r['주당순이익']))
                            r['예측'] = re.sub('[/,\s,\,]', '', r['예측'])
                            r['매출'] = self.strtonumber(r['매출'])
                            r['예측.1'] = self.strtonumber(r['예측.1'])
                            # r['매출'] = re.sub('[B,M,\,]', '', r['매출'])
                            # r['예측.1'] = re.sub('[/,\s, B,M,\,]', '', r['예측.1'])

                            r['발표일'] = re.sub('[년,월]', '-', r['발표일'])
                            r['발표일'] = re.sub('[일,\s]', '', r['발표일'])
                            r['기말'] = datetime.strptime(r['기말'], "%m/%Y")
                            self.mysql.earnings(row['code'], r)
                        except KeyError as e:
                            print('I got a KeyError - reason "%s"' % str(e))
                        except Exception as e:
                            print('I got a Exception  - reason "%s"' % str(e))
                            raise
                    print(df[0])

                except:
                    pass
        pass

    # def updateInvestingCompName(self):
    #     with open(r'ks.html', "r", encoding='utf8') as f:
    #         page = f.read()
    #
    #         df = pd.read_html(page)[0]
    #
    #         # 링크만 별도로 출력하기 위해 BeautifulSoup 사용
    #         soup = BeautifulSoup(page, 'html.parser')
    #         table = soup.find('table')
    #         links = []
    #         for tr in table.findAll("tr"):
    #             trs = tr.findAll("td")
    #             for each in trs:
    #                 try:
    #                     link = each.find('a')['href']
    #                     links.append(link)
    #                 except:
    #                     pass
    #
    #         df['link'] = links
    #         print(df)
    #
    #         for index, data_row in df.iterrows():
    #             print('==')
    #             print(data_row['종목'])
    #             link = data_row['link'].split('/')
    #             print(link[2])
    #             self.mysql.updateInvestingCompname(data_row['종목'], link[2])

    def test(self):
        # df = pd.read_html('https://www.investing.com/equities/hankuk-carbon-earnings')[0]
        # print(df);
        #
        # df = investpy.get_stock_historical_data(stock='AAPL',
        #                                         country='United States',
        #                                         from_date='01/01/2010',
        #                                         to_date='01/01/2020')
        # print(df.head())
        #
        # print('search_result')
        # search_result = investpy.search_quotes(text='apple', products=['stocks'],
        #                                        countries=['united states'], n_results=1)
        # print(search_result)
        #
        # search_result = investpy.search_quotes(text='hankuk-carbon', products=['stocks'],
        #                                        countries=['south korea'], n_results=1)
        # print(search_result)
        # recent_data = search_result.retrieve_recent_data()
        # historical_data = search_result.retrieve_historical_data(from_date='01/01/2019', to_date='01/01/2020')
        # information = search_result.retrieve_information()
        # default_currency = search_result.retrieve_currency()
        # technical_indicators = search_result.retrieve_technical_indicators(interval='daily')
        # print('recent_data', recent_data)
        # print('historical_data', historical_data)
        # print('information', information)
        # print('default_currency', default_currency)
        # print('technical_indicators', technical_indicators)
        #
        #
        #
        # result = investpy.stocks.get_stock_information('010690', 'south korea', as_json=False)
        # # result = investpy.stocks.get_stock_information('017960', 'south korea', as_json=True)
        # print(result)
        # for index, data_row in result.iterrows():
        #     print(data_row)

        headers = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        params = {

        }
        url = 'https://kr.investing.com/equities/hyundai-develop-earnings'
        page = requests.get(url, headers=headers, data=params)
        df = pd.read_html(page.text)
        # print(df[0])
        df[0].columns = df[0].columns.str.replace('[/,\s]', '', regex=True)

        for idx, r in df[0].iterrows():
            
            # row['예측'] = row['예측'].replace('/', '')

            r['주당순이익'] = re.sub('[/,\s,\,]', '', str(r['주당순이익']))
            r['예측'] = re.sub('[/,\s,\,]', '', r['예측'])

            r['매출'] = self.strtonumber(r['매출'])
            r['예측.1'] = self.strtonumber(r['예측.1'])

            r['발표일'] = re.sub('[년,월]', '-', r['발표일'])
            r['발표일'] = re.sub('[일,\s]', '', r['발표일'])
            r['기말'] = datetime.strptime(r['기말'], "%m/%Y")

            print(r);


        pass

    def searchTopbar(self):
        search_results = investpy.search_quotes(text='apple', products=['stocks', 'bonds'],
                                                countries=['united states'], n_results=5)

        search_results = investpy.search_quotes(text='124560', products=['stocks'],
                                                countries=['south korea'], n_results=5)
        print('search_results', search_results)

        for search_result in search_results:
            print(search_result)
        # headers = {
        #     "User-Agent": random_user_agent(),
        #     "X-Requested-With": "XMLHttpRequest",
        #     "Accept": "text/html",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Connection": "keep-alive",
        # }
        # params = {
        #     'search_text': '270660'
        # }
        # url = 'https://www.investing.com/search/service/searchTopBar'
        # page = requests.post(url, headers=headers, data=params)
        # print(page)
        pass

    def strtonumber(self, s):
        # s = re.sub('[/,\s, B,M,\,]', '',str)
        if s == '--':
            return '--'
        else :
            s = re.sub('[/,\s, \,]', '', s)
            last_char = s[-1]
            s = re.sub('[B,M]', '', s)
            s = float(s)
            if last_char == "M":
                s = s * 1000000
            elif last_char == "B":
                s = s * 1000000000
            return str(s)



investing = Investing()
# 월 1회
# investing.updateInvestingCompName()
# 주 1회
investing.earnings()
# investing.test()



