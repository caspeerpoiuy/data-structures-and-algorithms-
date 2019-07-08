from pymysql import *

connection = connect(host="localhost", port=3306, user="root", password="casper", database="class")

cursors = connection.cursor()

sql = "select class_name from class"

cursors.execute(sql)

data = cursors.fetchone()
# fetchall, fetchmany
cursors.close()

connection.close()

"""
pymysql的查询数据操作：
    1：创建连接
    2：创建cursor
    3：执行sql语句
    4：取查询结果
    5：关闭cursor
    6：关闭连接
"""