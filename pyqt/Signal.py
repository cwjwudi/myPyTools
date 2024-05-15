from PySide6.QtCore import Signal, QObject


class MySignal(QObject):
    setResult = Signal(str)
    setProgressBar = Signal(int)
    decideCalc = Signal(str)

my_signal = MySignal()
