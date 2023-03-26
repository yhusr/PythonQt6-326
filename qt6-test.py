import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
import test

def qt6_test():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = test.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    qt6_test()
