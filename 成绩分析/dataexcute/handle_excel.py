from time import sleep

import pandas as pd
import config
from handle_mysql import hm


def write_excel():
    scoredata = pd.read_excel(config.scorepath)
    li_course = scoredata["科目名称"].values
    li_course = list(li_course)
    save_course = []
    for course in li_course:
        result = hm.get_result(args=course)
        if result is not None:
            save_course.append(result["start_score"])
        else:
            save_course.append(0)
    hm.close()
    scoredata['起始得分'] = save_course
    scoredata.to_excel(config.scorepath, index=False)


if __name__ == '__main__':
    write_excel()
