import sqlite3


# 用户注册
def add_data():
    input_name = input("请输入用户名：")
    input_passworld = input("请输入密码：")
    input_againpassworld = input("请再次输入密码：")
    input_phone = input('请输入手机号：')
    input_email = input('请输入邮箱：')
    sql = sqlite3.connect("user.db")
    sql.execute("insert into user(username,passworld,againpassworld,phone,email) values(?,?,?,?,?)",
                (input_name, input_passworld, input_againpassworld, input_phone, input_email))
    sql.commit()
    print("添加成功")
    sql.close()





