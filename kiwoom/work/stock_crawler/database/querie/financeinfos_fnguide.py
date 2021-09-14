import pymysql
from stock_crawler.utils import *

# DB 테이블 칼럼대로 만든 객체
class Fnguide:
    def __init__(self, parent):
        self.parent = parent

    def updateFinancialStatements(self, code, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')
        if yyyymm[-2:] != '12':
            return

        dataSet = keyCheck(dataSet, ['매출액', '매출총이익', '영업이익', '당기순이익', '자산', '부채', '자본', '영업활동으로인한현금흐름'])

        revenue = dataSet['매출액']
        gross_profit = dataSet['매출총이익']
        operating_income = dataSet['영업이익']
        net_income = dataSet['당기순이익']
        asset = dataSet['자산']
        liability = dataSet['부채']
        equity = dataSet['자본']
        cashflow_operating = dataSet['영업활동으로인한현금흐름']

        print('update start', revenue, gross_profit, operating_income, net_income, asset, liability, equity,
              cashflow_operating)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from financeinfos_fnguide where code=%s and yyyymm=%s and flag=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm, 'y'))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinfos_fnguide ' \
                          '(code, flag, yyyymm, revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                    print(sql)
                    print(code, 'y', yyyymm, revenue, gross_profit, operating_income, net_income, asset, liability,
                          equity, cashflow_operating)
                    curs.execute(sql, (
                    code, 'y', yyyymm, revenue, gross_profit, operating_income, net_income, asset, liability, equity,
                    cashflow_operating))

                    conn.commit()
                else:
                    print('UPDATE', revenue, gross_profit, operating_income, net_income, asset, liability, equity,
                          cashflow_operating,
                          code, yyyymm)
                    sql = 'update financeinfos_fnguide set ' \
                          'revenue=%s, ' \
                          'gross_profit=%s, ' \
                          'operating_income=%s, ' \
                          'net_income=%s, ' \
                          'asset=%s, ' \
                          'liability=%s, ' \
                          'equity=%s, ' \
                          'cashflow_operating=%s ' \
                          'where code=%s and yyyymm=%s and flag=%s'
                    curs.execute(sql, (
                        revenue, gross_profit, operating_income, net_income, asset, liability, equity,
                        cashflow_operating,
                        code, yyyymm, 'y'))
                    conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
            # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


    def financeinfoFnguideFinancial(self, code, idx, column):
        column = keyCheck(column, ['매출액'])

        revenue = column['매출액'] if isNaN(column['매출액']) == False else None
        operating_income = column['영업이익'] if isNaN(column['영업이익']) == False else None
        # operating_income = column['영업이익(발표기준)'] if isNaN(column['영업이익(발표기준)']) == False else None
        net_income = column['당기순이익'] if isNaN(column['당기순이익']) == False else None
        net_income_in_controlling = column['지배주주순이익'] if isNaN(column['지배주주순이익']) == False else None
        net_income_non_controlling = column['비지배주주순이익'] if isNaN(column['비지배주주순이익']) == False else None
        controlling_shareholder = column['지배주주지분'] if isNaN(column['지배주주지분']) == False else None
        non_controlling_shareholder = column['비지배주주지분'] if isNaN(column['비지배주주지분']) == False else None
        # 자산총계, 부채총계, 자본총계, , , 자본금, 지배주주순이익률, 발행주식수, 배당수익률
        # operating_profit_margin = column['영업이익률'] if isNaN(column['영업이익률']) == False else None # 이부분은 실제 영업이익률과 달라서 아래 ratio를 별도로 처리
        # net_profit_margin = column['순이익률'] if isNaN(column['순이익률']) == False else None
        # roe = column['ROE(지배주주)'] if isNaN(column['ROE(지배주주)']) == False else None
        debt_ratio = column['부채비율'] if isNaN(column['부채비율']) == False else None
        # quick_ratio = column['당좌비율'] if column['당좌비율'] == False else None
        reserve_ratio = column['유보율'] if column['유보율'] == False else None
        roa = column['ROA'] if isNaN(column['ROA']) == False else None
        roe = column['ROE'] if isNaN(column['ROE']) == False else None
        eps = column['EPS(원)'] if isNaN(column['EPS(원)']) == False else None
        bps = column['BPS(원)'] if isNaN(column['BPS(원)']) == False else None
        dps = column['DPS(원)'] if isNaN(column['DPS(원)']) == False else None
        per = column['PER'] if isNaN(column['PER']) == False else None
        pbr = column['PBR'] if isNaN(column['PBR']) == False else None

        # print('debt_ratio', debt_ratio, isNaN(column['부채비율']))

        if idx[0] == 'Annual':
            flag = 'y'
        else:
            flag = 'q'

        print(idx[0])

        if len(idx[1]) > 10:
            print(idx[1] + '======================================')

        yyyymm = idx[1].replace('/', '')
        yyyymm = yyyymm.replace('(E)', '')
        yyyymm = yyyymm.replace('(P)', '')
        print(idx[1], yyyymm)

        if len(yyyymm) != 6:
            return

        print(yyyymm, len(yyyymm))

        # eps = column['주당순이익'] if data['주당순이익'] != '--' else None
        # eps_forcast = data['column'] if data['예측'] != '--' else None
        # revenue = data['column'] if data['매출'] != '--' else None
        # revenue_forcast = data['예측.1'] if data['예측.1'] != '--' else None
        # print(release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from financeinfos_fnguide where code=%s and flag=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (code, flag, yyyymm))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    print(code, flag, yyyymm, revenue, operating_income, net_income,
                          debt_ratio, reserve_ratio, roe, eps, per, bps, pbr)
                    sql = 'insert into financeinfos_fnguide ' \
                          '(code, flag, yyyymm, revenue, operating_income, net_income, ' \
                          'net_income_in_controlling, net_income_non_controlling, controlling_shareholder, non_controlling_shareholder, ' \
                          'debt_ratio, reserve_ratio, roe, eps, per, bps, pbr) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql,
                                 (code, flag, yyyymm, revenue, operating_income, net_income,
                                  net_income_in_controlling, net_income_non_controlling, controlling_shareholder,
                                  non_controlling_shareholder,
                                  debt_ratio, reserve_ratio, roe, eps, per, bps, pbr))

                    conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos_fnguide set ' \
                          'revenue=%s, ' \
                          'operating_income=%s, ' \
                          'net_income=%s, ' \
                          'net_income_in_controlling=%s, ' \
                          'net_income_non_controlling=%s, ' \
                          'controlling_shareholder=%s, ' \
                          'non_controlling_shareholder=%s, ' \
                          'debt_ratio=%s, ' \
                          'reserve_ratio=%s, ' \
                          'roe=%s, ' \
                          'eps=%s, ' \
                          'per=%s, ' \
                          'bps=%s, ' \
                          'pbr=%s ' \
                          'where id=%s'
                    curs.execute(sql, (revenue, operating_income, net_income,
                                       net_income_in_controlling, net_income_non_controlling, controlling_shareholder,
                                       non_controlling_shareholder,
                                       debt_ratio, reserve_ratio, roe, eps, per, bps, pbr, rs['id']))
                    conn.commit()
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateFinancialRatio(self, code, yyyymm, dataSet):

        yyyymm = yyyymm.replace('/', '')
        if yyyymm[-2:] == '12':
            flag = 'y'
        else:
            flag = 'q'

        current_ratio = dataSet['유동비율'] if ~np.isnan(dataSet['유동비율']) else None
        debt_ratio = dataSet['부채비율'] if ~np.isnan(dataSet['부채비율']) else None
        operating_profit_margin = dataSet['영업이익률'] if ~np.isnan(dataSet['영업이익률']) else None
        roa = dataSet['ROA'] if ~np.isnan(dataSet['ROA']) else None
        roic = dataSet['ROIC'] if ~np.isnan(dataSet['ROIC']) else None

        print('update start', code, yyyymm, current_ratio, debt_ratio, operating_profit_margin, roa, roic)
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from financeinfos_fnguide where code=%s and yyyymm=%s and flag=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm, flag))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinfos_fnguide ' \
                          '(code, flag, yyyymm, current_ratio, debt_ratio, operating_profit_margin, roa, roic) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql,
                                 (code, flag, yyyymm, current_ratio, debt_ratio, operating_profit_margin, roa, roic))

                    conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos_fnguide set ' \
                          'current_ratio=%s, ' \
                          'debt_ratio=%s, ' \
                          'operating_profit_margin=%s, ' \
                          'roa=%s, ' \
                          'roic=%s ' \
                          'where code=%s and yyyymm=%s and flag=%s'
                    curs.execute(sql,
                                 (current_ratio, debt_ratio, operating_profit_margin, roa, roic, code, yyyymm, flag))
                    conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
            # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass

    # srim 관련 데이타 가져오기
    def getControllingShareholder(self, code, yyyymm):
        """
        지배주주지분 가져오기
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select controlling_shareholder from financeinfos_fnguide WHERE code = %s AND yyyymm = %s AND flag = %s"
                curs.execute(sql, (code, yyyymm, 'y'))

                rs = curs.fetchone()
                return rs
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        # finally:
        #     pass

    def get3yearRoe(self, code, yyyymm):
        """
        3년간 roe가져오기
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select roe, yyyymm controlling_shareholder from financeinfos_fnguide WHERE code = %s AND flag = %s and yyyymm <= %s order by yyyymm desc limit 0, 3"
                curs.execute(sql, (code, 'y', yyyymm))

                rs = curs.fetchall()
                return rs
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        # finally:
        #     pass