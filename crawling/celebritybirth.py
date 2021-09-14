import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from connMysql import Mysql
# from stock_crawler.naver.util import Util
# import numpy as np

class Celebrity():
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()
        # self.util = Util()

    def crawler1(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        params = {

        }

        # print(tables[0])

        for p in range(1, 249):
            url = 'https://superkts.com/people/list/?p=' + str(p)
            print(url)
            r = requests.get(url, headers=headers, data=params)
            tables = pd.read_html(r.text)
            for index, row in tables[0].iterrows():
                name = row['이름']

                job = row['직업']
                birth_ym = row['생일'][0:10].replace('.', '')
                print(name, job, birth_ym)
                self.mysql.celebrity1(name, job, birth_ym)



    def crawler2(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        params = {

        }

        # print(tables[0])
        regex = "\(.*\)|\s-\s.*"
        for p in range(1, 8): #
            url = 'http://sajugate.com/saju/celebs.php?page=' + str(p)
            print(url)
            r = requests.get(url, headers=headers, data=params)
            tables = pd.read_html(r.text)
            # print(tables)
            for index, row in tables[0].iterrows():

                 nameall = row['이름']
                 name = re.sub(regex, '', nameall)
                 items = re.findall('\(([^)]+)', nameall)
                 gender = items[0]

                 yyyymmall = row['생년월일']
                 birth_ym = re.sub(regex, '', yyyymmall).replace('-', '')
                 items = re.findall('\(([^)]+)', yyyymmall)
                 s = items[0].split('/')

                 if s[0] == '양력':
                     sl = 'S'
                 elif s[0] == '음력':
                     sl = 'L'

                 flat_leap = s[1]

                 if row['생시'] == '생시모름':
                     ganji = ''
                     pass
                 else:
                     ganji = row['생시']

                 memo = row['메모']

                 if gender == '女':
                     gender = 'W'
                 elif gender == '男':
                     gender = 'M'



                 # birth_ym = row['생일'][0:10].replace('.', '')
                 print(name, gender, birth_ym, sl, flat_leap, ganji, memo)
                 self.mysql.celebrity2(name, gender, birth_ym, sl, flat_leap, ganji, memo)

# http://sajugate.com/saju/celebs.php?page=1

if __name__ == "__main__":
    cel = Celebrity()
    # cel.crawler1()
    # cel.crawler2()




