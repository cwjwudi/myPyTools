from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 连接到 SQLite 数据库
conn = sqlite3.connect('user_input.db', check_same_thread=False)
cur = conn.cursor()

# 创建表
cur.execute('''
    CREATE TABLE IF NOT EXISTS inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/')
def index():
    # 个人信息
    name = "Your Name"
    introduction = "Welcome to my personal website!"
    contact_info = "Contact me at: your_email@example.com"

    return render_template('index.html', name=name, introduction=introduction, contact_info=contact_info)

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    # 将用户输入的数据保存到数据库中
    cur.execute("INSERT INTO inputs (user_input) VALUES (?)", (user_input,))
    conn.commit()
    return "Your input has been submitted and saved to the database: " + user_input

if __name__ == '__main__':
    app.run(debug=True)
