from flask import Flask, render_template, request
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
import mmap


class WebApp:
    def __init__(self):
        self.app = Flask(__name__, static_folder='templates')
        self.input_str = None

        @self.app.route('/')
        def index():
            name = "Printing Machine UI"
            introduction = "This is a test of control UI for printing machine."
            contact_info = "Contact me at: Wenjie.Cui@br-automation.com"
            return render_template('index.html', name=name, introduction=introduction,
                                   contact_info=contact_info)

        @self.app.route('/submit', methods=['POST'])
        def submit():
            user_input = request.form['user_input']
            cmd_return_text = ""

            try:
                result = master.execute(slave=1, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=8,
                                        output_value=2)

                cmd_return_text = "Write operation successful. Returned result: {}\n".format(result)
            except Exception as e:
                cmd_return_text = "Error: {}\n".format(e)

            input_text = "Your cmd " + user_input + " has been processed! \n"

            return input_text + cmd_return_text

        @self.app.route('/view_img', methods=['GET'])
        def view_customers():
            with open("image_base64.txt", "r") as f:
                image_base64 = f.read()
            # from base64Pic import pic
            # image_base64 = pic
            with open("shared_memory.bin", "r+b") as f:
                mm = mmap.mmap(f.fileno(), 0)

            return render_template('view_img.html', image_base64=mm)


    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    web_app = WebApp()

    master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502, timeout_in_sec=5.0)

    web_app.run()
