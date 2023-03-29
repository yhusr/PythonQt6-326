import configparser
import yaml
from handle_os import YAML_PATH


class HandleYaml:
    def __init__(self, filepath=None):
        if filepath:
            self.filepath = filepath
        else:
            self.filepath = YAML_PATH

    def read_yaml(self, section_name, option_name):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            read_out = yaml.full_load(f)
        yaml_value = read_out[section_name][option_name]
        return yaml_value

    def write_yaml(self, datas):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            yaml.dump(datas, stream=f, allow_unicode=True)

    def write_phone_yaml(self, datas):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            yaml.dump(datas, stream=f, allow_unicode=True)


hy = HandleYaml()
