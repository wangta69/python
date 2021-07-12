from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import pandas as pd
import numpy as np
from .financialStatementCrawling import Crawling
# https://youngwonhan-family.tistory.com/46
from connMysql import Mysql
from utils.trie import Trie

form_class = uic.loadUiType("ui/stockinfo/listedcorporation.ui")[0]

class ListedCorporation(QWidget, form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)  # 현재 form_class를 선택한다.
        self.radioKOSPI.clicked.connect(self.radioButtonClicked)
        self.radioKOSDAQ.clicked.connect(self.radioButtonClicked)
        self.updateButton.clicked.connect(self.update)
        # self.lineedit_Test.textChanged.connect(self.lineeditTextFunction)
        # self.lineEdit_search.returnPressed.connect(self.inquire_list_func)
        self.mysql = Mysql()
        self.insertKeyword()

    def radioButtonClicked(self):
        msg = ""
        if self.radioKOSPI.isChecked():
            msg = "코스피"
        elif self.radioKOSDAQ.isChecked():
            msg = "코스닥"
        else:
            msg = "-"
        print('radioButtonClicked', msg)
        # self.statusBar.showMessage(msg + "선택 됨")

    def update(self):
        msg = ""
        if self.radioKOSPI.isChecked():
            msg = "코스피"
        elif self.radioKOSDAQ.isChecked():
            msg = "코스닥"
        else:
            msg = "-"
        print('radioButtonClicked', msg)

        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'  # 1

        kosdaq = pd.read_html(url + "?method=download&marketType=kosdaqMkt")[0]  # 2
        kospi = pd.read_html(url + "?method=download&marketType=stockMkt")[0]  # 3
        kosdaq.종목코드 = kosdaq.종목코드.astype(str).apply(lambda x: x.zfill(6))
        kospi.종목코드 = kospi.종목코드.astype(str).apply(lambda x: x.zfill(6))
        kosdaq['market'] = 'KQ'
        kospi['market'] = 'KS'

        print(f'kosdaq length: {len(kosdaq)}, kospi length {len(kospi)}')
        # print(kosdaq)
        # print(kospi)
        # print(f'kosdaq length: {len(kosdaq)}')
        # print(kosdaq)
      #  print(kosdaq)
        # for i, row in kosdaq:

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

        print(stocks)
        # stocks = stocks.where((stocks.notnull(stocks)), None)
        stocks = stocks.where((pd.notnull(stocks)), None)

        # ms = np.vectorize(len)
        #
        # col_info = dict(zip(stocks, ms(df.values.astype(str)).max(axis=0)))
        # print(col_info) # 각 컬럼별 Maximum length를 참고하여 TABLE을 설계한다.

        for row in stocks.itertuples():
            # market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region
            print(row[10], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            self.mysql.updateCorporations(row[10], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

        # (야후금융에서는 코스피를 "KS", 코스닥을 "KQ"로 관리한다.)
    """
        검색용 키워드를 미리 입력해 둔다.
    """
    def insertKeyword(self):
        corporations = self.mysql.corporations()
        trie = Trie()

        for row in corporations:
            trie.insert(row['comp_name'])

        # result = trie.search("해성")
        # result = trie.search("car")

        result = trie.starts_with(('해성'))
        print('result', result)



