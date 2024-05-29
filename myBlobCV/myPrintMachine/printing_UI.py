from flask import Flask, render_template, request
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks


class WebApp:
    def __init__(self):
        self.app = Flask(__name__, static_folder='templates')
        self.input_str = None

        @self.app.route('/')
        def index():
            name = "Your Name"
            introduction = "Welcome to my personal website!"
            contact_info = "Contact me at: your_email@example.com"
            return render_template('index.html', name=name, introduction=introduction,
                                   contact_info=contact_info)

        @self.app.route('/submit', methods=['POST'])
        def submit():
            user_input = request.form['user_input']
            # print("User input:", user_input)

            master.execute(slave=1, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=9,
                           output_value=2, data_format='>H')
            self.input_str = user_input
            return user_input

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    web_app = WebApp()

    master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502, timeout_in_sec=5.0)

    web_app.run()
