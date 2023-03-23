import sqlite3
# 用户查询
def showalldata():
    sql = sqlite3.connect("user.db")
    data = sql.execute("select * from user").fetchall()
    sql.close()
    return data



# 用户删除
def drop():
    print('指定id删除')
    sql = sqlite3.connect("user.db")
    data = sql.execute("select * from user").fetchall()
    print('所有数据:' + str(data))
    while 1:
        id = input('请输入你要删除的数据的id:')
        sql.execute("DELETE FROM user WHERE id = %s" % id)
        sql.commit()
        print('删除完成')
        data = sql.execute("select * from user")
        print(data.fetchall())
        sql.close()
        break
