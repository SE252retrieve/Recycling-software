import sqlite3


# 建物品数据库
def create_sql():
    sql = sqlite3.connect("goods.db")
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar,
        %s float,
        %s int)"""
                % ('goods',
                   'id',
                   'goodsname',
                   'price',
                   'quantity',
                   ))
    sql.close()


create_sql()

