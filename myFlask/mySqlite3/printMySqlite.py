import sqlite3

# 连接到数据库
conn = sqlite3.connect('customer_database.db')

# 创建一个游标对象
cursor = conn.cursor()

# 查询数据库中的所有客户数据
cursor.execute('SELECT * FROM customers')

# 检索所有数据行
rows = cursor.fetchall()

# 打印每一行数据
for row in rows:
    print("姓名:", row[1])
    print("公司名称:", row[2])
    print("手机号码:", row[3])
    print("电子邮箱:", row[4])
    print()

# 关闭连接
conn.close()
