import pandas as pd
import config
from handle_mysql import hm


def write_excel():
    scoredata = pd.read_excel(config.scorepath)
    li_course = scoredata["科目名称"].values
    save_course = []
    for course in li_course:
        result = hm.get_result(args=course)
        save_course.append(result["start_score"])
    scoredata["起始得分"] = save_course
    scoredata.to_excel(config.scorepath, index=False)


if __name__ == '__main__':
    write_excel()
