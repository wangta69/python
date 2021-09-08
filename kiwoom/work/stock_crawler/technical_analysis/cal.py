import time
from pykrx import stock
import pandas as pd
import numpy as np
from stock_crawler.database.connMysql import Mysql
from stock_crawler.technical_analysis.technical.stochastic import *

class Calculate():
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()


    def calStochastic(self, n, m, t, code=None):
        # fast_k, slow_k, slow_d를 획득
        day = max(n, m, t) * 2
        # day = 100
        # print('day', day + 10)
        if code:
            prices = self.mysql.prices(code, day)
            data = []
            # 역순으로 넣어 둔다.
            for price in prices:
                data.insert(0, [price['yyyymmdd'], price['close'], price['high'], price['low']])

            df = pd.DataFrame(data)
            df.columns = ['Date', 'Close', 'High', 'Low']
            df['fast_k'] = get_stochastic_fast_k(df['Close'], df['Low'], df['High'], n)
            df['slow_k'] = get_stochastic_slow_k(df['fast_k'], m)
            df['slow_d'] = get_stochastic_slow_d(df['slow_k'], t)

            for index, row in df.iterrows():
                # print('Date', row['Date'])
                # print('fast_k', row['fast_k'])
                # print('slow_k', row['slow_k'])
                # print('slow_d', row['slow_d'])
                date = row['Date']
                fast_k = row['fast_k']
                slow_k = row['slow_k']
                slow_d = row['slow_d']
                if ~np.isnan(fast_k) and ~np.isnan(slow_k) and ~np.isnan(slow_d):
                    # print('Date', row['Date'])
                    # print('fast_k', row['fast_k'])
                    # print('slow_k', row['slow_k'])
                    # print('slow_d', row['slow_d'])
                    self.mysql.updateStochastic(code, date, fast_k, slow_k, slow_d)
            # slow_k 가 20 이하 과매도구간, 80이상 과매수구간
            # 과매도구간에서 slow_d > slow_k 매수
            # 과매수구간에서 slow_d < slow_k 매수
            # 85이상 과매수(매도)
            # 70이상 일반적 상승
            # 30이하 일반적 하락
            # 15이하 과매도(매수)

            # print(df)
        else:
            rows = self.mysql.corporations()
            for row in rows:
                code = row['code']
                prices = self.mysql.prices(code, day)
                data = []
                # 역순으로 넣어 둔다.
                for price in prices:
                    data.insert(0, [price['yyyymmdd'], price['close'], price['high'], price['low']])

                df = pd.DataFrame(data)
                df.columns = ['Date', 'Close', 'High', 'Low']
                df['fast_k'] = get_stochastic_fast_k(df['Close'], df['Low'], df['High'], n)
                df['slow_k'] = get_stochastic_slow_k(df['fast_k'], m)
                df['slow_d'] = get_stochastic_slow_d(df['slow_k'], t)

                for index, row in df.iterrows():
                    date = row['Date']
                    fast_k = row['fast_k']
                    slow_k = row['slow_k']
                    slow_d = row['slow_d']
                    if ~np.isnan(fast_k) and ~np.isnan(slow_k) and ~np.isnan(slow_d):
                        self.mysql.updateStochastic(code, date, fast_k, slow_k, slow_d)


cal = Calculate()
# 대부분 증권사에서는 n(5)-m(3)-t(3)를 사용하고 네이버금융은 n(15)-m(5)-t(3)을
# cal.calStochastic(15, 5, 3, '054040') # 나는 14, 5, 3
cal.calStochastic(15, 5, 3)