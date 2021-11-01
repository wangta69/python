import pymysql
import time
from stock_crawler.utils import *

# DB 테이블 칼럼대로 만든 객체
class Sectors:
    def __init__(self, parent):
        self.parent = parent
    #
    # def sectors(self):
    #     """
    #     섹터 가져오기
    #     :return:
    #     """
    #     conn = self.parent.connect()
    #     try:
    #         with conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select id, code, code_krx, investing_comp_name, common_stocks from sectors where status = 0"
    #             curs.execute(sql)
    #
    #             rs = curs.fetchall()
    #             return rs
    #     except Exception as e:
    #         print('I got a Exception  - reason "%s"' % str(e))
    #         print(curs._last_executed)
    #         raise
    #     # finally:
    #     #     return rs
    #
    # def sectors(self, code):
    #     """
    #     기업정보 가져오기
    #     :return:
    #     """
    #     conn = self.parent.connect()
    #     try:
    #         with conn.cursor(pymysql.cursors.DictCursor) as curs:
    #             sql = "select id, code, code_krx, common_stocks, investing_comp_name from sectors where code=%s"
    #             curs.execute(sql, (code))
    #
    #             rs = curs.fetchone()
    #             return rs
    #     except Exception as e:
    #         print('I got a Exception  - reason "%s"' % str(e))
    #         print(curs._last_executed)
    #         raise
    #     # finally:
    #     #     pass

    def getSectorId(self, name):
        """
        섹터 아이디가 있으면 섹터 아이디를 리턴하고 없으면 입력후 섹터 아이디를 리턴한다.
        :param name:
        :return:
        """
        conn = self.parent.connect()
        sectorId = 0
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, name from sectors where name=%s limit 0, 1"
                curs.execute(sql, (name))

                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    sql = 'insert into sectors ' \
                          '(name) ' \
                          'values(%s)'
                    curs.execute(sql, (name))
                    conn.commit()
                    sectorId = curs.lastrowid
                else:
                    sectorId = rs['id']
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            return sectorId
            pass

    def MappingSector(self, code, sector_id):
        """
        섹터 아이디가 있으면 섹터 아이디를 리턴하고 없으면 입력후 섹터 아이디를 리턴한다.
        :param name:
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from corporations_sectors where code=%s and sector_id=%s limit 0, 1"
                curs.execute(sql, (code, sector_id))

                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    sql = 'insert into corporations_sectors ' \
                          '(code, sector_id) ' \
                          'values(%s, %s)'
                    curs.execute(sql, (code, sector_id))
                    conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def getThemeId(self, name):
        """
        섹터 아이디가 있으면 섹터 아이디를 리턴하고 없으면 입력후 섹터 아이디를 리턴한다.
        :param name:
        :return:
        """
        conn = self.parent.connect()
        sectorId = 0
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select id, name from themes where name=%s limit 0, 1"
                curs.execute(sql, (name))

                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    sql = 'insert into themes ' \
                          '(name) ' \
                          'values(%s)'
                    curs.execute(sql, (name))
                    conn.commit()
                    sectorId = curs.lastrowid
                else:
                    sectorId = rs['id']
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            return sectorId
            pass


    def MappingTheme(self, code, sector_id):
        """
        섹터 아이디가 있으면 섹터 아이디를 리턴하고 없으면 입력후 섹터 아이디를 리턴한다.
        :param name:
        :return:
        """
        conn = self.parent.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = "select code from corporations_themes where code=%s and sector_id=%s limit 0, 1"
                curs.execute(sql, (code, sector_id))

                rs = curs.fetchone()

                if rs == None:  # 값이 없을 경우 현재 값 입력
                    sql = 'insert into corporations_themes ' \
                          '(code, sector_id) ' \
                          'values(%s, %s)'
                    curs.execute(sql, (code, sector_id))
                    conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass