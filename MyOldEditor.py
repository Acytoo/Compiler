from PyQt5.QtCore import (QTimer, Qt)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QLabel, QGridLayout,
                             QWidget)

from editCore import TextEdit

__version__ = "2.0.0"
'''
自动补全还是不行， 暂时先放下了
2017年11月17日12点30分
@acytoo
'''

class Editor(QWidget):
    NextId = 1
    filename = ""
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.filename = 'Unnamed-{0}.txt'.format(
                         Editor.NextId)
        Editor.NextId += 1
        self.init_ui()

    def init_ui(self):
        self.init_edit(self)

    def init_edit(self, widget):
        font = QFont()
        self.e_label = QLabel(widget)
        self.e_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.e_label.setWordWrap(True)
        self.e_label.setText("1\n")

        self.LineCount = 1
        self.LineNo = 1
        self.startLine = 1

        font.setPointSize(12)
        self.e_label.setFont(font)
        self.e_label.setMargin(3)
        self.e_edit = TextEdit(widget)
        self.e_edit.setFont(font)
        g_edit = QGridLayout()
        g_edit.setColumnStretch(0, 2)
        g_edit.setColumnStretch(1, 100)
        g_edit.addWidget(self.e_label, 0, 0)
        g_edit.addWidget(self.e_edit, 0, 1)
        widget.setLayout(g_edit)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateLineNum)
        self.timer.start(100)

    def updateLineNum(self):
        self.startLine = self.e_edit.scrollbar.value() // 240
        h_c = int(self.e_edit.height() / 19.5)
        str_l = ""
        count = self.e_edit.document().blockCount()
        if count < h_c:
            end = count
        else:
            end = h_c
        for i in range(1, end):
            str_l += "%3d\n"%(i + self.startLine)
        str_l += "%3d\n"%(end + self.startLine)
        self.e_label.setText(str_l)
