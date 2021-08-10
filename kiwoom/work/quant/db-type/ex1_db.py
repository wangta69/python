import requests
import time
from utils_magic import MagicUtil
from connMysql import Mysql

class Quant():
    def __init__(self, parent=None):
        super().__init__()
        self.mysql = Mysql()

    # 재무제표데이터
    def createFinancialStatements(self):
        corporations = self.mysql.corporations()
        for row in corporations:
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
                continue
            except KeyError as e:
                print('I got a KeyError - reason "%s"' % str(e))
                continue


    # 재무비율데이터
    def createFinancialRatio(self):
        corporations = self.mysql.corporations()

        for row in corporations:
            code = MagicUtil.make_code(row['code'])
            try:
                time.sleep(0.1)
                try:
                    fr_df = MagicUtil.make_fr_dataframe(code)
                except requests.exceptions.Timeout:
                    time.sleep(10)
                    fr_df = MagicUtil.make_fr_dataframe(code)

                for idx, column in fr_df.iteritems():
                    trimcode = code.replace('A', '')
                    self.mysql.updateFinancialRatio(trimcode, idx, column)
            except ValueError as e:
                print('I got a ValueError - reason "%s"' % str(e))
                continue
            except KeyError as e:
                print('I got a KeyError - reason "%s"' % str(e))
                continue

    # 투자지표데이터
    def createInvestmentIndiators(self):
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
    #         self.mysql.updateFinancialStatements(trimcode, idx, column)
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

quant = Quant()
# quant.createFinancialStatementsToDB('A004840')
# quant.createFinancialRatioToDB('A004840')
# quant.createInvestmentIndiatorsToDB('A004840')
# quant.createFinancialStatements()
# quant.createFinancialRatio()
# quant.createInvestmentIndiators()