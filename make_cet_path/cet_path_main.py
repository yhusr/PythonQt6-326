import shutil
import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from cet_path import Ui_Dialog
import os
from PIL import (Image, ImageFont, ImageDraw)
import random


class CetPathMake(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.total_num = 0
        self.setupUi(self)
        self.show()
        self.pushButton_pic.clicked.connect(self.make_path)
        self.pushButton_student.clicked.connect(self.student_num)

    def generate_number(self, total_num):
        bean = 0
        # 省份和学校
        province = 10
        # 学校
        school = 100
        # 校区
        # campus_number = 1
        # 年度(固定22年)
        year = 22
        # 考次只有1和2，上半年为1，下半年为2
        examination = 1
        # 语种，暂定两种1和2
        languages = 2
        # 考场三位数
        # examination_room = 1
        # 座位号最大到30
        # seat_number = 1
        while bean <= total_num:
            with open(f'exam_number_{total_num}.txt', 'a', encoding='utf-8') as f:
                while province <= 30 and bean <= total_num:
                    school = 100
                    while school < 600 and bean <= total_num:
                        campus_number = 1
                        while campus_number < 2:
                            examination_room = 1
                            rand_examination = random.randint(40, 50)
                            while examination_room < rand_examination and bean <= total_num:
                                # 座位号最大到30
                                seat_number = 1
                                if examination_room < 10:
                                    rand_number = random.randint(2, 6)
                                    while seat_number < rand_number:
                                        f.write(str(province) + str(school) + str(campus_number) + str(year)
                                                + str(examination) + str(languages) + "00" + str(examination_room) +
                                                "0" + str(seat_number) + "\n")
                                        bean += 1
                                        seat_number += 1
                                else:
                                    rand_number_x = random.randint(2, 6)
                                    while seat_number < rand_number_x:
                                        f.write(str(province) + str(school) + str(campus_number) + str(year)
                                                + str(examination) + str(languages) + "0" + str(examination_room) +
                                                "0" + str(seat_number) + "\n")
                                        bean += 1
                                        seat_number += 1
                                examination_room += 1
                            campus_number += 1
                        school += 1
                    province += 1

    def draw_image(self, image_path, text1, data):

        text2 = str(data)
        img = Image.open(image_path)
        font = ImageFont.truetype(r'C:\WINDOWS\FONTS\simsun.ttc', 120)
        image_width, image_height = img.size
        draw = ImageDraw.Draw(img)
        text1_width, text1_height = font.getsize(text1)
        text2_width, text2_height = font.getsize(text2)
        draw.text(((image_width - text1_width) / 2, image_height / 6), text1, font=font, fill="red", align="center",
                  stroke_width=5)
        draw.text(((image_width - text2_width) / 2, image_height / 3.5), text2, font=font, fill="red", align="center",
                  stroke_width=5)
        img.save(image_path)

    def make_path(self):
        # 需要生成的考生数量
        total_num = self.lineEdit.text()
        if not total_num:
            QMessageBox.warning(self, '信息提示', '请输入考生数量')
            return
        if not total_num.isdigit() or list(total_num)[0] == '0':
            QMessageBox.warning(self, '信息提示', '考生数量输入错误')
            return
        self.total_num = int(total_num)
        self.generate_number(self.total_num)
        script_path = os.getcwd()
        PIC_PATH = os.path.join(script_path, 'SAMPA-1.jpg')
        base_path = os.path.join(script_path, 'slice')
        # 考试id
        examId = self.lineEdit_examID.text()
        # 科目id
        objectCode = self.lineEdit_subjectCode.text()
        # 题目id
        titleNumber = self.lineEdit_mainNum.text()

        if not examId.isdigit() or list(examId)[0] == '0':
            QMessageBox.warning(self, '信息提示', 'examId输入错误')
            return
        if not objectCode.isdigit() or list(objectCode)[0] == '0':
            QMessageBox.warning(self, '信息提示', '科目代码输入错误')
            return
        if not titleNumber.isdigit() or list(titleNumber)[0] == '0':
            QMessageBox.warning(self, '信息提示', '大题号输入错误')
            return
        # 水印文字
        image_text = self.lineEdit_drawImg.text()
        if not image_text:
            image_text = '作文'
        cet_path = os.path.join(base_path, examId)
        base_path_1 = os.path.join(cet_path, objectCode)
        f = open(f'exam_number_{self.total_num}.txt', 'r', encoding='utf-8')
        line = f.readline()
        page_num = 1
        while line:
            str_num = line[:-1]
            cet_path_1 = os.path.join(base_path_1, str_num[0:5])
            cet_path_2 = os.path.join(cet_path_1, str_num[5:6])
            cet_path_3 = os.path.join(cet_path_2, str_num[10:13])
            cet_path_4 = os.path.join(cet_path_3, titleNumber)
            if not os.path.exists(cet_path_4):
                os.makedirs(cet_path_4)
            image_path = os.path.join(cet_path_4, "{}-{}.jpg".format(str_num, titleNumber))
            shutil.copy(PIC_PATH, image_path)
            self.draw_image(image_path, text1=image_text, data=page_num)
            line = f.readline()
            page_num += 1
        f.close()
        QMessageBox.information(self, '信息提示', '考生图片生成成功')

    def student_num(self):
        with open(f'exam_number_{self.total_num}.txt', "r", encoding="utf-8") as f:
            for student_number in f:
                student_data = student_number.strip() + "," + str(random.randint(0, 50)) + random.choice([".0", ".5"])
                with open(f"student_exam_data_{self.total_num}.txt", "a", encoding="utf-8") as f:
                    f.writelines(student_data + "\n")
        QMessageBox.information(self, '信息提示', '考生数据生成成功')
        os.remove(f'exam_number_{self.total_num}.txt')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cetPathMake = CetPathMake()
    sys.exit(app.exec())
