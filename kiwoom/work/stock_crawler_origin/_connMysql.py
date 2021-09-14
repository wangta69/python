import os
import numpy as np
import pymysql
from dotenv import load_dotenv
from stock_crawler.utils import *


# DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
    
    # def corporations(self):
    #     """
    #     기업리스트 가져오기
    #     :return:
    #     """
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select id, code, investing_comp_name, common_stocks from corporations where status = 0"
    #             curs.execute(sql)
    #
    #             rs = curs.fetchall()
    #             return rs
    #     except Exception as e:
    #         print('I got a Exception  - reason "%s"' % str(e))
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    # def corporation(self, code):
    #     """
    #     기업정보 가져오기
    #     :return:
    #     """
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select common_stocks from corporations where code=%s"
    #             curs.execute(sql, (code))
    #
    #             rs = curs.fetchone()
    #             return rs
    #     except Exception as e:
    #         print('I got a Exception  - reason "%s"' % str(e))
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    def updateCorpStockPrice(self, id, price):
        """
        당일 종가 업데이트
        :param id: 
        :param price: 
        :return: 
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'stock_price=%s ' \
                      'where id=%s'
                curs.execute(sql, (price, id))
                self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass
    
    # fnguide 의 데이타를 이용해서 처리
    def updateCorpTotalShares(self, code, shares):
        """
        총주식수 업데이트 (보통주) 
        :param code: 
        :param shares: 
        :return: 
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'common_stocks=%s ' \
                      'where code=%s'
                curs.execute(sql, (
                    shares, code))
                self.conn.commit()
        except Exception as e:
            print('[updateCorpTotalShares] I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise
        finally:
            print('updateCorpTotalShares updated')
            pass

    def updateCorpRecom(self, code, df):

        """
        Deprecated
        투자의견 및 목표주가
        :param code:
        :param df:
        :return:
        """
        df = keyCheck(df, ['투자의견', '목표주가', '추정기관수', 'EPS', 'PER'])
        recom_cd = df['투자의견'][0]
        avg_prc = df['목표주가'][0]
        recom_cnt = df['추정기관수'][0]
        # eps = df['EPS'][0] # 추정치이므로 의미없음
        # per = df['PER'][0]
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set ' \
                      'recom_cd=%s, ' \
                      'avg_prc=%s, ' \
                      'recom_cnt=%s ' \
                      'where code=%s'
                curs.execute(sql, (
                    recom_cd, avg_prc, recom_cnt, code))
                self.conn.commit()
        except Exception as e:
            print('[updateCorpRecom] I got a Exception  - reason "%s"' % str(e))
            print(curs._last_executed)
            raise
        finally:
            print('updateCorpRecom updated')
            pass

    def updateCorpSrim(self, id, s_rim):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:

                sql = 'update corporations set ' \
                      's_rim=%s ' \
                      'where id=%s'
                curs.execute(sql, (s_rim, id))
                self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

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

        print('update start', revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from financeinfos_fnguide where code=%s and yyyymm=%s and flag=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm, 'y'))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into financeinfos_fnguide ' \
                          '(code, flag, yyyymm, revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                    print(sql)
                    print(code, 'y', yyyymm, revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating)
                    curs.execute(sql, (code, 'y', yyyymm, revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating))

                    self.conn.commit()
                else:
                    print('UPDATE', revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating,
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
                    revenue, gross_profit, operating_income, net_income, asset, liability, equity, cashflow_operating,
                    code, yyyymm, 'y'))
                    self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
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
                # rs = curs.fetchall()
                rs = curs.fetchone()

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
                    curs.execute(sql, (per, pcr, psr, pbr, total_cashflow, code, yyyymm))
                    self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass

    # def updateOrder(self, yyyymm, setField, orderItem):
    #
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'update financeinfos target ' \
    #                   'join ' \
    #                   '(' \
    #                   'select id, (@rownumber := @rownumber + 1) as rownum ' \
    #                   'from financeinfos ' \
    #                   'cross join (select @rownumber := 0) r ' \
    #                   ' where yyyymm = %s and {} is not null ' \
    #                   'order by {} asc ' \
    #                   ') source on target.id = source.id ' \
    #                   'set {} = rownum'
    #
    #             curs.execute(sql.format(orderItem, orderItem, setField), (yyyymm))
    #             self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    # def updateScore(self, yyyymm):
    #     """
    #     설정 조건 충족시 1점, 미충족시 0점
    #     당기순이익이 0이상인가?
    #     영업현금흐름이 0이상인가?
    #     ROA가 전년 대비 증가했는가?
    #     영업현금흐름이 순이익보다 높은가?
    #     부채비율이 전년 대비 감소했는가?
    #     유동비율이 전년 대비 증가했는가?
    #     당해 신규주식 발행을 하지 않았는가?
    #     매출총이익이 전년 대비 증가했는가?
    #     자산회전율이 전년 대비 증가했는가?
    #     """
    #     try:
    #         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
    #
    #             sql = 'UPDATE  financeinfos ' \
    #                   'SET     score_net_income = IF(net_income > 0, 1, 0), ' \
    #                   '        score_cashflow_operating = IF(cashflow_operating  > 0, 1, 0), ' \
    #                   '        score_diff = IF(cashflow_operating >  net_income, 1, 0), ' \
    #                   '        score_total = score_net_income +  score_cashflow_operating + score_diff ' \
    #                   'WHERE   yyyymm = %s'
    #
    #             curs.execute(sql, (yyyymm))
    #             self.conn.commit()
    #     except Exception as e:
    #         print(e)
    #         print(curs._last_executed)
    #         raise
    #     finally:
    #         pass

    def deleteConsensusEstimate(self, code):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'delete from concensus_estimate where code=%s'
                curs.execute(sql, code)
                self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateConsensusEstimate(self, code, row):
        inst_cd = row['INST_CD']
        inst_nm = row['INST_NM']
        est_dt = row['EST_DT'].replace('/', '-')
        target_prc = row['TARGET_PRC'].replace(',', '')
        target_prc_bf = row['TARGET_PRC_BF'].replace(',', '')
        yoy = row['YOY']
        recom_cd = row['RECOM_CD']
        recom_cd_bf = row['RECOM_CD_BF']
        avg_prc = row['AVG_PRC'].replace(',', '')
        avg_prc_bf = row['AVG_PRC_BF'].replace(',', '')
        avg_recom_cd = row['AVG_RECOM_CD']
        avg_recom_cd_bf = row['AVG_RECOM_CD_BF']

        print(code, inst_cd, inst_nm, est_dt, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg_prc,
              avg_prc_bf, avg_recom_cd, avg_recom_cd_bf)
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'insert into concensus_estimate ' \
                      '(code, inst_cd, inst_nm, est_dt, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg_prc, avg_prc_bf, avg_recom_cd, avg_recom_cd_bf) ' \
                      'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                curs.execute(sql, (
                code, inst_cd, inst_nm, est_dt, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg_prc,
                avg_prc_bf, avg_recom_cd, avg_recom_cd_bf))
                self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
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

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
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

                    self.conn.commit()
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
                    self.conn.commit()
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

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
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
                    curs.execute(sql, (code, flag, yyyymm, current_ratio, debt_ratio, operating_profit_margin, roa, roic))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos_fnguide set ' \
                          'current_ratio=%s, ' \
                          'debt_ratio=%s, ' \
                          'operating_profit_margin=%s, ' \
                          'roa=%s, ' \
                          'roic=%s ' \
                          'where code=%s and yyyymm=%s and flag=%s'
                    curs.execute(sql, (current_ratio, debt_ratio, operating_profit_margin, roa, roic, code, yyyymm, flag))
                    self.conn.commit()
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
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select controlling_shareholder from financeinfos_fnguide WHERE code = %s AND yyyymm = %s"
                curs.execute(sql, (code, yyyymm))

                rs = curs.fetchone()
                return rs
        finally:
            pass

    def get3yearRoe(self, code, yyyymm):
        """
        3년간 roe가져오기
        :return:
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select roe, yyyymm controlling_shareholder from financeinfos_fnguide WHERE code = %s AND flag = %s and yyyymm <= %s order by yyyymm asc limit 0, 3"
                curs.execute(sql, (code, 'y', yyyymm))

                rs = curs.fetchall()
                return rs
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateSrim(self, id, price):
        print('updateSrim', id, price)
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'update corporations set '\
                      's_rim=%s '\
                      'where id=%s'
                curs.execute(sql, (price, id))
                self.conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def financeinfoNaver(self, code, idx, column):
        """
        네이버 금융정보 업데이트
        :param code: 
        :param idx: 
        :param column: 
        :return: 
        """
        print('code:' + code)
        revenue = column['매출액'] if self.isNaN(column['매출액']) == False else None
        operating_income = column['영업이익'] if self.isNaN(column['영업이익']) == False else None
        net_income = column['당기순이익'] if self.isNaN(column['당기순이익']) == False else None
        operating_profit_margin = column['영업이익률'] if self.isNaN(column['영업이익률']) == False else None
        net_profit_margin = column['순이익률'] if self.isNaN(column['순이익률']) == False else None
        roe = column['ROE(지배주주)'] if self.isNaN(column['ROE(지배주주)']) == False else None
        debt_ratio = column['부채비율'] if self.isNaN(column['부채비율']) == False else None
        quick_ratio = column['당좌비율'] if column['당좌비율'] == False else None
        reserve_ratio = column['유보율'] if column['유보율'] == False else None
        eps = column['EPS(원)'] if self.isNaN(column['EPS(원)']) == False else None
        per = column['PER(배)'] if self.isNaN(column['PER(배)']) == False else None
        bps = column['BPS(원)'] if self.isNaN(column['BPS(원)']) == False else None
        pbr = column['PBR(배)'] if self.isNaN(column['PBR(배)']) == False else None

        # print('debt_ratio', debt_ratio, self.isNaN(column['부채비율']))

        if idx[0] == '최근 연간 실적':
            flag = 'y'
        else:
            flag = 'q'

        if len(idx[1]) > 10:
            print(idx[1] + '======================================')
            return

        yyyymm = idx[1].replace('.', '')
        yyyymm = yyyymm.replace('(E)', '')
        print(yyyymm)

        # eps = column['주당순이익'] if data['주당순이익'] != '--' else None
        # eps_forcast = data['column'] if data['예측'] != '--' else None
        # revenue = data['column'] if data['매출'] != '--' else None
        # revenue_forcast = data['예측.1'] if data['예측.1'] != '--' else None
        # print(release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from financeinfos_naver where code=%s and flag=%s and yyyymm=%s limit 0, 1"
                curs.execute(sql, (code, flag, yyyymm))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    print(code, flag, yyyymm, revenue, operating_income, net_income, operating_profit_margin,
                          net_profit_margin, debt_ratio, quick_ratio, reserve_ratio, roe, eps, per, bps, pbr)
                    sql = 'insert into financeinfos_naver ' \
                          '(code, flag, yyyymm, revenue, operating_income, net_income, operating_profit_margin, ' \
                          'net_profit_margin, debt_ratio, quick_ratio, reserve_ratio, roe, eps, per, bps, pbr) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql,
                                 (code, flag, yyyymm, revenue, operating_income, net_income, operating_profit_margin,
                                  net_profit_margin, debt_ratio, quick_ratio, reserve_ratio, roe, eps, per, bps, pbr))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update financeinfos_naver set ' \
                          'revenue=%s, ' \
                          'operating_income=%s, ' \
                          'net_income=%s, ' \
                          'operating_profit_margin=%s, ' \
                          'net_profit_margin=%s, ' \
                          'debt_ratio=%s, ' \
                          'quick_ratio=%s, ' \
                          'reserve_ratio=%s, ' \
                          'roe=%s, ' \
                          'eps=%s, ' \
                          'per=%s, ' \
                          'bps=%s, ' \
                          'pbr=%s ' \
                          'where id=%s'
                    curs.execute(sql, (revenue, operating_income, net_income, operating_profit_margin,
                                       net_profit_margin, debt_ratio, quick_ratio, reserve_ratio, roe, eps, per, bps,
                                       pbr, rs['id']))
                    self.conn.commit()
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    # Investing 관련
    def earnings(self, code, data):
        release_dt = data['발표일']
        period_end_dt = data['기말']
        eps = data['주당순이익'] if data['주당순이익'] != '--' else None
        eps_forcast = data['예측'] if data['예측'] != '--' else None
        revenue = data['매출'] if data['매출'] != '--' else None
        revenue_forcast = data['예측.1'] if data['예측.1'] != '--' else None
        print(release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from earnings where code=%s and period_end_dt=%s limit 0, 1"
                curs.execute(sql, (code, period_end_dt))
                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into earnings ' \
                          '(code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (code, release_dt, period_end_dt, eps, eps_forcast, revenue, revenue_forcast))

                    self.conn.commit()
                else:
                    print('UPDATE')
                    sql = 'update earnings set ' \
                          'release_dt=%s, ' \
                          'eps=%s, ' \
                          'eps_forcast=%s, ' \
                          'revenue=%s, ' \
                          'revenue_forcast=%s ' \
                          'where id=%s'
                    curs.execute(sql, (release_dt, eps, eps_forcast, revenue, revenue_forcast, rs['id']))
                    self.conn.commit()
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateInvestingCompname(self, id, eng):

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                    sql='UPDATE  corporations ' \
                            'SET     investing_comp_name = %s ' \
                            'WHERE   id = %s'

                    curs.execute(sql, (eng, id))
                    self.conn.commit()
        except:
            print(curs._last_executed)
            raise
        finally:
            pass

    def updateMarketPrices(self, code, yyyymm, close, open, high, low, trade_qty):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from market_prices where code=%s and yyyymmdd=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into market_prices ' \
                          '(code, yyyymmdd, close, open, high, low, trade_qty) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                        code, yyyymm, close, open, high, low, trade_qty
                    ))

                    self.conn.commit()
                else:
                    sql = 'update market_prices set ' \
                          'close=%s, ' \
                          'open=%s, ' \
                          'high=%s, ' \
                          'low=%s, ' \
                          'trade_qty=%s ' \
                          'where id=%s'
                    curs.execute(sql, (
                        close, open, high, low, trade_qty, rs['id']
                    ))
                    self.conn.commit()

                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass


            
    def isNaN(self, string):
        return string != string

    def close(self):
        self.conn.close()