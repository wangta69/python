# https://jsp-dev.tistory.com/82
# https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/
# https://github.com/FinanceData/FinanceDataReader (선행지수에 대해서도 읽을 거리가 많음)


from time import time
import FinanceDataReader as fdr
from stock_crawler.database.connMysql import Mysql

def square(x):
    return x * x

class Fdr:
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


if __name__ == '__main__':
    fdr = Fdr()
    fdr.startGetPrice('2021-02-01', '2021-09-06', '053080')
