import pymysql
import random
from handle_conf import hy


class HandleMysql:
    def __init__(self):
        self.conn = pymysql.connect(
            host=hy.read_yaml('mysql', 'host'),
            user=hy.read_yaml('mysql', 'user'),
            password=hy.read_yaml('mysql', 'password'),
            port=hy.read_yaml("mysql", "port"),
            charset='utf8',
            db=hy.read_yaml('mysql', 'db'),
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    # 查询数据中的数据：如13420835259,
    # hy.read_yaml('mysql', 'sql')
    def get_result(self, sql=hy.read_yaml('mysql', 'sql'), args=None, size=1, fetchone=True):
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
    result = hm.get_result(hy.read_yaml('mysql', 'sql'), '翻译实践')
    hm.close()
    print(result["start_score"], type(result["start_score"]))
    # phone = hm.no_exists_result()
    # print(phone)
