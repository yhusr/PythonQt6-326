import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from json_format import Ui_Dialog
import json


class JsonFormat(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.show()

        self.pushButton_format.clicked.connect(self.json_format('format'))
        self.pushButton_unformat.clicked.connect(self.json_format('unformat'))
        self.pushButton_copy.clicked.connect(self.copy_json)

    def json_format(self, type):
        def inner_format():
            plain_text = self.plainTextEdit.toPlainText()
            if not plain_text:
                QMessageBox.warning(self, '信息提示', '输入内容为空')
                return
            try:
                if type == 'format':
                    result = json.dumps(json.loads(plain_text), indent=4, ensure_ascii=False)
                else:
                    result = json.dumps(json.loads(plain_text), ensure_ascii=False)
            except Exception as e:
                QMessageBox.warning(self, '信息提示', f'输入内容错误:{e}')
                return
            else:
                self.plainTextEdit.setPlainText(result)
        return inner_format

    def copy_json(self):
        board = QApplication.clipboard()
        board.setText(self.plainTextEdit.toPlainText())
        QMessageBox.information(self, '信息提示', '复制成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    jsonFormat = JsonFormat()
    sys.exit(app.exec())
