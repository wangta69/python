import os
import time
import numpy as np

import pymysql
from dotenv import load_dotenv
# from .querie.corporations import Corporatons
# from .querie.market_prices import MarketPrices
# from .querie.financeinfos_fnguide import Fnguide
# from .querie.financeinfos_naver import Naver
# from .querie.concensus_estimate import Concensus
# from .querie.earings import Earnings
# from .querie.trading_volume_sector import VolumeSector
# # import numpy as np
# # from stock_crawler.utils import *

# DB 테이블 칼럼대로 만든 객체
class Mysql:
    def __init__(self):
        load_dotenv()
        # host = os.getenv('DB_HOST')
        # user = os.getenv('DB_USER')
        # password = os.getenv('DB_PASSWORD')
        # db = os.getenv('DB_DATABASE')
        #
        # self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        # self.conn = self.connect()


    def connect(self):
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db = os.getenv('DB_DATABASE')
        port = int(os.getenv('DB_PORT'))

        return pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset='utf8')

    def close(self):
        self.conn.close()

    def celebrity1(self, name, job, birth_ym):
        conn = self.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:

                print('None')
                sql = 'insert into celebrity ' \
                      '(name, job, birth_ym, created_at) ' \
                      'values(%s, %s, %s, %s)'
                curs.execute(sql, (
                    name, job, birth_ym,
                    time.strftime('%Y-%m-%d %H:%M:%S')))

                conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass

    def celebrity2(self, name, gender, yyyymm, sl, flat_leap, ganji, memo):
        memo = self.ItemCheck(memo)
        conn = self.connect()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:

                print('None')
                sql = 'insert into celebrity ' \
                      '(name, gender, birth_ym, sl, flat_leap, ganji, memo, created_at) ' \
                      'values(%s, %s, %s, %s, %s, %s, %s, %s)'
                curs.execute(sql, (
                    name, gender, yyyymm, sl, flat_leap, ganji, memo,
                    time.strftime('%Y-%m-%d %H:%M:%S')))

                conn.commit()
        except Exception as e:
            print(e)
            print(curs._last_executed)
            raise
        finally:
            pass


    def ItemCheck(self, source):

        try:
            source = source if ~np.isnan(source) else None
        except KeyError as e:
            print('[keyCheck] I got a KeyError - reason "%s"' % str(e))
            source = None
        except ValueError as e:
            print('[keyCheck] I got a ValueError - reason "%s"' % str(e))
        except IndexError as e:
            print('[keyCheck] I got a IndexError  - reason "%s"' % str(e))
        except Exception as e:
            print('[keyCheck] I got a Exception  - reason "%s"' % str(e))

        return source

    def keyCheck(source, keys):
        for k in keys:
            try:
                source[k] = source[k] if ~np.isnan(source[k]) else None
            except KeyError as e:
                print('[keyCheck] I got a KeyError - reason "%s"' % str(e))
                source[k] = None
            except ValueError as e:
                print('[keyCheck] I got a ValueError - reason "%s"' % str(e))
            except IndexError as e:
                print('[keyCheck] I got a IndexError  - reason "%s"' % str(e))
            except Exception as e:
                print('source', source, 'keys', keys)
                print('[keyCheck] I got a Exception  - reason "%s"' % str(e))
        return source



