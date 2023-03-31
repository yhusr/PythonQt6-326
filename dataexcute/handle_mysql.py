import pymysql
import random
from handle_conf import hy


class HandleMysql:
    def __init__(self, host='192.168.10.136', user='exam_score_statistic_test',
                 password='exam_score_statistic_test', port=3307, db='exam_score_statistic_test'):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            charset='utf8',
            db=db,
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    # 查询数据中的数据：如13420835259,
    # hy.read_yaml('mysql', 'sql')
    def get_result(self, sql="SELECT project.start_score FROM `ess_course` as course LEFT JOIN ess_project_course as "
                             "project ON course.id = project.course_id where course.name =%s",
                   args=None, size=1, fetchone=True):
        # result_sql = None
        self.cursor.execute(sql, args)
        self.conn.commit()
        if fetchone:
            result_sql = self.cursor.fetchone()
        else:
            if isinstance(size, int):
                if size >= 0:
                    result_sql = self.cursor.fetchmany(size=size)
                else:
                    result_sql = self.cursor.fetchall()
            else:
                print(f'此查询长度{size}输入错误')
        return result_sql

    def close(self):
        self.cursor.close()
        self.conn.close()


hm = HandleMysql()

if __name__ == '__main__':
    hm = HandleMysql()
    result = hm.get_result(sql="SELECT name FROM ess_course where code=%s", args='841')['name']
    print(result)
    hm.close()
    # result = hm.get_result(args='德语')
    # hm.close()
    # print(result["start_score"], type(result["start_score"]))
    # phone = hm.no_exists_result()
    # print(phone)
