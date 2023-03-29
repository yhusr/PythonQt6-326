import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog
from file_arrang import Ui_Dialog


class FileArrang(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.dir_path = ''
        self.setupUi(self)
        self.show()
        self.pushButton_chose.clicked.connect(self.choose_dir)
        self.pushButton_arrang.clicked.connect(self.arrang_dir)
        self.pushButton_open.clicked.connect(self.open_path)

    def open_path(self):
        if not self.dir_path:
            QMessageBox.warning(self, '信息提示', '未选择文件夹')
            return
        os.startfile(self.dir_path)

    def arrang_dir(self):
        if not self.dir_path:
            QMessageBox.warning(self, '信息提示', '未选择文件夹')
            return
        for name in os.listdir(self.dir_path):
            if os.path.isdir(os.path.join(self.dir_path, name)):
                continue
            dir_name = name.split('.')[-1].strip()
            file_dir_name = os.path.join(self.dir_path, dir_name)
            if not os.path.exists(file_dir_name):
                os.makedirs(file_dir_name)
            shutil.move(os.path.join(self.dir_path, name), os.path.join(file_dir_name, name))
        QMessageBox.information(self, '信息提示', '整理完成')

    def choose_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, '打开目录', os.getcwd())
        self.lineEdit_filepath.setText(self.dir_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileArrang = FileArrang()
    sys.exit(app.exec())
