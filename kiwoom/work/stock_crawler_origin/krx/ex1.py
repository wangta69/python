import pandas as pd
from connMysql import Mysql

class Corporation():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    def update(self):
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'  # 1

        kosdaq = pd.read_html(url + "?method=download&marketType=kosdaqMkt")[0]  # 2
        kospi = pd.read_html(url + "?method=download&marketType=stockMkt")[0]  # 3
        kosdaq.종목코드 = kosdaq.종목코드.astype(str).apply(lambda x: x.zfill(6))
        kospi.종목코드 = kospi.종목코드.astype(str).apply(lambda x: x.zfill(6))
        kosdaq['market'] = 'KQ'
        kospi['market'] = 'KS'

        stocks = kospi.append(kosdaq)  # kospi 뒤로 kosdaq dataframe을 합친다.
        stocks.sort_values(by="상장일", ascending=False)
        stocks = stocks.rename(
            columns={
                '회사명': 'comp_name',
                '종목코드': 'code',
                '업종': 'industry',
                '주요제품': 'products',
                '상장일': 'listed_at',
                '결산월': 'sett_month',
                '대표자명': 'ceo',
                '홈페이지': 'url',
                '지역': 'region'
            })

        stocks = stocks.where((pd.notnull(stocks)), None)

        for row in stocks.itertuples():
            # market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region
            print(row[10], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            self.mysql.updateCorporations(row[10], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

            # (야후금융에서는 코스피를 "KS", 코스닥을 "KQ"로 관리한다.)

corporation = Corporation()
corporation.update()


