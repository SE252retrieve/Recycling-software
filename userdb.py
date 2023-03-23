import sqlite3


# 建用户数据库
def create_sql():
    sql = sqlite3.connect("user.db")
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar,
        %s varchar,
        %s varchar,
        %s varchar,
        %s float,
        %s varchar)"""
                % ('user',
                   'id',
                   'username',
                   'passworld',
                   'againpassworld',
                   'phone',
                   'balance',
                   'email'
                   ))
    sql.close()


create_sql()
