import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from IBMcalc import Ui_BmiCompute
import string


class BmiComputeChinese(QDialog, Ui_BmiCompute):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.show()

        self.pushButton.clicked.connect(self.calc_chinese_bmi)

    def calc_chinese_bmi(self):
        height = self.lineEdit_stature.text()
        weight = self.lineEdit_weight.text()
        if not height or not weight:
            QMessageBox.warning(self, '信息提示', '请输入身高或者体重')
            return
        try:
            height = float(height)
            weight = float(weight)
        except Exception :
            QMessageBox.warning(self, '信息提示', '身高或体重输入不规范，请重新输入')
            return
        else:
            if height <= 0 or weight <= 0:
                QMessageBox.warning(self, '信息提示', '身高或体重应为正数')
                return
            bmi_calc = weight/pow(height/100, 2)
            bmi_calc = round(bmi_calc)
            best_bmi = int(22 * pow(height/100, 2))
            if bmi_calc < 18.5:
                self.label_warning.setText(f'BMI:{bmi_calc},属于体重过低，您的理想体重是{best_bmi}kg')
            if 18.5 <= bmi_calc <= 24:
                self.label_warning.setText(f'BMI:{bmi_calc},属于正常体重，您的理想体重是{best_bmi}kg')
            if bmi_calc > 24:
                self.label_warning.setText(f'BMI:{bmi_calc},属于体重超重，您的理想体重是{best_bmi}kg')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bmiComputeChinese = BmiComputeChinese()
    sys.exit(app.exec())