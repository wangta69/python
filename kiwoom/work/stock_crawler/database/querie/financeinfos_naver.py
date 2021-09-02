import pymysql

# DB 테이블 칼럼대로 만든 객체
class Naver:
    def __init__(self, parent=None):
        self.conn = parent.conn

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