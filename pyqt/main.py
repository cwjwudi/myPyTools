import time
from threading import Thread

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QTableWidget
# PySide6-uic demo.ui -o ui_demo.py  # 生成UI
# from ui_demo import Ui_Demo
from task import add, analyStatus
from myui import Ui_MainWindow

from Signal import my_signal


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.band()

        self.directory = ''

    def band(self):
        # 常用信号与槽的绑定
        # self.ui.___ACTION___.triggered.connect(___FUNCTION___)
        # self.ui.___BUTTON___.clicked.connect(___FUNCTION___)
        # self.ui.___COMBO_BOX___.currentIndexChanged.connect(___FUNCTION___)
        # self.ui.___SPIN_BOX___.valueChanged.connect(___FUNCTION___)
        # 自定义信号.属性名.connect(___FUNCTION___)

        self.ui.pushButton.clicked.connect(self.handle_click)

        self.ui.chooseFloderButton.clicked.connect(self.handle_chooseFloderButton_click)  # function不要带括号！！！

        self.ui.decideCalcButton.clicked.connect(self.handle_decideCalcButton_click)

        my_signal.setProgressBar.connect(self.set_progress_bar)

        my_signal.setResult.connect(self.set_result)

    def set_result(self, result: str):
        self.ui.result.setText(result)

    def set_progress_bar(self, progress: int):
        self.ui.progressBar.setValue(progress)

    def set_directory_text(self, directory: str):
        self.ui.directory.setText(directory)

    def set_cell_value(self, row: int, col: int, value: str, table: QTableWidget):
        # 设置指定单元格的内容
        item = QTableWidgetItem(value)
        table.setItem(row, col, item)

    def update_status_table(self, status_dict):
        self.updateTable(self.ui.statusTable, status_dict)

    def update_assignee_table(self, assignee_dict):
        self.updateTable(self.ui.assigneeWG2Table, assignee_dict)
        self.updateTable(self.ui.assigneeWG3Table, assignee_dict)

    def update_product_group_table(self, product_group_dict):
        self.updateTable(self.ui.productGroupTable, product_group_dict)

    def updateTable(self, table: QTableWidget, inputDict: dict):

        row_index = 0
        column_count = table.columnCount()
        # column_names = []
        for col_index in range(column_count):
            item = table.horizontalHeaderItem(col_index)
            column_name = item.text() if item else ""
            # column_names.append(column_name)
            if inputDict.get(column_name) is not None:
                self.set_cell_value(row_index, col_index, str(inputDict[column_name]), table)
            else:
                self.set_cell_value(row_index, col_index, str(0), table)

    def handle_chooseFloderButton_click(self):

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if dialog.exec() == QFileDialog.Accepted:
            self.directory = dialog.selectedFiles()[0]  # 用户选择的目录
            self.ui.directory.setText(self.directory)


    def handle_decideCalcButton_click(self):
        def innerFunc(directory):
            # 运行处理目录的函数
            my_signal.decideCalc.emit(directory)
            status_dict, assignee_dict, product_group_dict = analyStatus(directory)
            self.update_status_table(status_dict)
            self.update_assignee_table(assignee_dict)
            self.update_product_group_table(product_group_dict)


        # args中，如果没有这个逗号，Python 会将字符串中的每个字符都当作一个单独的参数
        task = Thread(target=innerFunc, args=(self.directory,))
        task.start()



    def handle_click(self):
        def innerFunc():
            a = self.ui.InputA.value()
            b = self.ui.InputB.value()

            time_cost = self.ui.timeCost.value()

            for index, _ in enumerate(range(time_cost)):
                progress = index * 100 // time_cost
                my_signal.setProgressBar.emit(progress)
                time.sleep(1)
            my_signal.setProgressBar.emit(100)

            result = str(add(a, b))
            my_signal.setResult.emit(result)

        # args中，如果没有这个逗号，Python 会将字符串中的每个字符都当作一个单独的参数
        task = Thread(target=innerFunc)
        task.start()


if __name__ == '__main__':
    app = QApplication([])  # 启动一个应用
    window = MainWindow()  # 实例化主窗口
    window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出
