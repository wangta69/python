import requests
import time
from stock_crawler.fnguide.utils_magic import MagicUtil
from stock_crawler.database.connMysql import Mysql

class Fnguide():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()
        self.util = MagicUtil()

    # 재무제표데이터
    def createFinancialStatements(self):
        """
        포괄 손익계산서, 재무상태료, 현금흐름표를 구함
        :return:
        """
        corporations = self.mysql.corporations()
        for row in corporations:
            # 기존코드에서 A를 추가한 총 7자리 코드를 만든다(comp.fnguide.com)
            code = self.util.make_code(row['code'])
            try:
                time.sleep(0.1)
                try:
                    fs_df = self.util.make_fs_dataframe(code)
                except requests.exceptions.Timeout:
                    time.sleep(10)
                    fs_df = MagicUtil.make_fs_dataframe(code)

                for idx, column in fs_df.iteritems():
                    trimcode = code.replace('A', '')
                    self.mysql.updateFinancialStatements(trimcode, idx, column)
            except ValueError as e:
                print('I got a ValueError - reason "%s"' % str(e))
                print('At Code : ' + row['code'])
                continue
            except KeyError as e:
                print('I got a KeyError - reason "%s"' % str(e))
                print('At Code : ' + row['code'])
                continue

    # 재무제표데이터
    # def createFinancialStatementsTest(self, code):
    #     """
    #     포괄 손익계산서, 재무상태료, 현금흐름표를 구함
    #     :return:
    #     """
    #     fs_df = MagicUtil.make_fs_dataframe_test(code)
    #     print(fs_df)


    # 재무비율데이터
    # def createFinancialRatio(self):
    #     """
    #     유동비율, 부채비율, 영업이익율 roa, roic 등을 구함
    #     :return:
    #     """
    #     corporations = self.mysql.corporations()
    #
    #     for row in corporations:
    #         code = MagicUtil.make_code(row['code'])
    #         try:
    #             time.sleep(0.1)
    #             try:
    #                 fr_df = MagicUtil.make_fr_dataframe(code)
    #             except requests.exceptions.Timeout:
    #                 time.sleep(10)
    #                 fr_df = MagicUtil.make_fr_dataframe(code)
    #
    #             for idx, column in fr_df.iteritems():
    #                 trimcode = code.replace('A', '')
    #                 self.mysql.updateFinancialRatio(trimcode, idx, column)
    #         except ValueError as e:
    #             print('I got a ValueError - reason "%s"' % str(e))
    #             continue
    #         except KeyError as e:
    #             print('I got a KeyError - reason "%s"' % str(e))
    #             continue

    # 투자지표데이터
    # def createInvestmentIndiators(self):
    #     """
    #     투자지표를 구한다. (per, pcr, psr, pbr, 총현금흐름)
    #     :return:
    #     """
    #     corporations = self.mysql.corporations()
    #
    #     for row in corporations:
    #         code = self.util.make_code(row['code'])
    #         try:
    #             time.sleep(0.1)
    #             try:
    #                 invest_df = self.util.make_invest_dataframe(code)
    #             except requests.exceptions.Timeout:
    #                 time.sleep(10)
    #                 invest_df = self.util.make_invest_dataframe(code)
    #
    #             for idx, column in invest_df.iteritems():
    #                 trimcode = code.replace('A', '')
    #                 self.mysql.updateInvestmentIndiators(trimcode, idx, column)
    #         except ValueError as e:
    #             print('I got a ValueError - reason "%s"' % str(e))
    #             continue
    #         except KeyError as e:
    #             print('I got a KeyError - reason "%s"' % str(e))
    #             continue

    # # 재무제표데이터
    # def createFinancialStatementsToDB(self, code):
    #     fs_df = MagicUtil.make_fs_dataframe(code)
    #     for idx, column in fs_df.iteritems():
    #         # print('idx', idx)
    #         # print(column)
    #         trimcode = code.replace('A', '')
    #         # self.mysql.updateFinancialStatements(trimcode, idx, column)
    #
    # # 재무비율데이터
    # def createFinancialRatioToDB(self, code):
    #     fs_df = MagicUtil.make_fr_dataframe(code)
    #     for idx, column in fs_df.iteritems():
    #         # print('idx', idx)
    #         # print(column)
    #         trimcode = code.replace('A', '')
    #         self.mysql.updateFinancialRatio(trimcode, idx, column)
    #     pass
    #
    # # 투자지표데이터
    # def createInvestmentIndiatorsToDB(self, code):
    #     fs_df = self.util.make_invest_dataframe(code)
    #     for idx, column in fs_df.iteritems():
    #         # print('idx', idx)
    #         # print(column)
    #         trimcode = code.replace('A', '')
    #         self.mysql.updateInvestmentIndiators(trimcode, idx, column)
    #     pass

    # 증권사별 적정주가 & 투자의견
    def crawlingConsensus(self, code=None):
        if code:
            result = self.util.crawalConsensus(code)
            self.mysql.deleteConsensusEstimate(code)
            for r in result['comp']:
                self.mysql.updateConsensusEstimate(code, r)

        else:
            corporations = self.mysql.corporations()

            for row in corporations:
                result = self.util.crawalConsensus(row['code'])
                self.mysql.deleteConsensusEstimate(row['code'])
                if len(result['comp']) > 0:
                    for r in result['comp']:
                        self.mysql.updateConsensusEstimate(row['code'], r)


    def crawalSvdMain(self, code=None):
        """
        종가, 최고가, 수익률, 시가총액, 발행주식수(보통주 / 우선주)
        (투자의견, 목표주가, 추정기관수,) EPS, PER
        매출액, 영업이익, 당기순이익, 지배주주순이익, 자본총계, 자본금, 부채비율, 유보율, ROA, ROE, EPS, BPS, DPS, PER, PBR, 발생주식수
        :param code:
        :return:
        """
        if code:
            self.util.crawalSvdMain(code)
        else:
            corporations = self.mysql.corporations()
            for row in corporations:
                self.util.crawalSvdMain(row['code'])

    # 재무비율데이터
    def crawalFinancialRatio(self, code=None):
        """
        유동비율, 부채비율, 영업이익율 roa, roic 등을 구함
        :return:
        """
        if code:
            self.util.crawalSvdFinanceRatio(code)
        else:
            corporations = self.mysql.corporations()
            for row in corporations:
                self.util.crawalSvdFinanceRatio(row['code'])

    def crawalFinance(self, code=None):
        """
        '매출액', '매출총이익', '영업이익', '당기순이익', '자산', '부채', '자본', '영업활동으로인한현금흐름'
        :param code:
        :return:
        """
        if code:
            self.util.crawalSvdFinance(code)
        else:
            corporations = self.mysql.corporations()
            for row in corporations:
                self.util.crawalSvdFinance(row['code'])


if __name__ == "__main__":
    fnguide = Fnguide()

    # 1(매일처리)
    # fnguide.crawalSvdMain()
    # fnguide.crawalSvdMain('023960')

    # 2 (매일 처리) 명령실행후 관리자단에서 한번더 처리한다.
    fnguide.crawlingConsensus()
    # fnguide.crawlingConsensus('005930')

    #3 (update monthly)  2017/12 2018/12 2019/12  2020/12 2021/06
    # fnguide.crawalFinancialRatio()

    #4 (update yearly)
    # fnguide.crawalFinance()

    # fnguide.createFinancialStatements()
    # fnguide.createFinancialRatio()
    # fnguide.createInvestmentIndiators()







