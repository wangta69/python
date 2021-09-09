import requests
from bs4 import BeautifulSoup
import pandas as pd

#
def get_element_by_css_selector(url, selector, rawdata=False):
    try:
        resp = requests.get(url)
        html = resp.text
        soup = BeautifulSoup(html, "html5lib")
        tag = soup.select(selector)[0]

        if rawdata:
            return tag.text
        else:
            return float(tag.text.replace(",", ""))
    except Exception as e:
        print('[get_element_by_css_selector] I got a Exception  - reason "%s"' % str(e))
        return None

def get_5years_earning_rate():
    """
    BBB- 등급의  5년채 수익률을 가져온다.
    :return:
    """
    url = "https://www.kisrating.com/ratingsStatistics/statics_spread.do"
    selector = "#con_tab1 > div.table_ty1 > table > tbody > tr:nth-child(11) > td:nth-child(9)"
    ret = get_element_by_css_selector(url, selector)
    return ret

#
#
# def get_elements_by_css_selector(url, selector):
#     try:
#         resp = requests.get(url)
#         html = resp.text
#         soup = BeautifulSoup(html, "html5lib")
#         tags = soup.select(selector)
#         return tags
#     except:
#         return None
#
#
# def get_code_list_by_market(market=1):
#     """
#     get listed company information such as code and name
#     :param market: 1: all, 2: kospi, 3: kosdaq
#     :return: DataFrame
#     """
#     url = f"http://comp.fnguide.com/SVO2/common/lookup_data.asp?mkt_gb={market}&comp_gb=1"
#     resp = requests.get(url)
#     data = resp.json()
#     df = pd.DataFrame(data)
#     df = df.set_index('cd')
#     return df
#
#
#
# def make_acode(code):
#     '''
#     generate acode such as A005930, A000020
#     :param code:
#     :return: acode
#     '''
#     acode = None
#     if len(code) == 6:
#         acode = 'A' + code
#     elif len(code) == 7:
#         acode = 'A' + code[1:]
#     return acode
#
#

#
#
# def get_net_worth(code):
#     """
#     지배주주지분
#     :param code:
#     :return:
#     """
#     acode = make_acode(code)
#     url = f"http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode={acode}"
#     selector = "#highlight_D_A > table > tbody > tr:nth-child(10) > td:nth-child(4)"
#     ret = get_element_by_css_selector(url, selector)
#     print('get_net_worth', 'ret', ret)
#     try:
#         return ret * 100000000
#     except:
#         return 0
#
#
# def get_roe(code):
#     """
#     년간 roe
#     :param code:
#     :return:
#     """
#     acode = make_acode(code)
#     url = f"http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode={acode}"
#     selector = "#highlight_D_A > table > tbody > tr:nth-child(18) > td"
#     tags = get_elements_by_css_selector(url, selector)
#     vals = [tag.text for tag in tags]
#
#     roes = []
#     for x in vals:
#         try:
#             x = x.replace(',', '')
#             roes.append(float(x))
#         except:
#             roes.append(0)
#
#     roe3 = roes[:3]
#
#     # uptrend or downtrend
#     if roe3[0] <= roe3[1] <= roe3[2] or roe3[0] >= roe3[1] >= roe3[2]:
#         roe = roe3[2]
#     else:
#         roe = (roe3[0] + roe3[1] * 2 + roe3[2] * 3) / 6     # weighting average
#     return roe
#
#
# def get_shares(code):
#     acode = make_acode(code)
#     url = f"http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode={acode}"
#     selector = "#svdMainGrid1 > table > tbody > tr:nth-child(7) > td:nth-child(2)"
#     total_shares = get_element_by_css_selector(url, selector, rawdata=True)
#     total_shares = total_shares.split("/")[0]
#     total_shares = total_shares.replace(",", "")
#
#     print('total_shares', total_shares)
#     try:
#         total_shares = float(total_shares)
#     except:
#         total_shares = 0
#
#     selector = "#svdMainGrid5 > table > tbody > tr:nth-child(5) > td:nth-child(3)"
#     self_hold_shares = get_element_by_css_selector(url, selector)
#     if self_hold_shares is None:
#         self_hold_shares = 0
#
#     return total_shares - self_hold_shares
#
#
# def get_current_price(code):
#     acode = make_acode(code)
#     url = f"http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode={acode}"
#     selector = "#svdMainChartTxt11"
#     return get_element_by_css_selector(url, selector)

