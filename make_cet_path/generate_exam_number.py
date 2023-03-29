import random


def generate_number():
    # 需要生成的考生数量
    total_num = 360000
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


if __name__ == '__main__':
    generate_number()
