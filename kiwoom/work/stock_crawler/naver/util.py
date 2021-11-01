import requests
import pandas as pd
from bs4 import BeautifulSoup
# from stock_crawler_origin._connMysql import Mysql
from stock_crawler.database.connMysql import Mysql
from stock_crawler.utils import *
# from stock_crawler.investing.utils.extra import random_user_agent
class Util:
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    @property
    def headers(self):
        return {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def get_bs_obj(self, url):
        # if url == None:
        #     url = "https://finance.naver.com/item/main.nhn?code=" + code

        result = requests.get(url, headers=self.headers)
        bs_obj = BeautifulSoup(result.content, "html.parser")  # html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
        return bs_obj

    def 투자자별매매동향(self, code=None):

        if code:
            url = 'https://finance.naver.com/item/frgn.naver?code=' + code
            page = requests.get(url, headers=self.headers)

            # 당일 날짜를 얻기위해
            tables1 = pd.read_html(page.text, match='외국인 기관 순매매 거래량', encoding='utf-8')
            ymd = tables1[0].iloc[0, 0].replace('.', '-')
            print(ymd)

            tables2 = pd.read_html(page.text, match='거래원정보', encoding='utf-8')
            print (tables2[0])
            # tables[0].style.hide_index()
            for i, row in tables2[0].iterrows():

                if not isNaN(row['매도상위']) and row['매도상위'] != '외국계추정합':
                    print('================')
                    print(row)
                    s_corp = row['매도상위']
                    s_qty = row['거래량']
                    self.mysql.updateTopVolumeSector(code, ymd, 'S', s_corp, s_qty)

                    b_corp = row['매수상위']
                    b_qty = row['거래량.1']
                    self.mysql.updateTopVolumeSector(code, ymd, 'B', b_corp, b_qty)
        else:
            rows = self.mysql.corporations()
            for row in rows:
                code = row['code']
                try:
                    url = 'https://finance.naver.com/item/frgn.naver?code=' + code
                    page = requests.get(url, headers=self.headers)

                    # 당일 날짜를 얻기위해
                    tables1 = pd.read_html(page.text, match='외국인 기관 순매매 거래량', encoding='utf-8')
                    ymd = tables1[0].iloc[0, 0].replace('.', '-')
                    print(ymd)

                    tables2 = pd.read_html(page.text, match='거래원정보', encoding='utf-8')
                    print(tables2[0])
                    # tables[0].style.hide_index()
                    for i, row in tables2[0].iterrows():

                        if not isNaN(row['매도상위']) and row['매도상위'] != '외국계추정합':
                            print('================')
                            print(row)
                            s_corp = row['매도상위']
                            s_qty = row['거래량']
                            self.mysql.updateTopVolumeSector(code, ymd, 'S', s_corp, s_qty)

                            b_corp = row['매수상위']
                            b_qty = row['거래량.1']
                            self.mysql.updateTopVolumeSector(code, ymd, 'B', b_corp, b_qty)
                except ValueError as e:
                    print('I got a ValueError - reason "%s"' % str(e))
                finally:
                    pass

    # def get_price(self, code):
    #     print('code', code)
    #     try:
    #         bs_obj = self.get_bs_obj(code)
    #         no_today = bs_obj.find("p", {"class": "no_today"})
    #         blind_now = no_today.find("span", {"class": "blind"})
    #         return blind_now.text
    #     except:
    #         return '0'


    def print_stock_price(self, code, page_num):
        result = [[], [], [], [], [], [], [], [], []]
        # headers = {
        #     "User-Agent": random_user_agent(),
        #     "X-Requested-With": "XMLHttpRequest",
        #     "Accept": "text/html",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Connection": "keep-alive",
        # }
        # params = {
        #
        # }

        # r = requests.get(url, headers=self.headers)
        # print('r', r)
        #
        # if not r.ok:
        #     print('Not more data !')

        # html = r.content
        # soup = BeautifulSoup(html, 'html.parser')

        # for n in range(page_num):

        url = 'https://finance.naver.com/item/sise_day.nhn?code=' + code + '&page=' + str(page_num)
        soup = self.get_bs_obj(url)
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

    def MappingcategorySector(self, surl, sectorId):
        """
        섹터매핑
        :return:
        """
        url = 'https://finance.naver.com' + surl

        soup = self.get_bs_obj(url)
        tables = soup.find_all("table", attrs={'summary' : '업종별 시세 리스트'})
        for t in tables:
            links = t.find_all("a")
            for a in links:
                href = a.attrs['href']
                text = a.string
                try:
                    print(text, ">", href, ">", href[-6:])
                    self.mysql.MappingSector(href[-6:], sectorId)
                except:
                    pass
            pass

    def categorySector(self):
        """
        섹터매핑
        :return:
        """
        url = 'https://finance.naver.com/sise/sise_group.naver?type=upjong'
        soup = self.get_bs_obj(url)
        links = soup.find_all("a")

        for a in links:
            href = a.attrs['href']
            text = a.string
            try:
                if 'sise_group_detail.naver' in href:
                    print(text, ">", href)
                    sectorId = self.mysql.getSectorId(text)
                    self.MappingcategorySector(href, sectorId)
            except:
                pass
        pass


    def MappingcategoryTheme(self, surl, sectorId):
        """
        섹터매핑
        :return:
        """
        url = 'https://finance.naver.com' + surl

        soup = self.get_bs_obj(url)
        tables = soup.find_all("table", attrs={'summary' : '업종별 시세 리스트'})
        for t in tables:
            links = t.find_all("a")
            for a in links:
                href = a.attrs['href']
                text = a.string
                try:
                    if text:
                        print(text, ">", href, ">", href[-6:])
                        self.mysql.MappingTheme(href[-6:], sectorId)
                except:
                    pass
            pass

    def categoryTheme(self):
        """
        섹터매핑
        :return:
        """
        pageurl = 'https://finance.naver.com/sise/theme.naver' # ?&page=2
        soup = self.get_bs_obj(pageurl)
        pages = soup.find_all("table", attrs={'summary': '페이지 네비게이션 리스트'})
        for p in pages:
            links = p.find_all("a")
            for a in links:

                try:
                    href = a.attrs['href']
                    text = a.string
                    if text:
                        print(text, ">", href, ">", href[-6:])
                        url = 'https://finance.naver.com' + href
                        soup = self.get_bs_obj(url)
                        links = soup.find_all("a")
                        for a in links:
                            href = a.attrs['href']
                            text = a.string
                            try:
                                if 'sise_group_detail.naver' in href:

                                    themeId = self.mysql.getThemeId(text)
                                    print(text, ">", href, '>', themeId)
                                    self.MappingcategoryTheme(href, themeId)
                            except:
                                pass
                        pass

                except:
                    pass
            pass
        #
        # links = soup.find_all("a")
        #
        # for a in links:
        #     href = a.attrs['href']
        #     text = a.string
        #     # print(text + '>>' + href)
        #     try:
        #         if 'sise_group_detail.naver' in href:
        #             print(text, ">", href)
        #             # sectorId = self.mysql.getSectorId(text)
        #             # self.MappingcategorySector(href, sectorId)
        #     except:
        #         pass
        # pass