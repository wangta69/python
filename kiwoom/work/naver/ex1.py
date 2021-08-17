#네이버 금융 삼성전자 데이터 수집
import requests
from bs4 import BeautifulSoup
import time
from connMysql import Mysql

class Naver():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def updatePrice(self):
        rows = self.mysql.corporations()
        for row in rows:
            time.sleep(0.1)
            price = self.get_price(row['code'])
            print(row['id'], price)
            self.mysql.updateCorporations(row['id'], price.replace(',', ''))


    def get_bs_obj(self, com_code):
        url = "https://finance.naver.com/item/main.nhn?code=" + com_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser") #html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
        return bs_obj

    def get_price(self, com_code):
        print('com_code', com_code)
        try:
            bs_obj = self.get_bs_obj(com_code)
            no_today = bs_obj.find("p", {"class":"no_today"})
            blind_now = no_today.find("span", {"class" : "blind"})
            return blind_now.text
        except:
            return '0'

naver = Naver()
naver.updatePrice()
