import sys
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import (QApplication, QGridLayout, QTextEdit, QWidget, QFrame,
                             QPushButton, QTableWidget, QLineEdit,  QAbstractItemView,
                             QMessageBox, QTableWidgetItem, QFileDialog, QLabel)

from Parser import *


class AnaUI(QFrame):
    filename = ''
    def __init__(self, fname=None):
        Pre_Deal()
        super(AnaUI, self).__init__()
        self.filename = fname
        # print('int ', self.filename)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.token = QLabel("Token")
        self.Key = QLabel("My Language")
        self.symbol = QLabel("Symbol Table")
        self.quat = QLabel("  Quat")
        self.ass = QLabel("Assembly")
        self.err = QLabel("Err Msg")


        self.tokenEdit = QTextEdit()
        self.keyEdit = QTextEdit()
        self.symbolEdit = QTextEdit()
        self.quatEdit = QTextEdit()
        self.assEdit = QTextEdit()
        self.errEdit = QTextEdit()

        self.tokenEdit.setStyleSheet("font: 15pt Comic Sans MS")
        self.keyEdit.setStyleSheet("font: 15pt Comic Sans MS")
        self.symbolEdit.setStyleSheet("font: 15pt Comic Sans MS")
        self.quatEdit.setStyleSheet("font: 15pt Comic Sans MS")
        self.assEdit.setStyleSheet("font: 15pt Comic Sans MS")
        self.errEdit.setStyleSheet("font: 15pt Comic Sans MS")

        self.token.setStyleSheet("font: 13pt Comic Sans MS")
        self.Key.setStyleSheet("font: 13pt Comic Sans MS")
        self.symbol.setStyleSheet("font: 13pt Comic Sans MS")
        self.quat.setStyleSheet("font: 13pt Comic Sans MS")
        self.ass.setStyleSheet("font: 13pt Comic Sans MS")
        self.err.setStyleSheet("font: 13pt Comic Sans MS")
        self.init_ui()
        self.run(self.filename)

    def init_ui(self):

        self.grid.addWidget(self.tokenEdit, 1, 0, 15, 5)
        self.grid.addWidget(self.token, 0, 2)
        self.grid.addWidget(self.keyEdit, 1, 6, 7, 10)
        self.grid.addWidget(self.Key, 0, 10)
        self.grid.addWidget(self.symbolEdit, 1, 17, 7, 10)
        self.grid.addWidget(self.symbol, 0, 22)
        self.grid.addWidget(self.quatEdit, 9, 6, 7, 10)
        self.grid.addWidget(self.quat, 8, 10)
        self.grid.addWidget(self.assEdit, 9, 17, 7, 10)
        self.grid.addWidget(self.ass, 8, 22)
        self.grid.addWidget(self.errEdit, 18, 0, 3, 27)
        self.grid.addWidget(self.err, 17, 13)

        # self.tokenEdit.setText('fgsdfgsdfgsd')

        self.setLayout(self.grid)

        self.setGeometry(30, 30, 1800, 999)
        self.setWindowTitle("Result")
        # self.show()


    def run(self, name):
        global ERR_MSG
        global ASSEMBLY_CODE
        global QUAT_DICT
        global Token
        global SYMBOL_TABLE
        global CODE_RESULT

             # 读取文法， 可以考虑将扫描的文法分析表保存， 以欧化结构， 加快速度
        Lexer.read_source_file(name)   # 读取要分析的文件
        # print(name)
        control(name)
        # self.errEdit.setText('asdfas')
        assem_code = open('./results/'+name.split('/')[-1].split('.')[0]+'.asm', 'w')
        self.symbolEdit.append("名字\t类型\t在内存中的起始位置\t所占内存大小 ")
        for i in ERR_MSG:
            # print(i)
            self.errEdit.append(i)
        for i in ASSEMBLY_CODE:
            self.assEdit.append(i)
            assem_code.write(i+'\n')
        for i in QUAT_DICT:
            self.quatEdit.append(str(QUAT_DICT[i]))
        for i in Token:
            self.tokenEdit.append(str(i))
        for i in SYMBOL_TABLE:
            self.symbolEdit.append(str(i))
        for i in CODE_RESULT:
            self.keyEdit.append(str(CODE_RESULT.index(i)) + ': ' + i)
        assem_code.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("Acytxx")
    app.setOrganizationDomain("acytoo.com")
    app.setApplicationName("Analysis")
    s = AnaUI('1.c')
    s.show()
    app.exec_()
