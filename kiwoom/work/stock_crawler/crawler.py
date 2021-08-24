from stock_crawler.connMysql import Mysql

class Crawler():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()


crawler = Crawler()


