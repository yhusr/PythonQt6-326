import random


def read_write():
    with open("exam_number_360000.txt", "r", encoding="utf-8") as f:
        for student_number in f:
            student_data = student_number.strip() + "," + str(random.randint(0, 50)) + random.choice([".0", ".5"])
            with open("student_exam_data_360000.txt", "a", encoding="utf-8") as f:
                f.writelines(student_data + "\n")


if __name__ == '__main__':
    read_write()
