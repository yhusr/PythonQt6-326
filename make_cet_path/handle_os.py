import os
import time

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
store_root_path = "G:/"

# config目录
YAML_PATH = os.path.join(script_path, 'my_yaml.yaml')
EXAM_NUM_PATH = os.path.join(script_path, 'exam_number_100W.txt')

# 图片目录
PIC_PATH = os.path.join(script_path, 'SAMPA-1.jpg')