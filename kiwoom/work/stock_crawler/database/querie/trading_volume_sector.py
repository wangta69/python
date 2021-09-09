import pymysql

# DB 테이블 칼럼대로 만든 객체
class VolumeSector:
    def __init__(self, parent):
        self.parent = parent

    def updateVolumeSector(self, code, yyyymm, corp, corp_etc, private, foreigner):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id from trading_volume_sector where code=%s and yyyymmdd=%s limit 0, 1"
                curs.execute(sql, (code, yyyymm))
                # columns = curs.description
                # print(columns)

                # rs = curs.fetchall()
                rs = curs.fetchone()
                print(rs)

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    print('None')
                    sql = 'insert into trading_volume_sector ' \
                          '(code, yyyymmdd, corp, corp_etc, private, foreigner) ' \
                          'values(%s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (
                        code, yyyymm, corp, corp_etc, private, foreigner
                    ))

                    conn.commit()
                else:
                    sql = 'update trading_volume_sector set ' \
                          'corp=%s, ' \
                          'corp_etc=%s, ' \
                          'private=%s, ' \
                          'foreigner=%s ' \
                          'where id=%s'
                    curs.execute(sql, (
                        corp, corp_etc, private, foreigner, rs['id']
                    ))
                    conn.commit()
        except:
            print(curs._last_executed)
            raise
                    # 존재할 경우 현재 값과 비교하여 동일하면 skip 하고 다를 경우 업데이트 한다.
        finally:
            pass