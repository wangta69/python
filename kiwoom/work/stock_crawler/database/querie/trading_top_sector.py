import pymysql

# DB 테이블 칼럼대로 만든 객체
class TopVolumeSector:
    def __init__(self, parent):
        self.parent = parent

    def update(self, code, ymd, sb, corp, qty):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from trading_top_sector where code=%s and ymd=%s and sb=%s and corp=%s limit 0, 1"
                curs.execute(sql, (code, ymd, sb, corp))

                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into trading_top_sector ' \
                          '(code, ymd, sb, corp, qty) ' \
                          'values(%s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                        code, ymd, sb, corp, qty
                    ))

                    conn.commit()
                else:
                    sql = 'update trading_top_sector set ' \
                          'qty=%s ' \
                          'where id=%s'
                    curs.execute(sql, (
                        qty, rs['id']
                    ))
                    conn.commit()
        except:
            print(curs._last_executed)
            raise
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass