# import pystocklib.srim.reader as reader
from .reader import *


def estimate_company_value(code, k, w=1):
    """
    estimate company value
    :param code: stock code
    :param k: expected earning rate
    :param w:
    :return: (Value, NetWorth, ROE, Excess Earning)
    """
    net_worth = get_net_worth(code)  # 지배주주지분
    roe = get_roe(code)  # roe
    excess_earning = net_worth * (roe - k) * 0.01

    if w == 1:
        value = net_worth + (net_worth * (roe - k)) / k
    else:
        excess_earning = net_worth * (roe - k) * 0.01
        mul = w / (1.0 + k * 0.01 - w)
        value = net_worth + excess_earning * mul

    return value, net_worth, roe, excess_earning


def estimate_price(code, k, w=1):
    """
    calculate reasonable price
    :param code:
    :param k:
    :param w:
    :return: Reasonable Price, Shares, Value, NetWorth, ROE, Excess Earning
    """
    value, net_worth, roe, excess_earning = estimate_company_value(code, k, w)

    print('estimate_price', value, net_worth, roe, excess_earning)
    shares = get_shares(code)
    try:
        price = value / shares
    except:
        price = 0
    return price, shares, value, net_worth, roe, excess_earning


def get_disparity(code, k, w=1):
    """
    get disparity that is calculated by (cur_price / est_price ) * 100
    :param code:
    :param k:
    :param w:
    :return:
    """
    est_price, shares, value, net_worth, roe, excess_earning = estimate_price(code, k, w)
    cur_price = get_current_price(code)

    try:
        disparity = (cur_price / est_price) * 100
    except:
        disparity = None
    return disparity, cur_price, est_price, shares, value, net_worth, roe, excess_earning

def cal3YearRoe(roe):
    l = len(roe)
    print(roe)
    print('length', l)
    if l == 3:
        if roe[0] <= roe[1] <= roe[2] or roe[0] >= roe[1] >= roe[2]:
            roe = roe[2]
        else:
            roe = (roe[0] + roe[1] * 2 + roe[2] * 3) / 6     # weighting average
        return roe
    elif l > 0:
        return roe[l-1]
    else:
        return 0

# if __name__ == "__main__":
#     k = reader.get_5years_earning_rate()
#
    # price_w = estimate_price("005930")
    # print('price_w', price_w)
#     #price_w_10 = estimate_price("005930", w=0.9)
#     #price_w_20 = estimate_price("005930", w=0.8)
#     #k = reader.get_5years_earning_rate()
#     #print(get_disparity("005930", k, w=0.3))
#
#     print(estimate_price("023460", k))



