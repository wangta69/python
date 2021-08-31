# https://wikidocs.net/94805
import pystocklib.srim as srim
import pystocklib.srim.reader as srim_reader

from lib.reader import *
from lib.srim import *

from connMysql import Mysql
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
        k = get_5years_earning_rate()
        print('k', k)
        price0 = estimate_price('005930', k)
        print(price0)
        pass

srimc = SrimClass()
# srimc.updatePrice()
srimc.test()

# s-rim
# 1. BBB- 등급의  5년채 수익률을 가져온다.