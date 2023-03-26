import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from password_generate import Ui_PasswordGenerate
import string
import random


class MyPasswordGenerate(Ui_PasswordGenerate, QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.show()

        self.pushButton.clicked.connect(self.new_password)

    def new_password(self):

        site_text = self.lineEdit_site.text()
        if not site_text:
            QMessageBox.warning(self, '信息提示', '请输入网站名称')
            return

        words = []
        if self.checkBox_upc.isChecked():
            words.append(string.punctuation * 2)

        if self.checkBox_lower.isChecked():
            words.append(string.ascii_lowercase * 2)

        if self.checkBox_upper.isChecked():
            words.append(string.ascii_uppercase * 2)

        if self.checkBox_number.isChecked():
            words.append(string.digits * 2)
        if not words:
            words = (string.digits + string.ascii_lowercase + string.ascii_uppercase + string.punctuation)
        else:
            words = ''.join(words)
        words = random.sample(list(words), 20)
        password = ''.join(words)
        with open('我的密码本.txt', 'a', encoding='utf8') as f:
            f.write(f'{site_text}\t{password}\n')
        self.lineEdit_result.setText(password)

        QMessageBox.information(self, '信息提示', '密码生产成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myPasswordGenerate = MyPasswordGenerate()

    sys.exit(app.exec())
