import os
import numpy as np
import pymysql
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

    def updateFinancialStatements(self, code, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')

        revenue = dataSet['매출액'] if ~np.isnan(dataSet['매출액']) else None
        operating_income = dataSet['영업이익'] if ~np.isnan(dataSet['영업이익']) else None
        net_income = dataSet['당기순이익'] if ~np.isnan(dataSet['당기순이익']) else None
        asset = dataSet['자산'] if ~np.isnan(dataSet['자산']) else None
        liability = dataSet['부채'] if ~np.isnan(dataSet['부채']) else None
        equity = dataSet['자본'] if ~np.isnan(dataSet['자본']) else None
        cashflow_operating = dataSet['영업활동으로인한현금흐름'] if ~np.isnan(dataSet['영업활동으로인한현금흐름']) else None

        print('update start', dataSet['매출액'], code, yyyymm, revenue, operating_income, net_income, asset, liability, equity, cashflow_operating)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from financeinfos where code=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinfos ' \
                          '(code, yyyymm, revenue, operating_income, net_income, asset, liability, equity, cashflow_operating) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (code, yyyymm, revenue, operating_income, net_income, asset, liability, equity, cashflow_operating))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos set ' \
                          'revenue=%s, ' \
                          'operating_income=%s, ' \
                          'net_income=%s, ' \
                          'asset=%s, ' \
                          'liability=%s, ' \
                          'equity=%s, ' \
                          'cashflow_operating=%s ' \
                          'where code=%s and yyyymm=%s'
                    curs.execute(sql, (revenue, operating_income, net_income, asset, liability, equity, cashflow_operating, code, yyyymm))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


    def updateFinancialRatio(self, code, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')

        current_ratio = dataSet['유동비율'] if ~np.isnan(dataSet['유동비율']) else None
        debt_ratio = dataSet['부채비율'] if ~np.isnan(dataSet['부채비율']) else None
        net_profit_margin = dataSet['영업이익률'] if ~np.isnan(dataSet['영업이익률']) else None
        roa = dataSet['ROA'] if ~np.isnan(dataSet['ROA']) else None
        roic = dataSet['ROIC'] if ~np.isnan(dataSet['ROIC']) else None

        print('update start', code, yyyymm, current_ratio, debt_ratio, net_profit_margin, roa, roic)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from financeinfos where code=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinfos ' \
                          '(code, yyyymm, current_ratio, debt_ratio, net_profit_margin, roa, roic) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (code, yyyymm, current_ratio, debt_ratio, net_profit_margin, roa, roic))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos set ' \
                          'current_ratio=%s, ' \
                          'debt_ratio=%s, ' \
                          'net_profit_margin=%s, ' \
                          'roa=%s, ' \
                          'roic=%s ' \
                          'where code=%s and yyyymm=%s'
                    curs.execute(sql, ( current_ratio, debt_ratio, net_profit_margin, roa, roic, code, yyyymm))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


    def updateInvestmentIndiators(self, code, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')

        per = dataSet['PER'] if ~np.isnan(dataSet['PER']) else None
        pcr = dataSet['PCR'] if ~np.isnan(dataSet['PCR']) else None
        psr = dataSet['PSR'] if ~np.isnan(dataSet['PSR']) else None
        pbr = dataSet['PBR'] if ~np.isnan(dataSet['PBR']) else None
        total_cashflow = dataSet['총현금흐름'] if ~np.isnan(dataSet['총현금흐름']) else None

        # print('update start', code, yyyymm, per, pcr, psr, pbr, total_cashflow)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from financeinfos where code=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinfos ' \
                          '(code, yyyymm, per, pcr, psr, pbr, total_cashflow) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (code, yyyymm, per, pcr, psr, pbr, total_cashflow))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos set ' \
                          'per=%s, ' \
                          'pcr=%s, ' \
                          'psr=%s, ' \
                          'pbr=%s, ' \
                          'total_cashflow=%s ' \
                          'where code=%s and yyyymm=%s'
                    curs.execute(sql, ( per, pcr, psr, pbr, total_cashflow, code, yyyymm))
                    self.conn.commit()

                        # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


    def updateOrder(self, yyyymm, setField, orderItem):

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:

                    sql = 'update financeinfos target ' \
                          'join ' \
                          '(' \
                          'select id, (@rownumber := @rownumber + 1) as rownum ' \
                          'from financeinfos ' \
                          'cross join (select @rownumber := 0) r ' \
                          ' where yyyymm = %s and {} is not null ' \
                          'order by {} asc ' \
                          ') source on target.id = source.id ' \
                          'set {} = rownum'

                    curs.execute(sql.format(orderItem, orderItem, setField), (yyyymm))
                    self.conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateScore(self, yyyymm):

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:

                    sql =   'UPDATE  financeinfos ' \
                            'SET     score_net_income = IF(net_income > 0, 1, 0), ' \
                            '        score_cashflow_operating = IF(cashflow_operating  > 0, 1, 0), ' \
                            '        score_diff = IF(cashflow_operating >  net_income, 1, 0), ' \
                            '        score_total = score_net_income +  score_cashflow_operating + score_diff ' \
                            'WHERE   yyyymm = %s'

                    curs.execute(sql, (yyyymm))
                    self.conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass


    def close(self):
        self.conn.close()



