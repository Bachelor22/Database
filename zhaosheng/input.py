from zhaosheng.Class import Student
from zhaosheng.DAO import StudentDAO


def get_student_info():
    print("请输入考生的个人信息：")
    name = input("姓名: ")
    dob = input("出生日期 (yyyy-mm-dd): ")
    id_card_number = input("身份证号: ")
    source_location = input("生源地: ")
    undergraduate_major = input("本科专业: ")
    email = input("邮箱: ")
    phone = input("电话: ")
    undergraduate_school = input("本科院校: ")
    school_type = input("本科院校类型: ")
    resume = input("个人简历: ")

    # 返回学生信息对象，不包括成绩
    return Student(
        name=name, dob=dob, id_card_number=id_card_number,
        source_location=source_location, undergraduate_major=undergraduate_major,
        email=email, phone=phone, undergraduate_school=undergraduate_school,
        school_type=school_type, resume=resume, preliminary_scores=None, interview_scores=None
    )


# 提交学生材料
def submit_student_material():
    student = get_student_info()  # 获取学生信息
    student_dao = StudentDAO()  # 创建StudentDAO对象
    student_dao.add_student(student)  # 插入学生信息到数据库
    print("学生个人信息提交成功！")