from flask import Flask, render_template, request, redirect, url_for
try:
    from myFlask.mySqlite3.createMySqlite3 import Database
except:
    from mySqlite3.createMySqlite3 import Database

app = Flask(__name__, static_folder='templates')

# 创建数据库对象
db = Database('./mySqlite3/customer_database.db')
# 在应用上下文中创建表
with app.app_context():
    db.create_table()
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        phone = request.form['phone']
        email = request.form['email']

        # 将客户信息保存到数据库中
        db.add_customer(name, company, phone, email)

        return redirect(url_for('index'))
    else:
        return render_template('add_customer.html')


@app.route('/view_customers', methods=['GET'])
def view_customers():
    customers = db.get_all_customers()
    return render_template('view_customers.html', customers=customers)


if __name__ == '__main__':
    app.run(debug=True)
