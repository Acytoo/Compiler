from PyQt5.QtCore import QFile, QFileInfo, QSettings, QTimer, Qt, QByteArray
from PyQt5.QtGui import QIcon, QKeySequence, QTextDocumentWriter
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QGridLayout,
                             QMainWindow, QMessageBox, QTabWidget,
                             QWidget, QDockWidget, QTabBar, QListWidget)
import sys
from MyOldEditor import Editor
from analysisUI import AnaUI

'''
新建保存还有bug, 不能保存， 是新建的问题， 这个新建方法写的有问题， 如果还能有时间， 可以改改。。。
2017年11月17日12点35分
@acytoo
'''
class MyMainWindow(QMainWindow):
    filename = ""
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('ic_launcher.png'))
        self.init_ui()
        self.init_menu()
        # Editor()


    def init_ui(self):
        w = QWidget()
        self.layout = QGridLayout()
        w.setObjectName("mainWindow")
        # w.setStyleSheet("background-color:black;")
        '''
        layout used after this???
        '''
        w.setLayout(self.layout)
        self.setCentralWidget(w)
        self.tab = QTabWidget(w)


        qtabBAR = QTabBar()
        # 那些模块的调用可以布置在bar中， 但是不好看， 试试能不能加在右边
        self.tab.setTabBar(qtabBAR)


        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.tab_close)
        self.tab.currentChanged.connect(self.tab_changed)

    def tab_changed(self):
        '''
        最后一个窗口关闭会没有filename, 无法换成另一个， 所以加一个try
        '''
        try:
            self.filename = self.tab.currentWidget().filename
            self.set_current_file_name(self.filename)
        except AttributeError:
            pass

    def tab_close(self, index):
        self.tab.setCurrentIndex(index)
        dock_name = QFileInfo(self.filename).fileName()
        # 关闭标签
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("文件 {0} 已被修改".format(QFileInfo(self.filename).fileName()))
        msgBox.setInformativeText("你想保存这些更改吗？")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec()
        if ret == QMessageBox.Save:
            self.file_save()
            self.tab.removeTab(index)
        elif ret == QMessageBox.Discard:
            self.tab.removeTab(index)
            self.layout.addWidget(self.tab)
        else:
            pass

    '''
    Qaction 使工具栏和菜单同步
    &是助记码
    '''
    def init_menu(self):
        file_new_action = self.create_action("&New", self.file_new,
                                             QKeySequence.New, "Create a text file")
        file_open_action = self.create_action("&Open...", self.file_open,
                                              QKeySequence.Open,
                                              "Open an existing text file")
        file_save_action = self.create_action("&Save", self.file_save,
                                              QKeySequence.Save, "Save the text")
        file_save_as_action = self.create_action("Save &As...",
                                                 self.file_save_as,
                                                 tip="Save the text using a new filename")


        file_quit_action = self.create_action("&Quit", self.close,
                                              "Ctrl+Q", "Close the application")

        '''
                                             "filequit",
        '''

        edit_copy_action = self.create_action("&Copy", self.edit_copy,
                                              QKeySequence.Copy,
                                              "Copy text to the clipboard")
        edit_cut_action = self.create_action("Cu&t", self.edit_cut,
                                             QKeySequence.Cut,
                                             "Cut text to the clipboard")
        edit_paste_action = self.create_action("&Paste", self.edit_paste,
                                               QKeySequence.Paste,
                                               "Paste in the clipboard's text")
        edit_redo_action = self.create_action("&Redo", self.edit_redo,
                                              QKeySequence.Redo,
                                              "Redo")
        edit_undo_action = self.create_action("&Undo", self.edit_undo,
                                              QKeySequence.Undo,
                                              "Undo")
        start_analysis_action = self.create_action("&Start Analysis",
                                                    self.start_analysis, 'F5',
                                                    icon='./resources/Start_icon.png')

        file_menu = self.menuBar().addMenu("&File")
        self.add_actions(file_menu, (file_new_action, file_open_action,
                                     file_save_action, file_save_as_action,
                                     None, file_quit_action))
        edit_menu = self.menuBar().addMenu("&Edit")
        self.add_actions(edit_menu, (edit_copy_action, edit_cut_action, edit_paste_action,
                                     edit_undo_action, edit_redo_action))

        start_toolbar = self.addToolBar("GO")
        start_toolbar.setObjectName("start_toolbar")
        self.add_actions(start_toolbar, (start_analysis_action, start_analysis_action))

    def create_action(self, text, slot=None, shortcut=None,
                      tip=None, checkable=False, signal="triggered()", icon = None):
        action = QAction(text, self)
        '''
        start 在bar中， 可以加一个绿色的三角形作为图标
        '''
        if icon is not None:
            action.setIcon(QIcon("{0}".format(icon)))

        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def file_new(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save as...", None,
                                                      "C Files (*.c *.h);;"
                                                      "Txt files (*.txt);;")
            if filename:
                t = Editor()
                t.filename = filename
                self.tab.addTab(t, QFileInfo(filename).fileName())
                self.tab.setCurrentWidget(t)
                self.layout.addWidget(self.tab)
        except:
            return False
        return True

    def set_current_file_name(self, fileName=''):
        # self.filename = fileName
        self.tab.currentWidget().e_edit.document().setModified(False)
        if not fileName:
            shownName = 'untitled.txt'
        else:
            shownName = QFileInfo(fileName).fileName()
        self.setWindowTitle(self.tr("%s[*] - %s" % (shownName, "Complier Editor")))
        self.setWindowModified(False)

    def file_open(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                                                       "C Files (*.c *.h);;"
                                                       "Txt files (*.txt);;")
        if filename:
            t = Editor()
            t.filename = filename

            self.tab.addTab(t, QFileInfo(filename).fileName())
            self.tab.setCurrentWidget(t)
            self.layout.addWidget(self.tab)
            return self.load_file()
        return False

    def load_file(self):
        if self.filename:
            try:
                inFile = QFile(self.filename)
                if inFile.open(QFile.ReadOnly | QFile.Text):
                    text = inFile.readAll()
                    text = str(text, encoding='utf-8')
                    self.tab.currentWidget().e_edit.setPlainText(text)
                    inFile.close()
            except Exception as e:
                QMessageBox.warning(self, "Text Editor -- Save Error",
                                    "保存失败： {0}: {1}".format(self.filename, e))
                return False
            return True

    def file_save(self):
        '''
        ?????????
        为什么直接调用这个函数会报错， 用下一个就不会报错？？？？？？？？？？？


        明白了， 重命名覆盖问题

        2017年11月17日16点10分
        '''
        print('s',[self.filename])
        if not self.filename:
            return self.file_save_as()
        else:
            writer = QTextDocumentWriter(self.filename)
            success = writer.write(self.tab.currentWidget().e_edit.document())
            if success:
                self.tab.currentWidget().e_edit.document().setModified(False)
                print("save")
                return True
            else:
                QMessageBox.warning(self, "Text Editor -- Save Error",
                                    "保存失败： {0}".format(self.filename))
        return False

    def file_save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save as...", None,
                                            "Txt files (*.txt);;"
                                            "Python files (*.py);;"
                                            "C Files (*.c *.h);;")
        if filename:
            self.filename = filename
            print('sas', [self.filename])
            if self.file_save():
                self.tab.setTabText(self.tab.currentIndex(),QFileInfo(filename).fileName())
        return False
    '''
    以下try为保证程序鲁棒性：
    当没有文件打开时， 调用以下函数不会报错
    '''
    def edit_copy(self):
        try:
            text_edit = self.tab.currentWidget().e_edit
            cursor = text_edit.textCursor()
            text = cursor.selectedText()
            if text:
                clipboard = QApplication.clipboard()
                clipboard.setText(text)
        except AttributeError:
            pass

    def edit_cut(self):
        try:
            text_edit = self.tab.currentWidget().e_edit
            cursor = text_edit.textCursor()
            text = cursor.selectedText()
            if text:
                cursor.removeSelectedText()
                clipboard = QApplication.clipboard()
                clipboard.setText(text)
        except AttributeError:
            pass

    def edit_paste(self):
        try:
            text_edit = self.tab.currentWidget().e_edit
            clipboard = QApplication.clipboard()
            text_edit.insertPlainText(clipboard.text())
        except AttributeError:
            pass

    def edit_redo(self):
        try:
            self.tab.currentWidget().e_edit.redo()
        except AttributeError:
            pass

    def edit_undo(self):
        try:
            self.tab.currentWidget().e_edit.undo()
        except AttributeError:
            pass

    @staticmethod
    def add_actions(target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def start_analysis(self):
        if self.filename:
            self.start_ui = AnaUI(self.filename)
            self.start_ui.show()
        else:
            QMessageBox.warning(self, "\t注意！","请先打开或新建文件！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("Acytxx")
    app.setOrganizationDomain("acytoo.com")
    app.setApplicationName("Complier")
    f = MyMainWindow()
    f.resize(1280, 720)
    f.show()
    app.exec_()
