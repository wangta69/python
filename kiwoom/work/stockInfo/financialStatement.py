from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QThread
import math
import time
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import threading

# from PyQt5.QtCore import QEventLoop
# from pykrx import stock
# import datetime
#
# import matplotlib.pyplot as plt
# # 참조 : https://yobro.tistory.com/202
#
# dt_now = datetime.datetime.now()
# COM_DATE = dt_now.strftime('%Y%m%d') # 기준일자 600 거래일 전일 부터 현제까지 받아옴

class FinancialStatements(QThread):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

    def printFinance(self, code, name):
        # print('=== code')
        # print(code)
        # print('=== name')
        # print(name)
        url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
        if len(code) == 6:
            url = url_tmpl % (code)
            tables = pd.read_html(url, encoding='euc-kr')
            df = tables[3]
            try:
                gain = df.iloc[1, 10]
                privious = df.iloc[1, 9]
                # if gain != 'nan':
                # print(type(gain))
                # if type(gain) is float:
                if isinstance(gain, float):
                    is_NAN = math.isnan(gain)
                    if not is_NAN:
                        print(name, code)
                        print(privious, gain)
            except IndexError:
                gain = 'nan'

    def run(self):
        print('expecting')

        df1 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

        df1 = df1[['회사명', '종목코드']]
        df1['종목코드'] = df1['종목코드'].astype(str)
        df1['종목코드'] = df1['종목코드'].apply(lambda x: '00' + str(x) if len(str(x)) == 4 else x)
        df1['종목코드'] = df1['종목코드'].apply(lambda x: '0' + str(x) if len(str(x)) == 5 else x)
        ##print(df1)


        # url = url_tmpl % ('005930')
        url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
        for i, row in df1.iterrows():
            # self.printFinance(row)
            # print(row)
            # code = row['종목코드']
            # name = row['회사명']
            # t = threading.Thread(target=self.printFinance, name="[th def {}]".format(i), args=(code, name))
            # t.start()
            # print(row['회사명'], row['종목코드'], len(row['종목코드']))

            if len(row['종목코드']) == 6:
                url = url_tmpl % (row['종목코드'])
                tables = pd.read_html(url, encoding='euc-kr')
                df = tables[3]
                try:
                    gain = df.iloc[1, 10]
                    privious = df.iloc[1, 9]
                    # if gain != 'nan':
                    if isinstance(gain, float):
                        is_NAN = math.isnan(gain)
                        if not is_NAN:
                            print(row['회사명'], row['종목코드'])
                            print(privious, gain)
                except IndexError:
                    gain = 'nan'
            time.sleep(1)
            # # # print(tables)
            # #
            # # print('=====================')
            # df = tables[3]
            # # # returning index
            # #
            # # print(df)
            # # print('=====================')
            # # print(df.index)
            # # print('=====================')
            # # print(df.iloc[1:2])
            # # print('=====================')
            # print(df.iloc[1, 10])
            # print('=====================')
            # # print(df['IFRS연결'])

    def info(self):
        print('info')
        url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
        url = url_tmpl % ('005930')
        tables = pd.read_html(url, encoding='euc-kr')
        try:
            df = tables[3]
            print(df)
        except IndexError:
            df = 'null'
        # url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
        # url = url_tmpl % ('005930')
        #
        # item_info = requests.get(url).text
        # soup = BeautifulSoup(item_info, 'html.parser')
        # finance_info = soup.select('div.section.cop_analysis div.sub_section')[0]
        #
        # th_data = [item.get_text().strip() for item in finance_info.select('thead th')]
        # annual_date = th_data[3:7]
        # quarter_date = th_data[7:13]
        #
        # finance_index = [item.get_text().strip() for item in finance_info.select('th.h_th2')][3:]
        # finance_data = [item.get_test().strip() for item in finance_info.select('td')]
        # finance_data = np.array(finance_data)
        # finance_data.resize(len(finance_index), 10)
        #
        # finance_data = annual_data + quarter_date
        #
        # finance = pd.DataFrame(data-finance_data[0:, 0:], index=finance_index, columns=finance_data)


