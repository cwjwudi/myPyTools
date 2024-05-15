from flask import Flask, render_template, request

app = Flask(__name__)

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
    print("User input:", user_input)
    return "Your input has been submitted: " + user_input

if __name__ == '__main__':
    app.run(debug=True)
