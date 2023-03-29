import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from phones_extras import Ui_Dialog
import re


class PhoneExtra(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pushButton_extra.clicked.connect(self.extra_phone)
        self.pushButton_copy.clicked.connect(self.copy_phone)

    def extra_phone(self):
        plain_text = self.plainTextEdit_extra.toPlainText()
        if not plain_text:
            QMessageBox.warning(self, '信息提示', '请输入内容')
            return
        partten = r'1\d{10}'
        phone_list = re.findall(partten, plain_text)
        phone_result = '\n'.join(phone_list)
        self.plainTextEdit_phones.setPlainText(phone_result)

    def copy_phone(self):
        board = QApplication.clipboard()
        board.setText(self.plainTextEdit_phones.toPlainText())
        QMessageBox.information(self, '信息提示', '复制成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    phoneExtra = PhoneExtra()
    sys.exit(app.exec())