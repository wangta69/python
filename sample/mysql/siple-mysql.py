import pymysql

#DB 테이블 칼럼대로 만든 객체
class Test:
    def __init__(self, num, name):
        self.num = num
        self.name = name

#전체 Select
def select_all():
    conn = pymysql.connect(host='localhost', user='mytest', password='akfldkDB', db='mytest', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "select * from test"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)
    finally:
        conn.close()

#DB Insert
def insert_test(test_obj):
    conn = pymysql.connect(host='localhost', user='mytest', password='akfldkDB', db='mytest', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'insert into test values(%s, %s)'
            curs.execute(sql, (test_obj.num, test_obj.name))
        conn.commit()
    finally:
        conn.close()

#num칼럼으로 DB Delete
def delete_test(num):
    conn = pymysql.connect(host='localhost', user='mytest', password='akfldkDB', db='mytest', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'delete from test where num=%s'
            curs.execute(sql, num)
        conn.commit()
    finally:
        conn.close()

#DB Delete All
def delete_all():
    conn = pymysql.connect(host='localhost', user='mytest', password='akfldkDB', db='mytest', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'delete from test'
            curs.execute(sql)
        conn.commit()
    finally:
        conn.close()

#DB Update
def update_test(test_obj):
    conn = pymysql.connect(host='localhost', user='mytest', password='akfldkDB', db='mytest', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'update test set name=%s where num=%s'
            curs.execute(sql, (test_obj.name, test_obj.num))
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":

    test = Test(3, '어제는')
    insert_test(test)

    # delete_all()
    # insert_excel_to_db()
    # select_all()
    pass
