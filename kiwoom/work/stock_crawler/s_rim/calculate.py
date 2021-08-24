# https://wikidocs.net/94805
import pystocklib.srim as srim
import pystocklib.srim.reader as srim_reader

from lib.reader import *
from lib.srim import *


from stock_crawler.connMysql import Mysql
class SrimClass():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def updatePrice(self):
        rows = self.mysql.corporations()
        for row in rows:
            try:
                k = srim_reader.get_5years_earning_rate()
                price0 = srim.estimate_price(row['code'], k) # BBB- 등급의 5년차 수익률 (8.17)
                price1 = srim.estimate_price(row['code'], k, w=0.9)
                price2 = srim.estimate_price(row['code'], k, w=0.8)

                self.mysql.updateSRim(row['id'], price0[0])
                print(row['code'])
                print("초과이익 지속      : ", price0[0])
                print("초과이익 감소 (10%): ", price1[0])
                print("초과이익 감소 (20%): ", price2[0])
            except:
                pass

    def test(self):
        code = '005930'
        k = get_5years_earning_rate()
        price0 = estimate_price(code, k)
        price1 = estimate_price(code, k, w=0.9)
        price2 = estimate_price(code, k, w=0.8)
        #
        # self.mysql.updateSRim(row['id'], price0[0])
        # print(row['code'])
        print("초과이익 지속      : ", price0)
        print("초과이익 감소 (10%): ", price1)
        print("초과이익 감소 (20%): ", price2)

        print(price0)
        pass
if __name__ == "__main__":
    srimc = SrimClass()
    # srimc.updatePrice()
    srimc.test()

    # s-rim
    # 1. BBB- 등급의  5년채 수익률을 가져온다.

    # 2. net_worth (지배주주지분) 가져온다.

    # 3. 3년간 roe를 가져와서 roe를 구한다.
    # if roe3[0] <= roe3[1] <= roe3[2] or roe3[0] >= roe3[1] >= roe3[2]:
    #     roe = roe3[2]
    # else:
    #     roe = (roe3[0] + roe3[1] * 2 + roe3[2] * 3) / 6     # weighting average
    # return roe

    # 4. 초과이익을 구한다.
    # excess_earning = net_worth * (roe - k) * 0.01

    # 5. valueㄹ르 구한다.
    # if w == 1:
    #     value = net_worth + (net_worth * (roe - k)) / k
    # else:
    #     excess_earning = net_worth * (roe - k) * 0.01
    #     mul = w / (1.0 + k * 0.01 - w)
    #     value = net_worth + excess_earning * mul

    # 6. 주식수를 가져온다.

    # 7. 적정가격을 계산한다.
    # try:
    #     price = value / shares
    # except:
    #     price = 0
    # return price, shares, value, net_worth, roe, excess_earning