import os
import pymysql
from dotenv import load_dotenv, dotenv_values

#DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        DOMAIN = os.getenv('DOMAIN')
        print(DOMAIN)
       # print('mysql test')
        # conn = pymysql.connect(host='localhost', user='mytest', password='akfldkDB', db='mytest', charset='utf8')




if __name__ == "__main__":
    test = Mysql()
    pass