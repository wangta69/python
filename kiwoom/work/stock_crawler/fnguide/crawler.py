import requests
import time
from utils_magic import MagicUtil
from stock_crawler.connMysql import Mysql

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
            code = MagicUtil.make_code(row['code'])
            try:
                time.sleep(0.1)
                try:
                    fs_df = MagicUtil.make_fs_dataframe(code)
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
    def createInvestmentIndiators(self):
        """
        투자지표를 구한다. (per, pcr, psr, pbr, 총현금흐름)
        :return:
        """
        corporations = self.mysql.corporations()

        for row in corporations:
            code = MagicUtil.make_code(row['code'])
            try:
                time.sleep(0.1)
                try:
                    invest_df = MagicUtil.make_invest_dataframe(code)
                except requests.exceptions.Timeout:
                    time.sleep(10)
                    invest_df = MagicUtil.make_invest_dataframe(code)

                for idx, column in invest_df.iteritems():
                    trimcode = code.replace('A', '')
                    self.mysql.updateInvestmentIndiators(trimcode, idx, column)
            except ValueError as e:
                print('I got a ValueError - reason "%s"' % str(e))
                continue
            except KeyError as e:
                print('I got a KeyError - reason "%s"' % str(e))
                continue

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
    #     fs_df = MagicUtil.make_invest_dataframe(code)
    #     for idx, column in fs_df.iteritems():
    #         # print('idx', idx)
    #         # print(column)
    #         trimcode = code.replace('A', '')
    #         self.mysql.updateInvestmentIndiators(trimcode, idx, column)
    #     pass

    # 증권사별 적정주가 & 투자의견
    def crawlingConsensus(self):
        corporations = self.mysql.corporations()

        for row in corporations:
            code = MagicUtil.make_code(row['code'])
            result = MagicUtil.crawalConsensus(code)
            if len(result['comp']) > 0:
                self.mysql.deleteConsensusEstimate(row['code'])
                for r in result['comp']:
                    print(r)
                    self.mysql.updateConsensusEstimate(row['code'], r)


        pass


    def crawalSvdMain(self, code=None):
        """
        종가, 최고가, 수익률, 시가총액, 발생주식수(보통주 / 우선주)
        투자의견, 목표주가, EPS, PER, 추정기관수
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
            print('start1')
            self.util.crawalSvdFinance(code)
        else:
            print('start1')
            corporations = self.mysql.corporations()
            for row in corporations:
                self.util.crawalSvdFinance(row['code'])


if __name__ == "__main__":
    fnguide = Fnguide()

    # 1
    # fnguide.crawalSvdMain()
    fnguide.crawalSvdMain('023960')


    #2 (update yearly)
    # fnguide.crawalFinancialRatio()

    #3 (update yearly)
    # fnguide.crawalFinance()


    # fnguide.createFinancialStatementsToDB('A386580')
    # fnguide.createInvestmentIndiatorsToDB('A004840')
    # fnguide.createFinancialStatementsTest('A005930')



    # fnguide.createFinancialStatements()
    # fnguide.createFinancialRatio()
    # fnguide.createInvestmentIndiators()
    # fnguide.crawlingConsensus()






