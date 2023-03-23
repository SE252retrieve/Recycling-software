import sqlite3
import os

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute("INSERT INTO user (name, points) VALUES ('user1', 100)")
cursor.execute("INSERT INTO user (name, points) VALUES ('user2', 200)")
cursor.execute("INSERT INTO user (name, points) VALUES ('user3', 300)")

cursor.execute("INSERT INTO goods (name, points) VALUES ('goods1', 10)")
cursor.execute("INSERT INTO goods (name, points) VALUES ('goods2', 20)")
cursor.execute("INSERT INTO goods (name, points) VALUES ('goods3', 30)")

cursor.execute("INSERT INTO recycle_goods (name, points) VALUES ('recycle_goods1', 10)")
cursor.execute("INSERT INTO recycle_goods (name, points) VALUES ('recycle_goods2', 20)")
cursor.execute("INSERT INTO recycle_goods (name, points) VALUES ('recycle_goods3', 30)")

def login():
    username = input("请输入用户名：")
    cursor.execute(f"SELECT name FROM user WHERE name='{username}'")
    result = cursor.fetchone()
    if result:
        return username
    else:
        print(f"{username}不存在")
        return None

def query_points(username):
    if not username:
        username = login()
    cursor.execute(f"SELECT points FROM user WHERE name='{username}'")
    result = cursor.fetchone()
    if result:
        print(f"{username}的积分为{result[0]}")
    else:
        print(f"{username}不存在")

def show_goods():
    cursor.execute("SELECT name, points FROM goods")
    result = cursor.fetchall()
    for row in result:
        print(f"{row[0]} - {row[1]}积分")

def add_to_cart(username):
    goods_name = input("请输入商品名称：")
    cursor.execute(f"SELECT points FROM goods WHERE name='{goods_name}'")
    result = cursor.fetchone()
    if result:
        points = result[0]
        cursor.execute(f"SELECT * FROM bought_goods WHERE user='{username}' AND goods='{goods_name}'")
        result = cursor.fetchone()
        if result:
            print(f"{goods_name}已购买，不允许重复购买")
        else:
            cursor.execute(f"INSERT INTO cart (user, goods, points) VALUES ('{username}', '{goods_name}', {points})")
            print(f"{goods_name}已添加到购物车")
    else:
        print(f"{goods_name}不存在")

def show_cart(username):
    cursor.execute(f"SELECT goods, points FROM cart WHERE user='{username}'")
    result = cursor.fetchall()
    total_points = 0
    for row in result:
        print(f"{row[0]} - {row[1]}积分")
        total_points += row[1]
    print(f"总积分：{total_points}")

def buy_goods(username):
    cursor.execute(f"SELECT goods, points FROM cart WHERE user='{username}'")
    result = cursor.fetchall()
    total_points = 0
    for row in result:
        total_points += row[1]
    cursor.execute(f"SELECT goods, points FROM cart WHERE user='{username}'")
    result = cursor.fetchall()
    if result:
        for row in result:
            cursor.execute(f"INSERT INTO bought_goods (user, goods, points) VALUES ('{username}', '{row[0]}', {row[1]})")
        cursor.execute(f"DELETE FROM cart WHERE user='{username}'")
        cursor.execute(f"UPDATE user SET points=points-{total_points} WHERE name='{username}'")
        print(f"购买成功，总积分：{total_points}")
    else:
        print(f"购物车为空")

def show_bought_goods(username):
    cursor.execute(f"SELECT goods, points FROM bought_goods WHERE user='{username}'")
    result = cursor.fetchall()
    for row in result:
        print(f"{row[0]} - {row[1]}积分")

def recycle_goods(username):
    goods_name = input("请输入回收物名称：")
    cursor.execute(f"SELECT points FROM recycle_goods WHERE name='{goods_name}'")
    result = cursor.fetchone()
    if result:
        points = result[0]
        cursor.execute(f"DELETE FROM bought_goods WHERE user='{username}' AND goods='{goods_name}'")
        cursor.execute(f"UPDATE user SET points=points+{points} WHERE name='{username}'")
        print(f"回收成功，获得{points}积分")
    else:
        print(f"{goods_name}不可回收")

def show_users():
    cursor.execute("SELECT name, points FROM user")
    result = cursor.fetchall()
    for row in result:
        print(f"{row[0]} - {row[1]}积分")

def main():
    username = None
    while True:
        if not username:
            print("1. 登陆")
        else:
            print("1. 退出登陆")
            print("2. 查询积分")
            print("3. 查看商品列表")
            print("4. 添加购物车")
            print("5. 查看已购买商品")
            print("6. 回收物品")
            print("7. 结算购物车")
            print("8. 查看用户列表")
            print("Q. 退出系统")
        choice = input("请输入操作编号：")
        if choice == '1':
            if not username:
                username = login()
            else:
                username = None
        elif choice == '2':
            if username:
                query_points(username)
            else:
                print("请先登陆")
        elif choice == '3':
            if username:
                show_goods()
            else:
                print("请先登陆")
        elif choice == '4':
            if username:
                add_to_cart(username)
            else:
                print("请先登陆")
        elif choice == '5':
            if username:
                show_bought_goods(username)
            else:
                print("请先登陆")
        elif choice == '6':
            if username:
                recycle_goods(username)
            else:
                print("请先登陆")
        elif choice == '7':
            if username:
                buy_goods(username)
            else:
                print("请先登陆")
        elif choice == '8':
            if username:
                show_users()
            else:
                print("请先登陆")
        elif choice == 'Q' or choice == 'q':
            break
        else:
            print("无效操作")

if __name__ == '__main__':
    main()

    conn.close()
