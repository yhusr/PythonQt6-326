import os
import shutil
from handle_conf import hy
from handle_os import EXAM_NUM_PATH, PIC_PATH, script_path, store_root_path
from PIL import (Image, ImageFont, ImageDraw)


def draw_image(image_path, text1, data):
    text2 = str(data)
    img = Image.open(image_path)
    font = ImageFont.truetype(r'C:\WINDOWS\FONTS\simsun.ttc', 120)
    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)
    text1_width, text1_height = font.getsize(text1)
    text2_width, text2_height = font.getsize(text2)
    draw.text(((image_width-text1_width)/2,  image_height/6), text1, font=font, fill="red", align="center", stroke_width=5)
    draw.text(((image_width-text2_width)/2,  image_height/3.5), text2, font=font, fill="red", align="center", stroke_width=5)
    img.save(image_path)


def make_cet_1_path():
    base_path = os.path.join(script_path, 'slice')
    # 考试id
    examId = hy.read_yaml('cet_1', 'examId')
    # 科目id
    objectCode = hy.read_yaml('cet_1', 'objectCode')
    # 题目id
    titleNumber = hy.read_yaml('cet_1', 'titleNumber')
    cet_path = os.path.join(base_path, str(examId))
    base_path_1 = os.path.join(cet_path, str(objectCode))
    f = open('exam_number_5000.txt', 'r', encoding='utf-8')
    line = f.readline()
    # str_num = line[:-1]
    # cet_path = os.path.join(cet_path, str_num[0:5])
    # cet_path = os.path.join(cet_path, str_num[5:6])
    # cet_path = os.path.join(cet_path, str_num[10:13])
    # cet_path = os.path.join(cet_path, str(titleNumber))
    page_num = 1
    while line:
        str_num = line[:-1]
        cet_path_1 = os.path.join(base_path_1, str_num[0:5])
        cet_path_2 = os.path.join(cet_path_1, str_num[5:6])
        cet_path_3 = os.path.join(cet_path_2, str_num[10:13])
        cet_path_4 = os.path.join(cet_path_3, str(titleNumber))
        if not os.path.exists(cet_path_4):
            os.makedirs(cet_path_4)
        image_path = os.path.join(cet_path_4, "{}-{}.jpg".format(str_num, str(titleNumber)))
        shutil.copy(PIC_PATH, image_path)
        draw_image(image_path, text1="作文", data=page_num)
        line = f.readline()
        page_num += 1
    f.close()


def make_cet_2_path():
    base_path = os.path.join(script_path, 'slice')
    # 考试id
    examId = hy.read_yaml('cet_2', 'examId')
    # 科目id
    objectCode = hy.read_yaml('cet_2', 'objectCode')
    # 题目id
    titleNumber = hy.read_yaml('cet_2', 'titleNumber')
    cjt_path = os.path.join(base_path, str(examId))
    base_path_1 = os.path.join(cjt_path, str(objectCode))
    f = open('exam_number_5000.txt', 'r', encoding='utf-8')
    line = f.readline()
    # str_num = line[:-1]
    # cet_path = os.path.join(cet_path, str_num[0:5])
    # cet_path = os.path.join(cet_path, str_num[5:6])
    # cet_path = os.path.join(cet_path, str_num[10:13])
    # cet_path = os.path.join(cet_path, str(titleNumber))
    page_num = 1
    while line:
        str_num = line[:-1]
        cjt_path_1 = os.path.join(base_path_1, str_num[0:5])
        cjt_path_2 = os.path.join(cjt_path_1, str_num[5:6])
        cjt_path_3 = os.path.join(cjt_path_2, str_num[10:13])
        cjt_path_4 = os.path.join(cjt_path_3, str(titleNumber))
        if not os.path.exists(cjt_path_4):
            os.makedirs(cjt_path_4)
        image_path = os.path.join(cjt_path_4, "{}-{}.jpg".format(str_num, str(titleNumber)))
        shutil.copy(PIC_PATH, image_path)
        draw_image(image_path, text1="翻译", data=page_num)
        line = f.readline()
        page_num += 1
    f.close()


if __name__ == '__main__':
    # make_cet_1_path()
    make_cet_2_path()
