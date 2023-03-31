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
            ry = yaml.full_load(f)
        result = ry[section_name][option_name]
        return result

    def write_yaml(self, datas, mode='a'):
        with open(self.filepath, mode, encoding='utf-8') as f:
            yaml.dump(datas, f, allow_unicode=True)


hy = HandleYaml()


if __name__ == '__main__':
    pass
    # hy = HandleYaml()
    # result = hy.read_yaml('mysql', 'host')
    # print(result)
    # dict1 = {'mysql': {
    #     'db': 'course'
    # }}
    # hy.write_yaml(dict1)
