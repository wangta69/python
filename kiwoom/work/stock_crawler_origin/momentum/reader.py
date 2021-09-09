# https://jsp-dev.tistory.com/82
# https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/
# https://github.com/FinanceData/FinanceDataReader (선행지수에 대해서도 읽을 거리가 많음)

import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.stats import linregress
import numpy as np
from time import time
import FinanceDataReader as fdr
from stock_crawler.database.connMysql import Mysql
import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def square(x):
    return x * x

class Mymomentum:
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()
        # self.df_krx = fdr.StockListing('KRX') # 회사정보를 가져온다 Symbol, Market, HomePage, Region
        # self.codes = self.df_krx['Symbol'] # 회사코드 (060310...)만 별도로 codes에 입력한다.
        # print(self.codes) #

    def getPrice(self, code, from_dt, to_dt):
        df_price = fdr.DataReader(code, from_dt, to_dt) # Date, Open, High, Low, Close, Volume, Change
        # df_price = df_price[['Close']] # Close 값만 가져온다
        # df_price.columns = [code] # code를 Close 값들의 column으로 정의한다.
        return df_price

    def startGetPrice(self, from_dt, to_dt, code=None):

        start = time()
        if code:
            df = self.getPrice(code, from_dt, to_dt)
            print(df)
            for ymd, row in df.iterrows():
                print('===================')
                print(ymd, int(row['High']), int(row['Low']), int(row['Close']), int(row['Volume']), row['Change'])
                open = int(row['Open'])
                high = int(row['High'])
                low = int(row['Low'])
                close = int(row['Close'])
                trade_qty = int(row['Volume'])

                self.mysql.updateMarketPrices(code, ymd, close, open, high, low, trade_qty)

        else:
            corporations = self.mysql.corporations()
            for row in corporations:
                code = row['code']
                df = self.getPrice(code, from_dt, to_dt)

                for ymd, row in df.iterrows():
                    print(ymd, int(row['High']), int(row['Low']), int(row['Close']), int(row['Volume']), row['Change'])
                    open = int(row['Open'])
                    high = int(row['High'])
                    low = int(row['Low'])
                    close = int(row['Close'])
                    trade_qty = int(row['Volume'])

                    self.mysql.updateMarketPrices(code, ymd, close, open, high, low, trade_qty)


        # pool = ProcessPoolExecutor(max_workers=32)
        # self.codes = ['005930', '066570']
        # pool = ProcessPoolExecutor()
        # pool = multiprocessing.Pool()

        # result = self.getPrice('005930')
        # print(result)
        # pool.map(self.getPrice, self.codes)
        # results = list(pool.map(self.getPrice, self.codes))
        # stocks = pd.concat(results, axis=1)
        #
        # end = time()
        # print(end - start)
        # stocks.to_excel('datas.xlsx')

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
            # print('===========')
            # print('idxmax()', momentums.idxmax(), 'idxmin()', momentums.idxmin())
            # # print('===========')
            # # end = momentums.index.get_loc(momentums.idxmax())  # 모멘텀이 가장 높은 시점
            # end = momentums.iloc[momentums.idxmax()].index.values.astype(int)[0]  # 모멘텀이 가장 높은 시점
            # print('===========')
            # print(end, end-5)
            # print(df.iloc[end - 5: end])
            # rets = np.log(df['Close'].iloc[end - 5: end])
            # print('===========')
            # print('rets', rets)
            # print('df ===========')
            # print(df)
            # print('df.index[end] ===========')
            # print(df.index[end])
            # closes.index[end]
            # print('end', end)
            # rets = np.log(momentums.iloc[end - 5: end])
            # print(end - 90)
            pass

        #     for best in bests:
        #         end = momentums[best].index.get_loc(momentums[best].idxmax()) # 모멘텀이 가장 높은 시점
        #         if end - 90 < 0 : # 모멘텀이 최고인 시점의 90일 이전이 최초설정한 2017-01-01 보다 이전이면 그냥 생략해 버림
        #             continue
        #
        #         rets = np.log(stocks[best].iloc[end - 90 : end])
        #         momentum_point = stocks[best].index[end].strftime("%Y/%m/%d") # 모멘텀이 최고인 시점을 label에 표헌하기 위함
        #
        #         x = np.arange(len(rets))
        #         slope, intercept, r_value, p_value, std_err = linregress(x, rets) # 회귀함수
        #
        #         try:
        #             plt.plot(np.arange(180), stocks[best][end-90:end+90], label=[best,momentum_point]) # 모멘텀이 최고인 시점의 90일 전후 종가
        #             plt.plot(x, np.e ** (intercept + slope*x)) # 회귀함수의 결과를 그림림

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

    # fig = plt.figure(figsize=(10,10))
    # ax = fig.add_subplot(1,1,1)
    # stocks = pd.read_excel('datas.xlsx', index_col=0) #저장된 종가 데이타를 읽어옮
    #
    # codes = stocks.columns
    # start = time()
    # def momentum(closes):
    #     returns = np.log(closes)
    #     x = np.arange(len(returns))
    #     slope, _, rvalue, _, _ = linregress(x, returns)
    #     return ((1 + slope) ** 252) * (rvalue ** 2) # annualize slope and multiply by R^2
    #
    # momentums = stocks.copy(deep=True)
    #
    # for code in codes:
    #     momentums[code] = stocks[code].rolling(90).apply(momentum) #각 종목마다 모멘텀 구하는 함수적용
    #     # rolling 합을 구한다..90 이란 90일 동안의 합을 구하는 것이다.
    #     bests = momentums.max().sort_values(ascending=False).index[:5] # 모멘텀 값이 가장 큰 상위 5개 종목을 bests에 넣음
    #
    #     for best in bests:
    #         end = momentums[best].index.get_loc(momentums[best].idxmax()) # 모멘텀이 가장 높은 시점
    #         if end - 90 < 0 : # 모멘텀이 최고인 시점의 90일 이전이 최초설정한 2017-01-01 보다 이전이면 그냥 생략해 버림
    #             continue
    #
    #         rets = np.log(stocks[best].iloc[end - 90 : end])
    #         momentum_point = stocks[best].index[end].strftime("%Y/%m/%d") # 모멘텀이 최고인 시점을 label에 표헌하기 위함
    #
    #         x = np.arange(len(rets))
    #         slope, intercept, r_value, p_value, std_err = linregress(x, rets) # 회귀함수
    #
    #         try:
    #             plt.plot(np.arange(180), stocks[best][end-90:end+90], label=[best,momentum_point]) # 모멘텀이 최고인 시점의 90일 전후 종가
    #             plt.plot(x, np.e ** (intercept + slope*x)) # 회귀함수의 결과를 그림림
    #         except
    #             continue


m = Mymomentum()
# m.startGetPrice('2021-02-01', '2021-08-02') # 일자별 가격을 가지고 옮
# m.startGetPrice('2021-02-01', '2021-09-06', '053080')
# m.calMomentum('005930')
# m.calMomentum('010060')
# m.calMomentum('207940')
# m.calMomentum() # 90일동안의 가격을 이용하여 추세를 구함(기울기)
# m.movingAverage(60, '207940')
m.movingAverage(60) # 60일 이동평균선

# # ax.legend(loc=5)
# # plt.show()
# # end = time()
# # print(end - start)

# if __name__ == '__main__':
#     # Pool 객체 초기화
#     pool = multiprocessing.Pool()
#     # pool = multiporcessing.Pool(processes=4)
#
#     # Pool.map
#     inputs = [0, 1, 2, 3, 4]
#     outputs = pool.map(square, inputs)
#
#     print(outputs)
#
#     # Pool.map_async
#     outputs_async = pool.map_async(square, inputs)
#     outputs = outputs_async.get()
#
#     print(outputs)
#
#     # Pool.apply_async
#     results_async = [pool.apply_async(square, [i]) for i in range(100)]
#     results = [r.get() for r in results_async]
#
#     print(results)