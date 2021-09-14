import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
# from stock_crawler.database.connMysql import Mysql
# from stock_crawler.naver.util import Util
# import numpy as np

class Celebrity():
    def __init__(self):
        super().__init__()
        # self.mysql = Mysql()
        # self.util = Util()

    def crawler(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        params = {

        }

        p = 1
        url = 'https://superkts.com/people/list/?p=' + str(p)
        r = requests.get(url, headers=headers, data=params)
        tables = pd.read_html(r.text)
        # print(tables[0])

        for index, row in tables[0].iterrows():
            name = row['이름']
            job = row['직업']
            yyyymm = row['생일'][0:10].replace('.', '')
            print(name, job, yyyymm)

# http://sajugate.com/saju/celebs.php?page=1

if __name__ == "__main__":
    print(__name__)
    cel = Celebrity()
    # naver.updateMarketPrice()  # 시가종가등 모든 가격을 업데이트
    cel.crawler()




