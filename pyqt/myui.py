# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'myui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_10 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.chooseFloderButton = QPushButton(self.tab)
        self.chooseFloderButton.setObjectName(u"chooseFloderButton")

        self.horizontalLayout_6.addWidget(self.chooseFloderButton)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)

        self.decideCalcButton = QPushButton(self.tab)
        self.decideCalcButton.setObjectName(u"decideCalcButton")

        self.horizontalLayout_6.addWidget(self.decideCalcButton)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_11)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")
        font = QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_6)

        self.directory = QLabel(self.tab)
        self.directory.setObjectName(u"directory")

        self.horizontalLayout_7.addWidget(self.directory)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.statusTable = QTableWidget(self.tab)
        if (self.statusTable.columnCount() < 5):
            self.statusTable.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.statusTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.statusTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.statusTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.statusTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.statusTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.statusTable.rowCount() < 1):
            self.statusTable.setRowCount(1)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.statusTable.setVerticalHeaderItem(0, __qtablewidgetitem5)
        self.statusTable.setObjectName(u"statusTable")

        self.verticalLayout.addWidget(self.statusTable)

        self.productGroupTable = QTableWidget(self.tab)
        if (self.productGroupTable.columnCount() < 7):
            self.productGroupTable.setColumnCount(7)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(4, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(5, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.productGroupTable.setHorizontalHeaderItem(6, __qtablewidgetitem12)
        if (self.productGroupTable.rowCount() < 1):
            self.productGroupTable.setRowCount(1)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.productGroupTable.setVerticalHeaderItem(0, __qtablewidgetitem13)
        self.productGroupTable.setObjectName(u"productGroupTable")

        self.verticalLayout.addWidget(self.productGroupTable)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_4.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.assigneeWG2Table = QTableWidget(self.tab)
        if (self.assigneeWG2Table.columnCount() < 6):
            self.assigneeWG2Table.setColumnCount(6)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.assigneeWG2Table.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.assigneeWG2Table.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.assigneeWG2Table.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.assigneeWG2Table.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.assigneeWG2Table.setHorizontalHeaderItem(4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.assigneeWG2Table.setHorizontalHeaderItem(5, __qtablewidgetitem19)
        if (self.assigneeWG2Table.rowCount() < 1):
            self.assigneeWG2Table.setRowCount(1)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.assigneeWG2Table.setVerticalHeaderItem(0, __qtablewidgetitem20)
        self.assigneeWG2Table.setObjectName(u"assigneeWG2Table")

        self.verticalLayout.addWidget(self.assigneeWG2Table)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.horizontalLayout_8.addWidget(self.label_7)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.assigneeWG3Table = QTableWidget(self.tab)
        if (self.assigneeWG3Table.columnCount() < 6):
            self.assigneeWG3Table.setColumnCount(6)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.assigneeWG3Table.setHorizontalHeaderItem(0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.assigneeWG3Table.setHorizontalHeaderItem(1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.assigneeWG3Table.setHorizontalHeaderItem(2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.assigneeWG3Table.setHorizontalHeaderItem(3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.assigneeWG3Table.setHorizontalHeaderItem(4, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.assigneeWG3Table.setHorizontalHeaderItem(5, __qtablewidgetitem26)
        if (self.assigneeWG3Table.rowCount() < 1):
            self.assigneeWG3Table.setRowCount(1)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.assigneeWG3Table.setVerticalHeaderItem(0, __qtablewidgetitem27)
        self.assigneeWG3Table.setObjectName(u"assigneeWG3Table")

        self.verticalLayout.addWidget(self.assigneeWG3Table)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 189, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.InputA = QDoubleSpinBox(self.tab_2)
        self.InputA.setObjectName(u"InputA")

        self.horizontalLayout_2.addWidget(self.InputA)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.InputB = QDoubleSpinBox(self.tab_2)
        self.InputB.setObjectName(u"InputB")

        self.horizontalLayout_2.addWidget(self.InputB)

        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.result = QLabel(self.tab_2)
        self.result.setObjectName(u"result")

        self.horizontalLayout_2.addWidget(self.result)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.progressBar = QProgressBar(self.tab_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_3.addWidget(self.progressBar)

        self.pushButton = QPushButton(self.tab_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.timeCost = QSpinBox(self.tab_2)
        self.timeCost.setObjectName(u"timeCost")

        self.horizontalLayout.addWidget(self.timeCost)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 189, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_10.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.chooseFloderButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.decideCalcButton.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5939\u8def\u5f84\uff1a", None))
        self.directory.setText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84", None))
        ___qtablewidgetitem = self.statusTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Open", None));
        ___qtablewidgetitem1 = self.statusTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Inprocess", None));
        ___qtablewidgetitem2 = self.statusTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Closed", None));
        ___qtablewidgetitem3 = self.statusTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Quality", None));
        ___qtablewidgetitem4 = self.statusTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"None", None));
        ___qtablewidgetitem5 = self.statusTable.verticalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u6570\u91cf", None));
        ___qtablewidgetitem6 = self.productGroupTable.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Control", None));
        ___qtablewidgetitem7 = self.productGroupTable.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Hardware", None));
        ___qtablewidgetitem8 = self.productGroupTable.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Motion", None));
        ___qtablewidgetitem9 = self.productGroupTable.horizontalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Visual", None));
        ___qtablewidgetitem10 = self.productGroupTable.horizontalHeaderItem(4)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"software", None));
        ___qtablewidgetitem11 = self.productGroupTable.horizontalHeaderItem(5)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Other", None));
        ___qtablewidgetitem12 = self.productGroupTable.horizontalHeaderItem(6)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"None", None));
        ___qtablewidgetitem13 = self.productGroupTable.verticalHeaderItem(0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u6570\u91cf", None));
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"WG2", None))
        ___qtablewidgetitem14 = self.assigneeWG2Table.horizontalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Ma Ruiqi", None));
        ___qtablewidgetitem15 = self.assigneeWG2Table.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Xu Zhihang", None));
        ___qtablewidgetitem16 = self.assigneeWG2Table.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Ye Qinglong", None));
        ___qtablewidgetitem17 = self.assigneeWG2Table.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Pan Junru", None));
        ___qtablewidgetitem18 = self.assigneeWG2Table.horizontalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Deng Hougang", None));
        ___qtablewidgetitem19 = self.assigneeWG2Table.horizontalHeaderItem(5)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"None", None));
        ___qtablewidgetitem20 = self.assigneeWG2Table.verticalHeaderItem(0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"\u6570\u91cf", None));
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"WG3", None))
        ___qtablewidgetitem21 = self.assigneeWG3Table.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Cui Wenjie", None));
        ___qtablewidgetitem22 = self.assigneeWG3Table.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Dai Juncheng", None));
        ___qtablewidgetitem23 = self.assigneeWG3Table.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Jiang Peiyang", None));
        ___qtablewidgetitem24 = self.assigneeWG3Table.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Zhou Shenyang", None));
        ___qtablewidgetitem25 = self.assigneeWG3Table.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Jing Feng", None));
        ___qtablewidgetitem26 = self.assigneeWG3Table.horizontalHeaderItem(5)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"None", None));
        ___qtablewidgetitem27 = self.assigneeWG3Table.verticalHeaderItem(0)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"\u6570\u91cf", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u6570\u91cf", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.result.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u5ea6", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u52a0\u6cd5\u5668", None))
    # retranslateUi

