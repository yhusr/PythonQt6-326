import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog, QComboBox
from score_calc import Ui_PerformanceAnalysis
from handle_mysql import HandleMysql


class PerformanceAnalysis(Ui_PerformanceAnalysis, QDialog):
    def __init__(self):
        super().__init__()
        self.li_item = ['计算试卷特征量数', '计算科目成绩总分频率分布', '科目成绩占初试总分权重', '试卷项目编排', '试卷特征量数',
                   '题型难度分布', '试题难度分组分布', '题型区分度分布']
        self.li_cal = ['excute1', 'excute2', 'excute3', 'excute4', 'excute5', 'excute6', 'excute7', 'excute8']
        self.scorceDetails_path = ''
        self.examstruct_path = ''
        self.questionstruct_path = ''
        self.handleMysql = ''
        self.result = ''
        self.setupUi(self)
        self.comboBox_target.addItems(self.li_item)
        self.show()
        self.pushButton_scoreDetails.clicked.connect(self.choose_sorcedetails)
        self.pushButton_examStruct.clicked.connect(self.choose_examstruct)
        self.pushButton_questionStruct.clicked.connect(self.choose_questionstruct)
        self.pushButton_count.clicked.connect(self.count)

    def choose_sorcedetails(self):
        self.scorceDetails_path = QFileDialog.getOpenFileName(self, '选择得分明细表', os.getcwd(),
                                                              'Excel files (*.xlsx)')[0]
        self.lineEdit_score_details.setText(self.scorceDetails_path)

    def choose_examstruct(self):
        self.examstruct_path = QFileDialog.getOpenFileName(self, '选择试卷结构表', os.getcwd(),
                                                           'Excel files (*.xlsx)')[0]
        self.lineEdit_paper_struct.setText(self.examstruct_path)

    def choose_questionstruct(self):
        self.questionstruct_path = QFileDialog.getOpenFileName(self, '选择试题结构表', os.getcwd(),
                                                               'Excel files (*.xlsx)')[0]
        self.lineEdit_question.setText(self.questionstruct_path)

    def count(self):
        li_mysql = [self.lineEdit_host.text().strip(), self.lineEdit_user.text().strip(),
                    self.lineEdit_password.text().strip(), self.lineEdit_port.text().strip(),
                    self.lineEdit_db.text().strip()]
        if '' not in li_mysql or li_mysql.count('') < len(li_mysql):
            host = self.lineEdit_host.text().strip()
            user = self.lineEdit_user.text().strip()
            password = self.lineEdit_password.text().strip()
            port = int(self.lineEdit_port.text().strip())
            db = self.lineEdit_db.text().strip()
            try:
                self.handleMysql = HandleMysql(host=host, user=user, password=password, port=port, db=db)
            except Exception:
                QMessageBox.warning(self, '信息提示', '数据库连接信息输入有误或输入不完整')
        course_code = self.lineEdit_courseCode.text()
        if not course_code:
            QMessageBox.warning(self, '信息提示', '课程代码输入为空')
            return
        try:
            self.handleMysql = HandleMysql()
            self.result = self.handleMysql.get_result(sql="SELECT name FROM ess_course where code=%s", args=course_code)['name']
            if not self.result:
                QMessageBox.warning(self, '信息提示', '请确认课程代码输入是否正确')
                return
        except Exception:
            QMessageBox.warning(self, '信息提示', '数据库连接失败')
            return
        current_combox = self.comboBox_target.currentText()
        current_index = self.li_item.index(current_combox)
        if current_index == 0:
            self.label_customline.setVisible(False)
            self.lineEdit_customline.setVisible(False)
            self.label_frequentness.setVisible(False)
            self.lineEdit_frequentness.setVisible(False)
            self.label_type.setVisible(False)
            self.lineEdit_type.setVisible(False)











if __name__ == '__main__':
    app = QApplication(sys.argv)
    performanceAnalysis = PerformanceAnalysis()
    sys.exit(app.exec())
