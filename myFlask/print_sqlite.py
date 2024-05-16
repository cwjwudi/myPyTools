import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('user_input.db')
cur = conn.cursor()

# 执行 SQL 查询获取数据库中的数据
cur.execute("SELECT * FROM inputs")
rows = cur.fetchall()

# 打印查询结果
for row in rows:
    print(row)

# 关闭数据库连接
conn.close()
