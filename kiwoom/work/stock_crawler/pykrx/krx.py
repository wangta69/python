import numpy as np
import pandas as pd
from pandas import DataFrame
from stock_crawler.database.connMysql import Mysql
import requests
from stock_crawler.investing.utils.extra import random_user_agent

class KRXCrawler:
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    @property
    def url(self):
        return "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

    @property
    def headers(self):
        return {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def readeCorp(self):
        print(self.url)
        url = self.url + '?mktsel=ALL&secuGrpCd=1&searchText=&bld=dbms%2Fcomm%2Ffinder%2Ffinder_srtisu'
        page = requests.get(url, headers=self.headers)
        page.encoding = 'utf-8-sig'
        # print(url)
        # print(page.json()['block1'])

        for r in page.json()['block1']:
            print('---------------')
            print(r['full_code'], r['short_code'])
            self.mysql.updateKrxCode(r['short_code'], r['full_code'])

    def getShorting(self, isuCd, strtDd, endDd):
        # print(self.url)
        bld = 'dbms/MDC/STAT/srt/MDCSTAT30001'
        url = self.url + '?bld=' + bld + '&isuCd=' + isuCd + '&strtDd=' + strtDd + '&endDd=' + endDd
        page = requests.get(url, headers=self.headers)
        # print(url)
        # print(page.json()['OutBlock_1'])
        for r in page.json()['OutBlock_1']:
            print('---------------')
            print(r)
            yyyymmdd = r['TRD_DD'].replace('/', '-') # 날짜 2021/10/14
            volume = r['CVSRTSELL_TRDVOL']  # 전체 공매도 거래량 = 업틱룰 적용 공매도 + 업틱룰 예외 공매도
            r['UPTICKRULE_APPL_TRDVOL'] # 업틱룰 적용 공매도 거래량
            r['UPTICKRULE_EXCPT_TRDVOL'] # 업틱룰 예외 공매도 거래량
            v_remain = r['STR_CONST_VAL1'] # 남은 수량
            tr_amount = r['CVSRTSELL_TRDVAL'] # 전체 공매도 거래 금액
            r['UPTICKRULE_APPL_TRDVAL'] # 업틱룰 적용 공매도 거래 금액
            r['UPTICKRULE_EXCPT_TRDVAL'] # 업틱룰 예외 공매도 거래 금액
            remain_amount = r['STR_CONST_VAL2'] # 남은 금액
            
            
            # print(r['TRD_DD'], r['CVSRTSELL_TRDVOL'])
            # self.mysql.updateKrxCode(r['short_code'], r['full_code'])
        pass

    #
    # def get_stock_ticker_isin(ticker):
    #     s = StockTicker().get(ticker)
    #     return s['ISIN']
    #
    # class 개별종목_공매도_종합정보(KrxWebIo):
    #     @property
    #     def bld(self):
    #         return "dbms/MDC/STAT/srt/MDCSTAT30001"
    #
    #     def fetch(self, strtDd: str, endDd: str, isuCd: str) -> DataFrame:
    #         """[31001] 개별종목 공매도 종합정보
    #         Args:
    #             strtDd (str): 조회 시작 일자 (YYMMDD)
    #             endDd  (str): 조회 종료 일자 (YYMMDD)
    #             isuCd  (str): 조회 종목 ISIN
    #         Returns:
    #             DataFrame:
    #                 >> 개별종목_공매도_종합정보().fetch("20210101", "20210115", "KR7005930003")
    #                        TRD_DD CVSRTSELL_TRDVOL STR_CONST_VAL1 CVSRTSELL_TRDVAL   STR_CONST_VAL2
    #                 0  2021/01/15                0      3,365,984                0  296,206,592,000
    #                 1  2021/01/14            1,432      3,374,585      127,498,700  302,700,274,500
    #                 2  2021/01/13              228      3,268,098       20,571,200  293,148,390,600
    #                 3  2021/01/12            5,144      3,659,530      466,020,200  331,553,418,000
    #                 4  2021/01/11              204      3,152,160       18,686,400  286,846,560,000
    #         """
    #         result = self.read(isuCd=isuCd, strtDd=strtDd, endDd=endDd)
    #         return DataFrame(result['OutBlock_1'])
    #
    # def get_shorting_status_by_date(fromdate, todate, ticker):
    #     """일자별 공매도 종합 현황
    #     :param fromdate: 조회 시작 일자   (YYYYMMDD)
    #     :param todate  : 조회 종료 일자 (YYYYMMDD)
    #     :param ticker  : 종목 번호
    #     :return        : 종합 현황 DataFrame
    #                   공매도    잔고   공매도금액     잔고금액
    #         날짜
    #         20180105   41726  177954   3303209900  14111752200
    #         20180108   32411  167754   2528196100  13118362800
    #         20180109   50486  175261   3885385100  13477570900
    #     """
    #     isin = get_stock_ticker_isin(ticker)
    #     df = 개별종목_공매도_종합정보().fetch(fromdate, todate, isin)
    #     df = df[['TRD_DD', 'CVSRTSELL_TRDVOL', 'STR_CONST_VAL1', 'CVSRTSELL_TRDVAL',
    #              'STR_CONST_VAL2']]
    #     df.columns = ['날짜', '거래량', '잔고수량', '거래대금', '잔고금액']
    #     df = df.set_index('날짜')
    #     df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
    #
    #     # '-'는 데이터가 집계되지 않은 것을 의미한다.
    #     # 최근 2일 간의 데이터 ([:2])에서 '-'가 하나는 행의 갯수를 계산함
    #     idx = (df.iloc[:2] == '-').any(axis=1).sum()
    #     df = df.iloc[idx:]
    #
    #     df = df.replace('\D', '', regex=True)
    #     df = df.replace('', 0)
    #     df = df.astype({"거래량": np.int32, "잔고수량": np.int32,
    #                     "거래대금": np.int64, "잔고금액": np.int64})
    #     return df.sort_index()