from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from pykrx import stock
import datetime
import pandas as pd
import matplotlib.pyplot as plt
# 참조 : https://yobro.tistory.com/202

dt_now = datetime.datetime.now()
COM_DATE = dt_now.strftime('%Y%m%d') # 기준일자 600 거래일 전일 부터 현제까지 받아옴

class Foreigner(QAxWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

    def info(self):
        kospi = stock.get_exhaustion_rates_of_foreign_investment_by_ticker(COM_DATE, 'KOSPI')
        kosdaq = stock.get_exhaustion_rates_of_foreign_investment_by_ticker(COM_DATE, 'KOSDAQ')
        stocks = pd.concat([kospi, kosdaq], axis=0)


        df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

        df = df[['회사명', '종목코드']]
        df['종목코드'] = df['종목코드'].astype(str)
        df['종목코드'] = df['종목코드'].apply(lambda x: '00' + str(x) if len(str(x)) == 4 else x)
        df['종목코드'] = df['종목코드'].apply(lambda x: '0' + str(x) if len(str(x)) == 5 else x)
        df2 = df.set_index('종목코드')

        table = pd.merge(left=df2, right=stocks, how='left', left_on=df2.index, right_on=stocks.index)
        table = table.dropna()
        table = table.rename(columns={'key_0':'code'})
        table = table.set_index('code')

        # top 10 종목 구하기
        table = table.sort_values(by='한도소진율', ascending=False)
        sojin = table[:10]

        # Plot 출력하기
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.size'] = 12
        plt.figure(figsize=(16, 8))

        plt.bar(sojin['회사명'], sojin['한도소진율'])
        for x,y in enumerate(list(sojin['한도소진율'])):
            plt.text(x, y, '{:.2f}%'.format(y), fontsize=13, color='#ff0000',
                     horizontalalignment='center', verticalalignment='bottom')
            plt.title('11월 20일 종목별 외국인 소진율 Top 10')
            plt.show()
        # print(sojin)
