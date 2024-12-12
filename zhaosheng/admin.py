from zhaosheng.DAO import StudentDAO, InterviewCandidateDAO
from zhaosheng.input import get_student_info
from datetime import datetime


# 获取管理员输入的学生成绩信息
def get_scores_from_admin():
    print("请输入要更新的学生成绩信息：")
    show_all_students()  # 显示所有学生信息

    # 输入学生ID
    student_id = int(input("请输入学生ID: "))

    # 获取学生信息并显示
    student_info = get_student_info(student_id)
    if not student_info:
        return None  # 如果找不到该学生，退出

    # 输入成绩信息
    foreign_language_score = int(input("外语成绩: "))
    professional_knowledge_score = int(input("专业知识成绩: "))
    comprehensive_ability_score = int(input("综合素质面试成绩: "))

    # 输入并验证复试时间格式
    while True:
        interview_time_str = input("复试时间 (yyyy-mm-dd hh:mm:ss): ")
        try:
            # 尝试将输入的字符串转换为 datetime 对象
            interview_time = datetime.strptime(interview_time_str, "%Y-%m-%d %H:%M:%S")
            break  # 如果转换成功，跳出循环
        except ValueError:
            print("日期格式错误，请按照 yyyy-mm-dd hh:mm:ss 格式输入时间。")

    interview_location = input("复试地点: ")

    # 输入新增的字段信息
    interview_evaluation = input("面试评价: ")
    interview_group_members = input("面试小组成员: ")
    proposed_mentor_signatures = input("拟定导师签名: ")

    # 计算复试总成绩
    total_score = foreign_language_score + professional_knowledge_score + comprehensive_ability_score

    # 将成绩存入 interview_scores 表
    student_dao = StudentDAO()  # 创建DAO对象
    student_dao.add_interview_score(student_id, foreign_language_score, professional_knowledge_score,
                                    comprehensive_ability_score, total_score, interview_time, interview_location,
                                    interview_evaluation, interview_group_members, proposed_mentor_signatures)

    print("学生成绩已成功更新！")

# 显示所有学生信息
def show_all_students():
    student_dao = StudentDAO()  # 创建StudentDAO对象
    students = student_dao.get_all_students()  # 获取所有学生数据

    print("\n--- 所有学生信息 ---")
    print("学生ID | 姓名")  # 只显示ID和姓名
    for student in students:
        print(f"{student[0]} | {student[1]}")
    print("\n")


# 管理员输入学生ID和录取状态
def get_admission_info_from_admin():
    print("请输入要更新的学生录取状态信息：")
    student_id = int(input("学生ID: "))
    admission_status = input("录取状态 (已录取/未录取): ")

    # 返回录取状态信息
    return student_id, admission_status


# 更新学生录取状态
def update_student_admission_status():
    show_all_students()  # 显示所有学生信息
    student_id, admission_status = get_admission_info_from_admin()  # 获取管理员输入的学生ID和录取状态
    student_dao = StudentDAO()  # 创建 DAO 对象
    student_dao.update_admission_status(student_id, admission_status)  # 更新学生录取状态
    print("学生录取状态更新成功！")

def get_interview_candidate_info_from_admin():
    print("请输入学生的志愿信息：")

    # 输入学生ID并获取学生信息
    student_id = int(input("请输入学生ID: "))
    student_info = get_student_info(student_id)
    if not student_info:
        return None  # 如果找不到该学生，退出

    # 输入个人信息
    gender = input("性别: ")
    candidate_type = input("考生类型（应届生/往届生/同等学力，定向生/非定向考生）: ")
    graduation_school = input("本科毕业学校及时间: ")
    major = input("毕业专业: ")
    contact_phone = input("考生联系方式（本人手机号）: ")
    emergency_contact_phone = input("紧急联系人手机号: ")

    # 输入导师志愿
    first_choice_mentor = int(input("一志愿导师ID: "))
    second_choice_mentor = int(input("二志愿导师ID: "))
    third_choice_mentor = int(input("三志愿导师ID: "))

    # 输入报考方向和是否接受方向调整
    research_direction = input("报考研究方向（计算机科学与技术考生填写）: ")
    accepts_direction_adjustment = input("是否接受方向调整（仅电子信息全日制考生填写）: ")
    direction_adjustment_order = input("方向调整的优先顺序（电子信息考生填写，1,2,3,4）: ")

    # 签名确认
    signature = input("考生签名确认（信息真实）: ")

    # 提交信息
    interview_candidate_dao = InterviewCandidateDAO()
    interview_candidate_dao.add_interview_candidate(student_id, gender, candidate_type, graduation_school, major,
                                                    contact_phone, emergency_contact_phone, first_choice_mentor,
                                                    second_choice_mentor, third_choice_mentor, research_direction,
                                                    accepts_direction_adjustment, direction_adjustment_order, signature)


def get_student_info(student_id):
    # 创建DAO对象
    student_dao = StudentDAO()

    # 从数据库中获取学生信息
    student_info = student_dao.get_student_by_id(student_id)  # 根据student_id获取学生信息

    if student_info:
        print(f"学生ID: {student_info[0]}, 姓名: {student_info[1]}")  # 显示学生ID和姓名
        return student_info  # 返回学生信息
    else:
        print("未找到该学生信息！")
        return None  # 如果没有找到学生，返回None