import requests
import bs4
import pandas as pd
import time
from utils_magic import MagicUtil
#file_path = '마법공식 데이터.xlsx'
#path = 'data.xls'
from connMysql import Mysql
'''
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']
for num, code in enumerate(firmcode_list):
    fs_df = make_fs_dataframe(code)
    fs_df_changed = change_df(code, fs_df)
    if num == 0 :
        total_fs = fs_df_changed
    else:
        total_fs = pd.concat([total_fs, fs_df_changed])
print(total_fs)
'''

'''
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']
for num, code in enumerate(firmcode_list):
    fr_df = make_fr_dataframe(code)
    fr_df_changed = change_df(code, fr_df)
    if num == 0 :
        total_fr = fr_df_changed
    else:
        total_fr = pd.concat([total_fr, fr_df_changed])
print(total_fr)
'''

'''
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']
for num, code in enumerate(firmcode_list):
    invest_df = make_invest_dataframe(code)
    invest_df_changed = change_df(code, invest_df)
    if num == 0 :
        total_invest = invest_df_changed
    else:
        total_invest = pd.concat([total_invest, invest_df_changed])
print(total_invest)
'''

path = './data/data.sample.xls'
code_data = pd.read_excel(path)
code_data = code_data[['종목코드', '기업명']]
# print(code_data)

code_data['종목코드'] = code_data['종목코드'].apply(MagicUtil.make_code)

# print(code_data)

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


    # def createFinancialStatements(self):
    #     corporations = self.mysql.corporations()
    #     num = 0
    #     for row in corporations:
    #         code = MagicUtil.make_code(row['code'])
    #         try:
    #             time.sleep(0.1)
    #             try:
    #                 fs_df = MagicUtil.make_fs_dataframe(code)
    #             except requests.exceptions.Timeout:
    #                 time.sleep(10)
    #                 fs_df = MagicUtil.make_fs_dataframe(code)
    #             fs_df_changed = MagicUtil.change_df(code, fs_df)
    #             if num == 0:
    #                 total_fs = fs_df_changed
    #             else:
    #                 total_fs = pd.concat([total_fs, fs_df_changed])
    #             num = num + 1
    #         except ValueError as e:
    #             print('I got a ValueError - reason "%s"' % str(e))
    #             continue
    #         except KeyError as e:
    #             print('I got a KeyError - reason "%s"' % str(e))
    #             continue
    #
    #     total_fs.to_excel('재무제표데이터.xlsx')

    # createFinancialStatements()

    # 재무비율데이터
    def createFinancialRatio(self):
        corporations = self.mysql.corporations()
        # for num, code in enumerate(code_data['종목코드']):
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


    # def createFinancialRatio(self):
    #     corporations = self.mysql.corporations()
    #     num = 0
    #     # for num, code in enumerate(code_data['종목코드']):
    #     for row in corporations:
    #         code = MagicUtil.make_code(row['code'])
    #         print(num, code)
    #         try:
    #             time.sleep(0.1)
    #             try:
    #                 fr_df = MagicUtil.make_fr_dataframe(code)
    #             except requests.exceptions.Timeout:
    #                 time.sleep(10)
    #                 fr_df = MagicUtil.make_fr_dataframe(code)
    #             fr_df_changed = MagicUtil.change_df(code, fr_df)
    #             if num == 0 :
    #                 total_fr = fr_df_changed
    #             else:
    #                 total_fr = pd.concat([total_fr, fr_df_changed])
    #             num = num + 1
    #         except ValueError as e:
    #             print('I got a ValueError - reason "%s"' % str(e))
    #             continue
    #         except KeyError as e:
    #             print('I got a KeyError - reason "%s"' % str(e))
    #             continue
    #     total_fr.to_excel('재무비율데이터.xlsx')

    # 투자지표데이터
    def createInvestmentIndiators(self):
        corporations = self.mysql.corporations()
        # for num, code in enumerate(code_data['종목코드']):
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

    # def createInvestmentIndiators(self):
    #     corporations = self.mysql.corporations()
    #     num = 0
    #     # for num, code in enumerate(code_data['종목코드']):
    #     for row in corporations:
    #         code = MagicUtil.make_code(row['code'])
    #         print(num, code)
    #         try:
    #             time.sleep(0.1)
    #             try:
    #                 invest_df = MagicUtil.make_invest_dataframe(code)
    #             except requests.exceptions.Timeout:
    #                 time.sleep(10)
    #                 invest_df = MagicUtil.make_invest_dataframe(code)
    #             invest_df_changed = MagicUtil.change_df(code, invest_df)
    #             print(invest_df_changed)
    #             if num == 0 :
    #                 total_invest = invest_df_changed
    #             else:
    #                 total_invest = pd.concat([total_invest, invest_df_changed])
    #             num = num + 1
    #         except ValueError as e:
    #             print('I got a ValueError - reason "%s"' % str(e))
    #             continue
    #         except KeyError as e:
    #             print('I got a KeyError - reason "%s"' % str(e))
    #             continue
    #     total_invest.to_excel('투자지표데이터.xlsx')


    # 재무제표데이터
    def createFinancialStatementsToDB(self, code):
        fs_df = MagicUtil.make_fs_dataframe(code)
        for idx, column in fs_df.iteritems():
            # print('idx', idx)
            # print(column)
            trimcode = code.replace('A', '')
            self.mysql.updateFinancialStatements(trimcode, idx, column)

    # 재무비율데이터
    def createFinancialRatioToDB(self, code):
        fs_df = MagicUtil.make_fr_dataframe(code)
        for idx, column in fs_df.iteritems():
            # print('idx', idx)
            # print(column)
            trimcode = code.replace('A', '')
            self.mysql.updateFinancialRatio(trimcode, idx, column)
        pass

    # 투자지표데이터
    def createInvestmentIndiatorsToDB(self, code):
        fs_df = MagicUtil.make_invest_dataframe(code)
        for idx, column in fs_df.iteritems():
            # print('idx', idx)
            # print(column)
            trimcode = code.replace('A', '')
            self.mysql.updateInvestmentIndiators(trimcode, idx, column)
        pass

quant = Quant()
# quant.createFinancialStatementsToDB('A004840')
# quant.createFinancialRatioToDB('A004840')
# quant.createInvestmentIndiatorsToDB('A004840')
# quant.createFinancialStatements()
# quant.createFinancialRatio()
quant.createInvestmentIndiators()