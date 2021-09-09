import pymysql

# DB 테이블 칼럼대로 만든 객체
class Concensus:
    def __init__(self, parent):
        self.parent = parent
        # self.conn = parent.conn


    def deleteConsensusEstimate(self, code):
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'delete from concensus_estimate where code=%s'
                curs.execute(sql, code)
                conn.commit()
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

        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'insert into concensus_estimate ' \
                      '(code, inst_cd, inst_nm, est_dt, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg_prc, avg_prc_bf, avg_recom_cd, avg_recom_cd_bf) ' \
                      'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                curs.execute(sql, (
                    code, inst_cd, inst_nm, est_dt, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg_prc,
                    avg_prc_bf, avg_recom_cd, avg_recom_cd_bf))
                conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass