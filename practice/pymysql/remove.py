from pymysql import *

connection = connect(host="localhost", port=3306, user="root", password="casper", database="class")

cursors = connection.cursor()

sql = "delete from class where class_id=2;"

cursors.execute(sql)

connection.commit()

cursors.close()

connection.close()

"""
pymysql的删除数据操作：
    1：创建连接
    2：创建cursor
    3：执行sql语句
    4：connection commit
    5：关闭cursor
    6：关闭连接
"""

