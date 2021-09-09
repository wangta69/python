import requests
from bs4 import BeautifulSoup
from stock_crawler_origin._connMysql import Mysql
from stock_crawler.utils import *

class Util:
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def get_bs_obj(self, code):
        url = "https://finance.naver.com/item/main.nhn?code=" + code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")  # html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
        return bs_obj

    def get_price(self, code):
        print('code', code)
        try:
            bs_obj = self.get_bs_obj(code)
            no_today = bs_obj.find("p", {"class": "no_today"})
            blind_now = no_today.find("span", {"class": "blind"})
            return blind_now.text
        except:
            return '0'


    def print_stock_price(self, code, page_num):
        result = [[], [], [], [], [], [], [], [], []]

        headers = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        params = {

        }

        # for n in range(page_num):
        url = 'https://finance.naver.com/item/sise_day.nhn?code=' + code + '&page=' + str(page_num)
        print(url)

        r = requests.get(url, headers=headers, data=params)
        print('r', r)

        if not r.ok:
            print('Not more data !')




        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('table > tr')


        for i in range(1, len(tr) - 1):
            td = tr[i].select('td')
            if td[0].text.strip():
                result[0].append(td[0].text.strip())  # 날짜
                result[1].append(td[1].text.strip())  # 종가

                img = td[2].select('img')
                if len(img) != 0:
                    if 'src' in img[0].attrs:
                        src = img[0]['src']
                        if 'up' in src:
                            result[2].append('상승')
                        else:
                            result[2].append('하락')
                else:
                    result[2].append('보합')

                result[3].append(td[2].text.strip())  # 전일대비
                result[4].append(td[3].text.strip())  # 시장가
                result[5].append(td[4].text.strip())  # 최고가
                result[6].append(td[5].text.strip())  # 최저가
                result[7].append(td[6].text.strip())  # 거래량
        return result;

        # for i in range(len(result[0])):
            # self.mysql.updateMarketPrices()
            
            #     날짜          종가           상승/하락/보합+a           시장가         최고가        최저가        거래량
            # print(result[0][i], result[1][i], result[2][i] + result[3][i], result[4][i], result[5][i], result[6][i],
            #       result[7][i])

    def get_market_prices(self, code, page_num=1):
        result = self.print_stock_price(code, page_num)
        for i in range(len(result[0])):
            yyyymm = result[0][i].replace('.', '-') # 날짜
            close = result[1][i].replace(',', '') # 종가 (현재가)
            open = result[4][i].replace(',', '') # 시가
            high = result[5][i].replace(',', '') # 고가
            low = result[6][i].replace(',', '') # 저가
            trade_qty = result[7][i].replace(',', '') # 거래량
            print(code, yyyymm, close, open, high, low, trade_qty)
            self.mysql.updateMarketPrices(code, yyyymm, close, open, high, low, trade_qty)
