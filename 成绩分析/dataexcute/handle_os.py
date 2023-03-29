import os
import time


current_path = os.path.abspath(__file__)
SCRIPTS_PATH = os.path.dirname(current_path)
# config配置文件的路径：
config_path = os.path.join(SCRIPTS_PATH, 'config')
YAML_PATH = os.path.join(config_path, 'confYaml.yaml')

