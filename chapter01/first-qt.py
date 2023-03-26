from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QHBoxLayout, QMessageBox
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QDialog()
    window.resize(400, 300)
    button = QPushButton('点击我')

    def msg_click():
        QMessageBox.information(window, 'msg弹窗', '请再次点击我')
    button.clicked.connect(msg_click)
    layout = QHBoxLayout()
    layout.addWidget(button)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())