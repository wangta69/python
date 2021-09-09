# https://jsp-dev.tistory.com/82
# https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/
# https://github.com/FinanceData/FinanceDataReader (선행지수에 대해서도 읽을 거리가 많음)

import time
from pykrx import stock
import pandas as pd
import numpy as np
from scipy.stats import linregress
from stock_crawler.database.connMysql import Mysql
from stock_crawler.technical_analysis.technical.stochastic import *
from stock_crawler.technical_analysis.technical.s_rim import Srim

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
                date = row['Date']
                fast_k = row['fast_k']
                slow_k = row['slow_k']
                slow_d = row['slow_d']
                if ~np.isnan(fast_k) and ~np.isnan(slow_k) and ~np.isnan(slow_d):
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

    def momentum(self, closes):
        returns = np.log(closes)

        x = np.arange(len(returns))

        slope, _, rvalue, _, _ = linregress(x, returns) # 선형회귀분석
        return ((1 + slope) ** 252) * (rvalue ** 2) # annualize slope and multiply by R^2

    def calMomentum(self, code=None):
        if code:
            prices = self.mysql.prices(code, 120)
            closes = []
            for price in prices:
                closes.insert(0, [price['yyyymmdd'], price['close']])

            df = pd.DataFrame(closes)
            df.columns = ['Date', 'Close']

            momentums = df.rolling(90).apply(self.momentum)  # 각 종목마다 모멘텀 구하는 함수적용
            self.mysql.updateMomentum(code, momentums['Close'].iloc[-1])
        else:
            corporations = self.mysql.corporations()
            for row in corporations:
                code = row['code']
                prices = self.mysql.prices(code, 120)
                closes = []
                for price in prices:
                    closes.insert(0, [price['yyyymmdd'], price['close']])

                df = pd.DataFrame(closes)
                df.columns = ['Date', 'Close']

                momentums = df.rolling(90).apply(self.momentum)  # 각 종목마다 모멘텀 구하는 함수적용
                self.mysql.updateMomentum(code, momentums['Close'].iloc[-1])

    def movingAverage(self, day, code=None):
        if code:
            prices = self.mysql.prices(code, day)
            closes = []
            # 역순으로 넣어 둔다.
            for price in prices:
                closes.insert(0, [price['yyyymmdd'], price['close']])

            df = pd.DataFrame(closes)
            df.columns = ['Date', 'Close']

            latest = df['Close'].iloc[-1]

            mean = df.rolling(day).mean()  # 각 종목마다 모멘텀 구하는 함수적용
            avg = mean['Close'].iloc[-1]
            gap60 = (latest - avg) / latest * 100
            self.mysql.updateMovingAverage(code, gap60)
        else:
            corporations = self.mysql.corporations()
            for row in corporations:
                code = row['code']
                prices = self.mysql.prices(code, day)
                closes = []
                for price in prices:
                    closes.insert(0, [price['yyyymmdd'], price['close']])

                df = pd.DataFrame(closes)
                df.columns = ['Date', 'Close']

                latest = df['Close'].iloc[-1]

                mean = df.rolling(day).mean()  # 각 종목마다 모멘텀 구하는 함수적용
                avg = mean['Close'].iloc[-1]
                gap60 = (latest - avg) / latest * 100
                self.mysql.updateMovingAverage(code, gap60)

    def calSrim(self, yyyymm):
        srim = Srim()
        srim.updateSrim(yyyymm)



if __name__ == "__main__":
    print(__name__)
    cal = Calculate()
    # 대부분 증권사에서는 n(5)-m(3)-t(3)를 사용하고 네이버금융은 n(15)-m(5)-t(3)을
    # cal.calStochastic(15, 5, 3, '054040') # 나는 14, 5, 3
    # cal.calStochastic(15, 5, 3)

    # cal.calMomentum('207940') # 모멘텀(60일의 가격을 이용하여 예상 기울기)
    # cal.movingAverage(60)  # 60일 이동평균선
    cal.calSrim("202012")

