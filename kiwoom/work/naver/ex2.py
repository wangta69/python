# https://jsp-dev.tistory.com/193
# 적정주가 계산법 (사경인)


import traceback
# from lib.StockDB import *
from connMysql import Mysql
import time
import FinanceDataReader as fdr

if __name__ == "__main__":
    # 시작시간 측정
    start_time = time.time()
    # stock_db = StockDB()
    # stock_db.init()
    mysql = Mysql()

    code_list = mysql.select_all_codes()
    total_summary = []
    empty_finance = []
    # kospi code iterate
    for idx, row in enumerate(code_list):
        try:
            index, code, name, financial_crawl_date, daily_candle_date = row[0], row[1], row[2], row[3], row[4]
            finance_list = mysql.select_all_naver_finance(code).fillna(0)
            # 컬럼 지우기 0: for row, 1: for column
            finance_list = finance_list.drop('index', 1)
            '''
            s-rim계산에 필요한 것
            1. 자본총계(지배)
            2. ROE(%)
            3. 발행주식수(보통주)
            '''
            자기자본 = finance_list.loc['자본총계(지배)']['2020/03']
            ROE = (finance_list.loc['ROE(%)']['2020/03'] + finance_list.loc['ROE(%)']['2019/12']) / 2
            발행주식수 = finance_list.loc['발행주식수(보통주)']['2020/03'] or finance_list.loc['발행주식수(보통주)']['2019/12'] or \
            finance_list.loc['발행주식수(보통주)']['2018/12']
            PER = finance_list.loc['PER(배)']['2020/03']
            PBR = finance_list.loc['PBR(배)']['2020/03']
            억 = 100000000
            초과이익 = 자기자본 * 억 * (ROE - 7.9) / 100
            적정주가가치 = 자기자본 * 억 + 자기자본 * 억 * (ROE - 7.9) / 7.9
            적정주가 = 적정주가가치 / 발행주식수
            할인율10가치 = 자기자본 * 억 + 초과이익 * 0.9 / (1 + 0.079 - 0.9)
            적정주가_할인율10 = 할인율10가치 / 발행주식수
            할인율20가치 = 자기자본 * 억 + 초과이익 * 0.8 / (1 + 0.079 - 0.8)
            적정주가_할인율20 = 할인율20가치 / 발행주식수
            # 가격정보
            price_df = fdr.DataReader(code, '2020')
            today_close = price_df[-1:]['Close'][0]
            if today_close < 적정주가:
                info_summary = {'name': name, 'PBR': PBR, 'PER': PER, 'ROE': ROE, '적정주가': 적정주가,
                '적정주가_할인율10': 적정주가_할인율10, '적정주가_할인율20': 적정주가_할인율20}
                # ROE가 채권 수익률보다 작으면 할인율 적용한 적정 주가가 오히려 더 큰 값이 나온다.
            if today_close <= 적정주가_할인율20 <= 적정주가 and 적정주가_할인율20:
                diff = (적정주가_할인율20 - today_close) / today_close * 100
                info_summary['band'] = 1
                info_summary['diff'] = diff
            elif today_close <= 적정주가_할인율10 <= 적정주가 and 적정주가_할인율10:
                diff = (적정주가_할인율10 - today_close) / today_close * 100
                info_summary['band'] = 2
                info_summary['diff'] = diff
            else:
                diff = (적정주가 - today_close) / today_close * 100
                info_summary['band'] = 3
                info_summary['diff'] = diff
                total_summary.append(info_summary)
        except Exception as e:
         empty_finance.append(name)

    print(traceback.format_exc())
    print(total_summary)
    print(empty_finance)
    df = pd.DataFrame(total_summary)
    df['BPR'] = 1 / df['PBR'].astype(float) # BPR = 1/PBR
    df['1/PER'] = 1 / df['PER'].astype(float) # PER의 역수
    df['RANK_BPR'] = df['BPR'].rank(method='max', ascending=False) # BPR의 순위
    df['RANK_1/PER'] = df['1/PER'].rank(method='max', ascending=False) # 1/PER의 순위
    df['RANK_ROE'] = df['ROE'].rank(method='max', ascending=False) # BPR의 순위
    df['RANK_TOTAL'] = ((df['RANK_BPR'] + df['RANK_1/PER'] + df['RANK_ROE']) / 3 * df['band']).rank(method='max', ascending=True)
    df = df.sort_values(by=['RANK_TOTAL']) # 최종 순위로 정렬
    df = df.reset_index(drop=True)
    df.to_excel('s-rim_kospi_result.xlsx')
    print("--- %s seconds ---" % (time.time() - start_time))