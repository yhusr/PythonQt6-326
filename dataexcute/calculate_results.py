"""
  功能:计算成绩数据
"""
import pandas as pd
import numpy as np
import config
from handle_excel import write_excel

write_excel()
scoredata = pd.read_excel(config.scorepath)
scoredata = scoredata[scoredata["卷面总分"] > scoredata["起始得分"]]
paperdata = pd.read_excel(config.paperpath)
paperdisdata = pd.read_excel(config.paperdistributionpath)


def excute1(courseCode, papertype, paperName):
    """
      计算试卷特征量数
    """
    # 根据试卷类型，试卷名称，科目划分成绩
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    # 信度1,信度2
    # 做统一处理
    # 试题数量
    k = current_paper.shape[0]
    # 计算客观题
    # 每题方差的和
    var = 0

    def solve(x):
        if x.isnull().loc["客观分得分明细"]:
            pass
        else:
            # 拆分客观题
            idx = 1
            for y in x["客观分得分明细"].split(";"):
                x["object_" + str(idx)] = float(y.split(":")[1])
                idx = idx + 1
        if x.isnull().loc["主观分得分明细"]:
            pass
        else:
            idx = 1
            for y in x["主观分得分明细"].split(";"):
                x["subject_" + str(idx)] = float(y)
                idx = idx + 1
        return x

    groupdata_new = groupdata.apply(solve, axis=1)
    columns = set(groupdata_new.columns)
    var_1 = 0
    var_2 = 0
    for column in columns:
        if "subject" in column or "object" in column:
            var = var + groupdata_new[column].var(ddof=0)
            if int(column.split("_")[1]) % 2 != 0:
                var_1 = var_1 + groupdata_new[column]
            else:
                var_2 = var_2 + groupdata_new[column]
    print("方差的和",var)
    trust_1 = round((k / (k - 1)) * (1 - (var / groupdata["卷面总分"].var(ddof=0))), 2)
    # trust_2有问题
    trust_2 = round(2 * (1 - ((var_1.std(ddof=0) / var_1.mean() + var_2.std(ddof=0) / var_2.mean()) / (
            groupdata["卷面总分"].std(ddof=0) / groupdata["卷面总分"].mean()))), 2)

    print(courseCode, courseName, papertype, paperName, current_paper["小题满分"].sum(), groupdata["卷面总分"].max(),
          groupdata["卷面总分"].min(),
          groupdata["卷面总分"].max() - groupdata["卷面总分"].min(),
          round(groupdata["卷面总分"].mean(), 2)
          , round(groupdata["卷面总分"].std(ddof=0), 2),
          round(groupdata["卷面总分"].std(ddof=0) / groupdata["卷面总分"].mean() * 100, 2), trust_1, trust_2,
          round(groupdata["卷面总分"].mean() / current_paper["小题满分"].sum(), 2)

          )


def excute2(courseCode, papertype, paperName, pingdu=10, customline=[0, 110, 122, 227]):
    """
       计算科目成绩总分频率分布，频度默认10,如需修改，请自行修改
       分数线默认[0,100,120,227],如需修改，请修改customline
    """
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    pingdudatarange = [x for x in range(0, int(current_paper["小题满分"].sum()), pingdu)]
    pingdudatarange.append(float('inf'))
    # groupdata["分数段"]=pd.cut(groupdata["卷面总分"],bins=pingdudatarange,right=False)
    # groupdata.sort_values(by="分数段",inplace=True)
    # table_1=groupdata["分数段"].value_counts().sort_index()
    # dict_table={"分数段":table_1.index,"个数":table_1.values}
    # data_1=pd.DataFrame(dict_table)
    # data_1["频率"]=data_1["个数"]/data_1["个数"].sum()
    # data_1["累计个数"]=data_1["个数"].cumsum()
    # data_1["累计频率"]=data_1["累计个数"]/data_1["个数"].sum()
    data_1 = scorefenduan(groupdata, pingdudatarange)
    print(data_1)
    # 计算自定义分数段
    customline.append(float('inf'))
    data_2 = scorefenduan(groupdata, customline)
    print(data_2)


def scorefenduan(data, cutline):
    data["分数段"] = pd.cut(data["卷面总分"], bins=cutline, right=False)
    data.sort_values(by="分数段", inplace=True)
    table_1 = data["分数段"].value_counts().sort_index()
    dict_table = {"分数段": table_1.index, "个数": table_1.values}
    data_1 = pd.DataFrame(dict_table)
    data_1["频率"] = data_1["个数"] / data_1["个数"].sum()
    data_1["累计个数"] = data_1["个数"].cumsum()
    data_1["累计频率"] = data_1["累计个数"] / data_1["个数"].sum()
    return data_1


def excute3(courseCode, papertype, paperName, customline=[0, 110, 122, 227]):
    """
       科目成绩占初试总分权重
    """
    # 先取该科目成绩
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    # 统计该科目学号下的每个人的成绩总和
    total_score_data = scoredata[scoredata["学号"].isin(list(groupdata["学号"]))]
    # 把成绩合并后求总分
    total_score_data_groupby=total_score_data.groupby(by=["学号"])
    total_score_data_frame=pd.DataFrame(columns=["学号","初试总分"])
    for studentcode,data in total_score_data_groupby:
        total_score_data_frame=total_score_data_frame.append({"学号":studentcode,"初试总分":data["卷面总分"].sum()},ignore_index=True)


    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    # 开始进行分箱
    customline.append(float('inf'))
    total_score_data_frame["分数段"] = pd.cut(total_score_data_frame["初试总分"], bins=customline, right=False)
    total_score_data_frame.sort_values(by="分数段", inplace=True)
    result = pd.DataFrame(columns=["分数段", "人数占比", "初始总分平均分", "本科目成绩平均分", "本科目难度", "占总分权重%"])
    scorelist = set(total_score_data_frame["分数段"])
    for scorerange in scorelist:
        cur_score_data = total_score_data_frame[total_score_data_frame["分数段"] == scorerange]
        total_avg = cur_score_data["初试总分"].mean()
        cur_course_avg = total_score_data[(total_score_data["科目代码"] == courseCode) & (total_score_data["学号"].isin(cur_score_data["学号"]))]["卷面总分"].mean()
        cur_course_diffcult = total_score_data[(total_score_data["科目代码"] == courseCode) & (total_score_data["学号"].isin(cur_score_data["学号"]))]["卷面总分"].mean() / \
                              current_paper["小题满分"].sum()
        zongfen_quanzhong = cur_course_avg/total_avg  * 100
        result = result.append(
            {"分数段": scorerange, "人数占比": cur_score_data.shape[0] / total_score_data_frame.shape[0], "初始总分平均分": total_avg,
             "本科目成绩平均分": cur_course_avg, "本科目难度": cur_course_diffcult, "占总分权重%": zongfen_quanzhong}, ignore_index=True)
    result = result.append(
        {"分数段": "全体考生", "人数占比": 1, "初始总分平均分": total_score_data_frame["初试总分"].mean(),
         "本科目成绩平均分": total_score_data[total_score_data["科目代码"] == courseCode]["卷面总分"].mean(),
         "本科目难度": total_score_data[total_score_data["科目代码"] == courseCode]["卷面总分"].mean() / current_paper["小题满分"].sum(),
         "占总分权重%":total_score_data[total_score_data["科目代码"] == courseCode][
             "卷面总分"].mean()/total_score_data_frame["初试总分"].mean()  * 100}, ignore_index=True)
    #

    print(result)


def excute4(courseCode, papertype, paperName):
    """
       试卷项目编排
    """
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]

    def solve(x):
        if x.isnull().loc["客观分得分明细"]:
            pass
        else:
            # 拆分客观题
            idx = 1
            for y in x["客观分得分明细"].split(";"):
                x["object_" + str(idx)] = float(y.split(":")[1])
                idx = idx + 1
        if x.isnull().loc["主观分得分明细"]:
            pass
        else:
            idx = 1
            for y in x["主观分得分明细"].split(";"):
                x["subject_" + str(idx)] = float(y)
                idx = idx + 1
        return x

    groupdata_new = groupdata.apply(solve, axis=1)

    # 统计每一个子题号的难度指数,按照大题题号，小题号进行分组
    number_group = current_paper.groupby(by=["大题号", "小题号"])
    result = pd.DataFrame(columns=["大题号", "小题号", "难度"])
    object_index_number = 1
    subject_index_number = 1
    for index, questiondata in number_group:
        main_number = index[0]
        sub_number = index[1]
        object_question_data = questiondata[questiondata["是否客观题"] == "是"]
        subject_question_data = questiondata[questiondata["是否客观题"] == "否"]
        total_score = questiondata["小题满分"].sum()
        sum_var = 0
        for i in range(0, object_question_data.shape[0]):
            sum_var = sum_var + groupdata_new["object_" + str(object_index_number)]
            object_index_number = object_index_number + 1
        for i in range(0, subject_question_data.shape[0]):
            sum_var = sum_var + groupdata_new["subject_" + str(subject_index_number)]
            subject_index_number = subject_index_number + 1
        avg = sum_var.mean()
        diffcult = avg / total_score
        result = result.append({"大题号": main_number, "小题号": sub_number, "难度": diffcult}, ignore_index=True)
    print(result)


def excute5(courseCode, papertype, paperName):
    """
           试卷特征量数
        """
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]

    def solve(x):
        if x.isnull().loc["客观分得分明细"]:
            pass
        else:
            # 拆分客观题
            idx = 1
            for y in x["客观分得分明细"].split(";"):
                x["object_" + str(idx)] = float(y.split(":")[1])
                idx = idx + 1
        if x.isnull().loc["主观分得分明细"]:
            pass
        else:
            idx = 1
            for y in x["主观分得分明细"].split(";"):
                x["subject_" + str(idx)] = float(y)
                idx = idx + 1
        return x

    groupdata_new = groupdata.apply(solve, axis=1)

    # 统计每一个子题号的难度指数,按照大题题号，小题号进行分组
    number_group = current_paper.groupby(by=["大题号", "小题号"])
    result = pd.DataFrame(columns=["大题号", "小题号", "满分", "最高分", "最低分", "平均分", "差异系数", "区分度", "零分人数", "有效卷数"])
    object_index_number = 1
    subject_index_number = 1
    for index, questiondata in number_group:
        main_number = index[0]
        sub_number = index[1]
        object_question_data = questiondata[questiondata["是否客观题"] == "是"]
        subject_question_data = questiondata[questiondata["是否客观题"] == "否"]
        total_score = questiondata["小题满分"].sum()
        sum_var = 0
        for i in range(0, object_question_data.shape[0]):
            sum_var = sum_var + groupdata_new["object_" + str(object_index_number)]
            object_index_number = object_index_number + 1
        for i in range(0, subject_question_data.shape[0]):
            sum_var = sum_var + groupdata_new["subject_" + str(subject_index_number)]
            subject_index_number = subject_index_number + 1
        avg = sum_var.mean()
        diffcult = avg / total_score
        import math
        result = result.append(
            {"大题号": main_number, "小题号": sub_number, "满分": questiondata["小题满分"].sum(), "最高分": sum_var.max(),"难度": diffcult,
             "最低分": sum_var.min(),
             "平均分": round(sum_var.mean(), 2), "标准差": round(sum_var.std(), 2),
             "差异系数": round(sum_var.std() / sum_var.mean(), 2)
                , "区分度": (((sum_var * groupdata_new["卷面总分"]).sum()) - (
                    sum_var.sum() * groupdata_new["卷面总分"].sum() / sum_var.shape[0])) / math.sqrt(
                ((sum_var ** 2).sum() - sum_var.sum() ** 2 / sum_var.shape[0]) * (
                        (groupdata_new["卷面总分"] ** 2).sum() - ((
                                                                  groupdata_new["卷面总分"].sum()) ** 2) / sum_var.shape[
                            0])),
             "零分人数": (sum_var == 0).astype(int).sum(), "满分人数":(sum_var == total_score).astype(int).sum(),"有效卷数": sum_var.shape[0]}, ignore_index=True)
    print(result)
    print(result["区分度"])


# excute5("CS2021001", "A", "Y2021090201")

def excute6(courseCode, papertype, paperName, type):
    """
       题型难度分布 type为 题型1，题型2，题型3，内容1,2,3等，参考导入模板
    """
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    current_paper_dis = paperdisdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    # 题型难度一
    current_paper_dis["idx"] = np.array([i for i in range(1, current_paper_dis.shape[0] + 1)])
    current_paper["idx"] = np.array([i for i in range(1, current_paper.shape[0] + 1)])
    question_dis_group_1 = current_paper_dis.groupby(type)

    def solve(x):
        idx = 1
        if x.isnull().loc["客观分得分明细"]:
            pass
        else:
            # 拆分客观题
            for y in x["客观分得分明细"].split(";"):
                x["object_" + str(idx)] = float(y.split(":")[1])
                idx = idx + 1
        if x.isnull().loc["主观分得分明细"]:
            pass
        else:
            for y in x["主观分得分明细"].split(";"):
                x["subject_" + str(idx)] = float(y)
                idx = idx + 1
        return x

    groupdata_new = groupdata.apply(solve, axis=1)
    print("题型,题量,满分,难度")
    for title, data in question_dis_group_1:
        qustion_data = current_paper[current_paper["大题号"].isin(data["大题号"]) & current_paper["小题号"].isin(data["小题号"])]
        sum_var = 0
        hard_num = 0
        hard_score = 0
        normal_num = 0
        normal_score = 0
        easy_num = 0
        easy_score = 0
        for index, ques in qustion_data.iterrows():
            question_index = ques["idx"]
            cur_questiton=0
            if "object_" + str(question_index) in groupdata_new.columns:
                cur_questiton = groupdata_new["object_" + str(question_index)]
                sum_var = sum_var + cur_questiton
            elif "subject_" + str(question_index) in groupdata_new.columns:
                cur_questiton = groupdata_new["subject_" + str(question_index)]
                sum_var = sum_var + cur_questiton
            diffcult = cur_questiton.mean() / ques["小题满分"]
            print(diffcult)
            if diffcult < 0.4:
                # 高难度
                hard_num = hard_num + 1
                hard_score = hard_score + ques["小题满分"]
            elif 0.4 <= diffcult <= 0.6:
                normal_num = normal_num + 1
                normal_score = normal_score + ques["小题满分"]
            elif diffcult > 0.6:
                easy_num = easy_num + 1
                easy_score = easy_score + ques["小题满分"]
        print(title, data.shape[0], qustion_data["小题满分"].sum(), sum_var.mean() / qustion_data["小题满分"].sum())
        print("高难度")
        print("题量", "分值", "%")
        print(hard_num, hard_score, hard_num / data.shape[0])
        print("中难度")
        print("题量", "分值", "%")
        print(normal_num, normal_score, normal_num / data.shape[0])
        print("低难度")
        print("题量", "分值", "%")
        print(easy_num, easy_score, easy_num / data.shape[0])


def excute7(courseCode, papertype, paperName, pingdu=10, customline=[0, 110, 122, 227]):
    """
       试题难度分组分布，10分一段
    """
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    current_paper_dis = paperdisdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    # 题型难度一
    current_paper_dis["idx"] = np.array([i for i in range(1, current_paper_dis.shape[0] + 1)])
    current_paper["idx"] = np.array([i for i in range(1, current_paper.shape[0] + 1)])
    question_dis_group_1 = current_paper_dis.groupby(type)

    def solve(x):
        idx = 1
        if x.isnull().loc["客观分得分明细"]:
            pass
        else:
            # 拆分客观题
            for y in x["客观分得分明细"].split(";"):
                x["object_" + str(idx)] = float(y.split(":")[1])
                idx = idx + 1
        if x.isnull().loc["主观分得分明细"]:
            pass
        else:
            for y in x["主观分得分明细"].split(";"):
                x["subject_" + str(idx)] = float(y)
                idx = idx + 1
        return x

    groupdata_new = groupdata.apply(solve, axis=1)
    # 按总分进行切片
    pingdudatarange = [x for x in range(0, int(current_paper["小题满分"].sum()), pingdu)]
    pingdudatarange.append(float('inf'))
    score_fenduan_1(groupdata_new, pingdudatarange, current_paper)
    customline.append(float('inf'))
    score_fenduan_1(groupdata_new, customline, current_paper)


def score_fenduan_1(data, cutline, paper):
    data["分数段"] = pd.cut(data["卷面总分"], bins=cutline, right=False)
    group_fenduan = data.groupby(by=["分数段"])
    for index, current_ques in paper.iterrows():
        print("大题号,小题号")
        print(current_ques["大题号"], current_ques["小题号"])
        question_index = current_ques["idx"]
        for scorerange, group_data in group_fenduan:
            if group_data.shape[0] != 0:
                if "object_" + str(question_index) in group_data.columns:
                    cur_questiton_score = group_data["object_" + str(question_index)]
                elif "subject_" + str(question_index) in group_data.columns:
                    cur_questiton_score = group_data["subject_" + str(question_index)]
                avg = cur_questiton_score.mean()
            else:
                avg = 0
            # print(cur_questiton_score)
            print(scorerange, avg / current_ques["小题满分"])

    # groupdata_new.sort_values(by="分数段", inplace=True)


def excute8(courseCode, papertype, paperName, type):
    """
       题型区分度分布 type为 题型1，题型2，题型3，内容1,2,3等，参考导入模板
    """
    score_groups = scoredata.groupby(by=["科目代码", "试卷类型", "试卷名称"])
    groupdata = score_groups.get_group((courseCode, papertype, paperName))
    courseName = groupdata["科目名称"].values[0]

    # 获取当前试卷的试题结构
    current_paper = paperdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    current_paper_dis = paperdisdata[
        (paperdata["科目代码"] == courseCode) & (paperdata["试卷类型"] == papertype) & (paperdata["试卷名称"] == paperName)]
    # 题型难度一
    current_paper_dis["idx"] = np.array([i for i in range(1, current_paper_dis.shape[0] + 1)])
    current_paper["idx"] = np.array([i for i in range(1, current_paper.shape[0] + 1)])
    question_dis_group_1 = current_paper_dis.groupby(type)

    def solve(x):
        idx = 1
        if x.isnull().loc["客观分得分明细"]:
            pass
        else:
            # 拆分客观题
            for y in x["客观分得分明细"].split(";"):
                x["object_" + str(idx)] = float(y.split(":")[1])
                idx = idx + 1
        if x.isnull().loc["主观分得分明细"]:
            pass
        else:
            for y in x["主观分得分明细"].split(";"):
                x["subject_" + str(idx)] = float(y)
                idx = idx + 1
        return x

    groupdata_new = groupdata.apply(solve, axis=1)
    print("题型,题量,满分,难度")
    for title, data in question_dis_group_1:
        qustion_data = current_paper[current_paper["大题号"].isin(data["大题号"]) & current_paper["小题号"].isin(data["小题号"])]
        hard_num = 0
        hard_score = 0
        normal_num = 0
        normal_score = 0
        easy_num = 0
        easy_score = 0
        sum_var = 0
        bad_num = 0
        bad_score = 0
        for index, ques in qustion_data.iterrows():
            team_var=0
            question_index = ques["idx"]
            if "object_" + str(question_index) in groupdata_new.columns:
                cur_questiton = groupdata_new["object_" + str(question_index)]
                sum_var = sum_var + cur_questiton
                team_var = team_var + cur_questiton
            elif "subject_" + str(question_index) in groupdata_new.columns:
                cur_questiton = groupdata_new["subject_" + str(question_index)]
                sum_var = sum_var + cur_questiton
                team_var = team_var + cur_questiton
            # diffcult=cur_questiton.mean()/ques["小题满分"]
            import math
            dimeistion = sum_var.std() / sum_var.mean()
            dimeistion_1=(((team_var * groupdata_new["卷面总分"]).sum()) - (
                    team_var.sum() * groupdata_new["卷面总分"].sum() / team_var.shape[0])) / math.sqrt(
                ((team_var ** 2).sum() - team_var.sum() ** 2 / team_var.shape[0]) * (
                        (groupdata_new["卷面总分"] ** 2).sum() - ((
                                                                  groupdata_new["卷面总分"].sum()) ** 2) / team_var.shape[
                            0]))
            print("区分度:",dimeistion_1)
            if dimeistion_1 >= 0.4:
                # 高难度
                hard_num = hard_num + 1
                hard_score = hard_score + ques["小题满分"]
            elif 0.3 <= dimeistion_1 < 0.4:
                normal_num = normal_num + 1
                normal_score = normal_score + ques["小题满分"]
            elif 0.2 <= dimeistion_1 < 0.3:
                easy_num = easy_num + 1
                easy_score = easy_score + ques["小题满分"]
            elif dimeistion_1 < 0.2:
                bad_num = bad_num + 1
                bad_score = bad_score + ques["小题满分"]
        print(title, data.shape[0], qustion_data["小题满分"].sum(), dimeistion)
        print("优")
        print("题量", "分值", "%")
        print(hard_num, hard_score, hard_num / data.shape[0])
        print("良")
        print("题量", "分值", "%")
        print(normal_num, normal_score, normal_num / data.shape[0])
        print("中")
        print("题量", "分值", "%")
        print(easy_num, easy_score, easy_num / data.shape[0])
        print("差")
        print("题量", "分值", "%")
        print(bad_num, bad_score, bad_num / data.shape[0])



#excute8(354, "#", 354,"泛题型F3-1")
#excute7(824010,"#",824010)
# excute6(824009,"#",824009,"题型3")
#excute8(710009,"#",710009,"题型3")
#excute7(710009, "#", 710009)

excute1("CS2021111","A","Y2021090311")
# excute2("CS2021001","A","Y2021090201")
