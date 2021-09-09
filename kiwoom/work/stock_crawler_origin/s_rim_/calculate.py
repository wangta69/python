# https://wikidocs.net/94805
import pystocklib.srim as srim
import pystocklib.srim.reader as srim_reader
import math
from lib.reader import *
from lib.srim import *
from stock_crawler.database.connMysql import Mysql

class SrimClass():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def cal3YearRoe(self, roe):
        try:
            l = len(roe)
            if l == 3:
                if roe[0] <= roe[1] <= roe[2] or roe[0] >= roe[1] >= roe[2]:
                    roe = roe[2]
                else:
                    roe = (roe[0] + roe[1] * 2 + roe[2] * 3) / 6  # weighting average
                return roe
            elif l > 0:
                return roe[l - 1]
            else:
                return 0
        except Exception as e:
            print(e)
            print('cal3YearRoe===')
            print(roe[0], roe[1], roe[2])

    def srim_price(self, net_worth, roe, shares, k, w=1):
        """
        
        :param net_worth: 지배주주지분
        :param roe: 3년간 roe를 가져와서 roe를 구한다.
        :param shares: 보통주식수
        :param k: 수익율 (BBB- 등급의 5년차 수익률)
        :param w: 초과이익
        :return: 
        """
        if w == 1:
            value = net_worth + (net_worth * (roe - k)) / k
        else:
            excess_earning = net_worth * (roe - k) * 0.01
            mul = w / (1.0 + k * 0.01 - w)
            value = net_worth + excess_earning * mul

        # 적정가격을 계산한다.
        try:
            price = value / shares
        except:
            price = 0

        return price
        pass

    def updatePrice(self):
        rows = self.mysql.corporations()
        # 1. BBB- 등급의  5년채 수익률을 가져온다.
        k = srim_reader.get_5years_earning_rate()
        yyyymm = '202012'
        for row in rows:
            # try:
                code = row['code']
                corp_id = row['id']
                # 보통주식수 (shares)
                shares = row['common_stocks']

                # 지배주주지분 (net_worth)
                row = self.mysql.getControllingShareholder(code, yyyymm)

                if row is None:
                    net_worth = 0
                elif row['controlling_shareholder'] is not None:
                    net_worth = row['controlling_shareholder'] * 100000000  # 현재 db 저장단위(1억)
                else:
                    net_worth = 0

                # 3년간 roe를 가져와서 roe를 구한다.
                rows = self.mysql.get3yearRoe(code, yyyymm)
                roes = []

                for row in rows:
                    # if ~math.isnan(row['roe']):
                    if row['roe'] is not None:
                        roes.append(row['roe'])
                roe = self.cal3YearRoe(roes)

                price = self.srim_price(net_worth, roe, shares, k) # BBB- 등급의 5년차 수익률 (8.17)
                price09 = self.srim_price(net_worth, roe, shares, k, w=0.9)
                price08 = self.srim_price(net_worth, roe, shares, k, w=0.8)

                self.mysql.updateSrim(corp_id, price)
                # print("초과이익 지속      : ", price)
                # print("초과이익 감소 (10%): ", price09)
                # print("초과이익 감소 (20%): ", price08)
            # except Exception as e:
            #     print('updatePrice ===========')
            #     print(e)
            #     pass

    # def updatePrice(self):
    #     rows = self.mysql.corporations()
    #     for row in rows:
    #         try:
    #             k = srim_reader.get_5years_earning_rate()
    #             price0 = srim.estimate_price(row['code'], k) # BBB- 등급의 5년차 수익률 (8.17)
    #             price1 = srim.estimate_price(row['code'], k, w=0.9)
    #             price2 = srim.estimate_price(row['code'], k, w=0.8)
    #
    #             self.mysql.updateSRim(row['id'], price0[0])
    #             print(row['code'])
    #             print("초과이익 지속      : ", price0[0])
    #             print("초과이익 감소 (10%): ", price1[0])
    #             print("초과이익 감소 (20%): ", price2[0])
    #         except:
    #             pass

    # def test(self):
    #     code = '005930'
    #     k = get_5years_earning_rate()
    #     price0 = estimate_price(code, k)
    #     price1 = estimate_price(code, k, w=0.9)
    #     price2 = estimate_price(code, k, w=0.8)
    #     #
    #     # self.mysql.updateSRim(row['id'], price0[0])
    #     # print(row['code'])
    #     print("초과이익 지속      : ", price0)
    #     print("초과이익 감소 (10%): ", price1)
    #     print("초과이익 감소 (20%): ", price2)
    #
    #     print(price0)
    #     pass

    def test(self):
        """
        데이타 베이스의 기초데이타를 기준으로 계산하기
        :return: 
        """
        # 1. BBB- 등급의  5년채 수익률을 가져온다.
        k = get_5years_earning_rate()
        print('k', k)

        code = '005930'
        yyyymm = '202012'

        # 보통주식수 가져오기
        row = self.mysql.corporation(code)
        shares = row['common_stocks'];
        print('shares', shares)

        # 2. net_worth (지배주주지분) 가져온다.
        row = self.mysql.getControllingShareholder(code, yyyymm)
        net_worth = row['controlling_shareholder'] * 100000000  # 현재 db 저장단위(1억)
        print('net_worth', net_worth)

        # 3. 3년간 roe를 가져와서 roe를 구한다.
        rows = self.mysql.get3yearRoe(code, yyyymm)
        roes = []
        for row in rows:
            roes.append(row['roe'])
            # try:
            # except:


        roe = cal3YearRoe(roes)
        print('roe', roe)

        # 4. 초과이익을 구한다.
        excess_earning = net_worth * (roe - k) * 0.01
        print('excess_earning', excess_earning)

        # 5. value를 구한다.
        w = 1
        if w == 1:
            value = net_worth + (net_worth * (roe - k)) / k
        else:
            excess_earning = net_worth * (roe - k) * 0.01
            mul = w / (1.0 + k * 0.01 - w)
            value = net_worth + excess_earning * mul
        print('value', value)

        # 7. 적정가격을 계산한다.
        try:
            price = value / shares
        except:
            price = 0

        print('price', price)
        # return price, shares, value, net_worth, roe, excess_earning

        # price0 = estimate_price(code, k)
        # price1 = estimate_price(code, k, w=0.9)
        # price2 = estimate_price(code, k, w=0.8)
        #
        # self.mysql.updateSRim(row['id'], price0[0])
        # print(row['code'])
        # print("초과이익 지속      : ", price0)
        # print("초과이익 감소 (10%): ", price1)
        # print("초과이익 감소 (20%): ", price2)
        #
        # print(price0)
        pass

    # def isNaN(self, string):
    #     return string != string

if __name__ == "__main__":
    srimc = SrimClass()
    srimc.updatePrice()
    # srimc.test()

    # s-rim
    # 1. BBB- 등급의  5년채 수익률을 가져온다.

    # 기준은 지금은 2021년 이라고 가정할때 2020.12 월을 기준으로 이전 데이타를 가공한다.
    # 2. net_worth (지배주주지분) 가져온다.

    # 3. 3년간 roe를 가져와서 roe를 구한다.
    # if roe3[0] <= roe3[1] <= roe3[2] or roe3[0] >= roe3[1] >= roe3[2]:
    #     roe = roe3[2]
    # else:
    #     roe = (roe3[0] + roe3[1] * 2 + roe3[2] * 3) / 6     # weighting average
    # return roe

    # 4. 초과이익을 구한다.
    # excess_earning = net_worth * (roe - k) * 0.01

    # 5. value를 구한다.
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