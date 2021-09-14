# https://wikidocs.net/94805
import pystocklib.srim as srim
# import pystocklib.srim.reader as srim_reader
import math
from stock_crawler.technical_analysis.technical.s_rim_util import *
# from lib.srim import *
from stock_crawler.database.connMysql import Mysql


class Srim():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def cal3YearRoe(self, roe):
        roe.reverse() # 현재 최근값이 0번째인것을 과거값이 0번째로 변경
        try:
            l = len(roe)
            if l == 3:
                # if roe[0] <= roe[1] <= roe[2] or roe[0] >= roe[1] >= roe[2]:
                if roe[0] <= roe[1] <= roe[2]:
                    roe = roe[2]
                elif roe[0] >= roe[1] >= roe[2]: # roe가 계속 줄어드는 기업은 위험하므로 0으로 처리한다.
                    return 0
                else:
                    roe = (roe[0] + roe[1] * 2 + roe[2] * 3) / 6  # weighting average
                return roe
            elif l > 0: # 2개나 1하일경우는 최근값을 리턴
                return roe[l - 1]
            else: # 이럴경우는 최근 분기 roe를 가져와서 처리하는 것은 어떨까?
                return 0
        except Exception as e:
            print('[cal3YearRoe] I got a Exception - reason "%s"' % str(e))
            print(roe[0], roe[1], roe[2])

    def srim_price(self, net_worth, roe, shares, k, w=1):
        """
        :param net_worth: 지배주주지분(자기자본(순자산))
        :param roe: 3년간 roe를 가져와서 roe를 구한다.
        :param shares: 보통주식수
        :param k: 할인율 (BBB- 등급의 5년차 수익률)
        :param w: 지속계수
        :return:
        """
        # 기업가치 = 자기자본 + 초과이익 / 할인율
        # 적정주가 = 기업가치 / 발행주식수
        # 초과이익 = 자기자본 * (ROE - 할인율)
        # value : 기업가치, price: 적정주가
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

    def updateSrim(self, yyyymm, code=None):
        # 1. BBB- 등급의  5년채 수익률을 가져온다.
        k = get_5years_earning_rate()

        if code:
            row = self.mysql.corporation(code)
            corp_id = row['id']
            shares = row['common_stocks']

            # 지배주주지분
            row = self.mysql.getControllingShareholder(code, yyyymm)

            if row is None:
                net_worth = 0
            elif row['controlling_shareholder'] is not None:
                net_worth = row['controlling_shareholder'] * 100000000  # 현재 db 저장단위(1억)
            else:
                net_worth = 0

            print('net_worth', net_worth)

            # 3년간 roe를 가져와서 roe를 구한다.
            rows = self.mysql.get3yearRoe(code, yyyymm)
            roes = []

            for row in rows:
                # if ~math.isnan(row['roe']):
                if row['roe'] is not None:
                    roes.append(row['roe'])
            roe = self.cal3YearRoe(roes)

            price = self.srim_price(net_worth, roe, shares, k)  # BBB- 등급의 5년차 수익률 (8.17)
            # price09 = self.srim_price(net_worth, roe, shares, k, w=0.9)  # 감소비율 10% => 0.9  (적정가격)
            # price08 = self.srim_price(net_worth, roe, shares, k, w=0.8)  # 감소비율 20% => 0.8   (안전마진)
            # price07 = self.srim_price(net_worth, roe, shares, k, w=0.7)  # 감소비율 30% => 0.7

            self.mysql.updateSrim(corp_id, price)

        else:
            rows = self.mysql.corporations()
            for row in rows:
                # try:
                code = row['code']
                corp_id = row['id']
                # 보통주식수 (shares)
                shares = row['common_stocks']

                # 지배주주지분
                row = self.mysql.getControllingShareholder(code, yyyymm)

                if row is None:
                    net_worth = 0
                elif row['controlling_shareholder'] is not None:
                    net_worth = row['controlling_shareholder'] * 100000000  # 현재 db 저장단위(1억)
                else:
                    net_worth = 0

                print('net_worth', net_worth)

                # 3년간 roe를 가져와서 roe를 구한다.
                rows = self.mysql.get3yearRoe(code, yyyymm)
                roes = []

                for row in rows:
                    # if ~math.isnan(row['roe']):
                    if row['roe'] is not None:
                        roes.append(row['roe'])
                roe = self.cal3YearRoe(roes)

                price = self.srim_price(net_worth, roe, shares, k)  # BBB- 등급의 5년차 수익률 (8.17)
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


if __name__ == "__main__":
    srimc = Srim()
    # srimc.updateSrim('202012', '005930')
    srimc.updateSrim('202012')
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