import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
import sqlite3  # 使用sql数据库
import numpy as np
import os



def is_Chinese(word):
    for ch in word:
        if ch < '\u4e00':
            return False
        if ch > '\u9fff':
            return False
    return True


# 得到当前执行文件同级目录的其他文件绝对路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        # 图标
        self.img = QIcon(resource_path(os.path.join("imgs", "icon.png")))
        self.setWindowIcon(self.img)
        self.setupUi(self)
        self.db = resource_path(os.path.join("db", "ChinessStroke.db"))
        self.conn = sqlite3.connect(self.db)
        print("Opened database successfully")
        self.c = self.conn.cursor()
        self.c.execute('select * from BI_HUA_BEAN')
        self.list = self.c.fetchall()
        self.list = np.array(list)

    def ClickBtn(self):
        inputText = self.lineEdit.text()
        stroke = 0
        if inputText is None:
            QMessageBox.information(self, '提示：', '请输入您的姓名')
        elif is_Chinese(inputText):
            for i in inputText:
                num = ord(i)  # 使用汉字的unicode来匹配
                print(num)
                equal_to_num = (self.list[:, 3] == '%d' % num)
                stroke += int(self.list[equal_to_num, 2])
                print(self.list[equal_to_num, :])
        else:
            stroke = -1

        if (stroke % 2) == 0:
            QMessageBox.information(self, '结果：', '阳性！')
        else:
            if stroke == -1:
                QMessageBox.information(self, '结果：', '阳性！这里是中国！！！\nPositive! This is China!!!')
            else:
                QMessageBox.information(self, '结果：', '阴性！')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = window()
    window.show()
    sys.exit(app.exec())
