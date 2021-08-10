import os
import pandas as pd
import numpy as np
import pymysql
import time
import math
from dotenv import load_dotenv

#DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')

    def updateFinancialStatements(self, jcode, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')

        print(dataSet);

        # revenue = dataSet['매출액']
        # operating_income = dataSet['영업이익']
        # net_income = dataSet['당기순이익']
        # asset = dataSet['자산']
        # liability = dataSet['부채']
        # equity = dataSet['자본']
        # cashflow_operating = dataSet['영업활동으로인한현금흐름']

        # print('==============', ~np.isnan(revenue))

        revenue = dataSet['매출액'] if ~np.isnan(dataSet['매출액']) else None
        operating_income = dataSet['영업이익'] if ~np.isnan(dataSet['영업이익']) else None
        net_income = dataSet['당기순이익'] if ~np.isnan(dataSet['당기순이익']) else None
        asset = dataSet['자산'] if ~np.isnan(dataSet['자산']) else None
        liability = dataSet['부채'] if ~np.isnan(dataSet['부채']) else None
        equity = dataSet['자본'] if ~np.isnan(dataSet['자본']) else None
        cashflow_operating = dataSet['영업활동으로인한현금흐름'] if ~np.isnan(dataSet['영업활동으로인한현금흐름']) else None

        print('update start', dataSet['매출액'], jcode, yyyymm, revenue, operating_income, net_income, asset, liability, equity, cashflow_operating)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select jcode from financeinnfos where jcode=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (jcode, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinnfos ' \
                          '(jcode, yyyymm, revenue, operating_income, net_income, asset, liability, equity, cashflow_operating) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (jcode, yyyymm, revenue, operating_income, net_income, asset, liability, equity, cashflow_operating))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinnfos set ' \
                          'revenue=%s, ' \
                          'operating_income=%s, ' \
                          'net_income=%s, ' \
                          'asset=%s, ' \
                          'liability=%s, ' \
                          'equity=%s, ' \
                          'cashflow_operating=%s ' \
                          'where jcode=%s and yyyymm=%s'
                    curs.execute(sql, (revenue, operating_income, net_income, asset, liability, equity, cashflow_operating, jcode, yyyymm))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


    def updateFinancialRatio(self, jcode, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')

        # revenue = dataSet['매출액']
        # operating_income = dataSet['영업이익']
        # net_income = dataSet['당기순이익']
        # asset = dataSet['자산']
        # liability = dataSet['부채']
        # equity = dataSet['자본']
        # cashflow_operating = dataSet['영업활동으로인한현금흐름']

        # print('==============', ~np.isnan(revenue))
        print('update start', jcode, yyyymm, dataSet)
        current_ratio = dataSet['유동비율'] if ~np.isnan(dataSet['유동비율']) else None
        debt_ratio = dataSet['부채비율'] if ~np.isnan(dataSet['부채비율']) else None
        net_profit_margin = dataSet['영업이익률'] if ~np.isnan(dataSet['영업이익률']) else None
        roa = dataSet['ROA'] if ~np.isnan(dataSet['ROA']) else None
        roic = dataSet['ROIC'] if ~np.isnan(dataSet['ROIC']) else None

        print('update start', jcode, yyyymm, current_ratio, debt_ratio, net_profit_margin, roa, roic)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select jcode from financeinnfos where jcode=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (jcode, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinnfos ' \
                          '(jcode, yyyymm, current_ratio, debt_ratio, net_profit_margin, roa, roic) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (jcode, yyyymm, current_ratio, debt_ratio, net_profit_margin, roa, roic))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinnfos set ' \
                          'current_ratio=%s, ' \
                          'debt_ratio=%s, ' \
                          'net_profit_margin=%s, ' \
                          'roa=%s, ' \
                          'roic=%s ' \
                          'where jcode=%s and yyyymm=%s'
                    curs.execute(sql, ( current_ratio, debt_ratio, net_profit_margin, roa, roic, jcode, yyyymm))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


    def updateInvestmentIndiators(self, jcode, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')

        # revenue = dataSet['매출액']
        # operating_income = dataSet['영업이익']
        # net_income = dataSet['당기순이익']
        # asset = dataSet['자산']
        # liability = dataSet['부채']
        # equity = dataSet['자본']
        # cashflow_operating = dataSet['영업활동으로인한현금흐름']

        # print('==============', ~np.isnan(revenue))
        print('update start', jcode, yyyymm, dataSet)
        per = dataSet['PER'] if ~np.isnan(dataSet['PER']) else None
        pcr = dataSet['PCR'] if ~np.isnan(dataSet['PCR']) else None
        psr = dataSet['PSR'] if ~np.isnan(dataSet['PSR']) else None
        pbr = dataSet['PBR'] if ~np.isnan(dataSet['PBR']) else None
        total_cashflow = dataSet['총현금흐름'] if ~np.isnan(dataSet['총현금흐름']) else None

        print('update start', jcode, yyyymm, per, pcr, psr, pbr, total_cashflow)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select jcode from financeinnfos where jcode=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (jcode, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinnfos ' \
                          '(jcode, yyyymm, per, pcr, psr, pbr, total_cashflow) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (jcode, yyyymm, per, pcr, psr, pbr, total_cashflow))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinnfos set ' \
                          'per=%s, ' \
                          'pcr=%s, ' \
                          'psr=%s, ' \
                          'pbr=%s, ' \
                          'total_cashflow=%s ' \
                          'where jcode=%s and yyyymm=%s'
                    curs.execute(sql, ( per, pcr, psr, pbr, total_cashflow, jcode, yyyymm))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass

    #
    # def financeinfos(self):
    #     cur = self.conn.cursor()
    #     sql = "SELECT id, jcode, name, q1, q2, created_at, updated_at FROM financeinnfo ORDER BY id desc"
    #     cur.execute(sql)
    #
    #     rows = cur.fetchall()
    #     return rows
    #
    # def updateCorporations(self, market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region):
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select id, code from corporations where code=%s limit 0, 1"
    #             curs.execute(sql, (code))
    #             # columns = curs.description
    #             # print(columns)
    #
    #             # rs = curs.fetchall()
    #             rs = curs.fetchone()
    #             print(rs)
    #
    #             if rs == None:  # 값이 없을 경우 현재 값 입력
    #                 print('None')
    #                 sql = 'insert into corporations ' \
    #                       '(market, code, comp_name, industry, products, listed_at, sett_month, ceo, url, region, created_at, updated_at) ' \
    #                       'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #                 curs.execute(sql, (
    #                 market, str(code), comp_name, industry, products, listed_at, sett_month, ceo, url, region,
    #                 time.strftime('%Y-%m-%d %H:%M:%S'),
    #                 time.strftime('%Y-%m-%d %H:%M:%S')))
    #
    #                 self.conn.commit()
    #             else:
    #                 sql = 'update corporations set '\
    #                       'market=%s, '\
    #                       'comp_name=%s, '\
    #                       'industry=%s, '\
    #                       'products=%s, '\
    #                       'listed_at=%s, '\
    #                       'sett_month=%s, '\
    #                       'ceo=%s, '\
    #                       'url=%s, '\
    #                       'region=%s, '\
    #                       'updated_at=%s '\
    #                       'where id=%s'
    #                 curs.execute(sql, (
    #                     market, comp_name, industry, products, listed_at, sett_month, ceo, url, region, time.strftime('%Y-%m-%d %H:%M:%S'), rs['id']))
    #                 self.conn.commit()
    #
    #                     # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
    #     finally:
    #         pass
    #
    def corporations(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code, comp_name from corporations"
                curs.execute(sql)

                rs = curs.fetchall()
                return rs
        finally:
            pass

    # def codeFromCompName(self, comp_name):
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             # sql = "select comp_name from corporations"
    #             # curs.execute(sql)
    #             sql = "select code from corporations where comp_name=%s limit 0, 1"
    #             curs.execute(sql, (comp_name))
    #             rs = curs.fetchone()
    #
    #             if rs == None:  # 값이 없을 경우 현재 값 입력
    #                 return ''
    #             else:
    #                 return rs['code']
    #     finally:
    #         pass

    def close(self):
        self.conn.close()
