import pymysql

# DB 테이블 칼럼대로 만든 객체
class Shorting:
    def __init__(self, parent):
        self.parent = parent

    def update(self, code, ymd, s_vol, s_amt, r_vol, s_remain_vol, s_remain_amt, ratio):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from shorting_info where code=%s and ymd=%s limit 0, 1"
                curs.execute(sql, (code, ymd))
                rs = curs.fetchone()
                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into shorting_info ' \
                          '(code, ymd, s_vol, s_amt, r_vol, s_remain_vol, s_remain_amt, ratio) ' \
                          'values(%s, %s, %s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                        code, ymd, s_vol, s_amt, r_vol, s_remain_vol, s_remain_amt, ratio
                    ))

                    conn.commit()
                else:
                    sql = 'update shorting_info set ' \
                          's_vol=%s, ' \
                          's_amt=%s, ' \
                          'r_vol=%s, ' \
                          's_remain_vol=%s, ' \
                          's_remain_amt=%s, '\
                          'ratio=%s ' \
                          'where id=%s'
                    curs.execute(sql, (
                        s_vol, s_amt, r_vol, s_remain_vol, s_remain_amt, ratio, rs['id']
                    ))
                    conn.commit()
        except:
            print(curs._last_executed)
            raise
            # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass

    # def updateShortingStatus(self, code, ymd, volume, v_remain, tr_amount, remain_amount):
    #     conn = self.parent.connect()
    #     try:
    #         with conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select id from shorting_info where code=%s and ymd=%s limit 0, 1"
    #             curs.execute(sql, (code, ymd))
    #             rs = curs.fetchone()
    #             if rs == None:  # 값이 없을 경우 현재 값 입력
    #                 print('None')
    #                 sql = 'insert into shorting_info ' \
    #                       '(code, ymd, volume, v_remain, tr_amount, remain_amount) ' \
    #                       'values(%s, %s, %s, %s, %s, %s)'
    #                 curs.execute(sql, (
    #                     code, ymd, volume, v_remain, tr_amount, remain_amount
    #                 ))
    #
    #                 conn.commit()
    #             else:
    #                 sql = 'update shorting_info set ' \
    #                       'volume=%s, ' \
    #                       'v_remain=%s, ' \
    #                       'tr_amount=%s, ' \
    #                       'remain_amount=%s ' \
    #                       'where id=%s'
    #                 curs.execute(sql, (
    #                     volume, v_remain, tr_amount, remain_amount, rs['id']
    #                 ))
    #                 conn.commit()
    #     except:
    #         print(curs._last_executed)
    #         raise
    #                 # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
    #     finally:
    #         pass
    #
    # def updateShortingVolume(self, code, ymd, volume, v_buy, ratio):
    #     print(code, ymd, volume, v_buy, ratio)
    #     conn = self.parent.connect()
    #     try:
    #         with conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select id from shorting_info where code=%s and ymd=%s limit 0, 1"
    #             curs.execute(sql, (code, ymd))
    #             # columns = curs.description
    #             # print(columns)
    #
    #             # rs = curs.fetchall()
    #             rs = curs.fetchone()
    #             print(rs)
    #
    #             if rs == None:  # 값이 없을 경우 현재 값 입력
    #                 print('None')
    #                 sql = 'insert into shorting_info ' \
    #                       '(code, ymd, volume, v_buy, ratio) ' \
    #                       'values(%s, %s, %s, %s, %s)'
    #                 curs.execute(sql, (
    #                     code, ymd, volume, v_buy, ratio
    #                 ))
    #
    #                 conn.commit()
    #             else:
    #                 sql = 'update shorting_info set ' \
    #                       'volume=%s, ' \
    #                       'v_buy=%s, ' \
    #                       'ratio=%s ' \
    #                       'where id=%s'
    #                 curs.execute(sql, (
    #                     volume, v_buy, ratio, rs['id']
    #                 ))
    #                 conn.commit()
    #     except:
    #         print(curs._last_executed)
    #         raise
    #         # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
    #     finally:
    #         pass