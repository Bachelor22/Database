class User:
    def __init__(self, username, password, email, phone):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone

class Subject:
    def __init__(self, subject_id, subject_name, subject_level, parent_subject, subject_description, subject_type, year, total_quota, supplementary_quota):
        self.subject_id = subject_id  # 学科ID
        self.subject_name = subject_name  # 学科名称
        self.subject_level = subject_level  # 学科等级
        self.parent_subject = parent_subject  # 上级学科
        self.subject_description = subject_description  # 学科描述
        self.subject_type = subject_type  # 学科类型
        self.year = year  # 年度
        self.total_quota = total_quota  # 年度总指标
        self.supplementary_quota = supplementary_quota  # 年度补充指标

    def __repr__(self):
        return f"Subject(subject_id={self.subject_id}, subject_name={self.subject_name}, subject_level={self.subject_level}, " \
               f"parent_subject={self.parent_subject}, subject_description={self.subject_description}, subject_type={self.subject_type}, " \
               f"year={self.year}, total_quota={self.total_quota}, supplementary_quota={self.supplementary_quota})"

class SubjectMentor:
    def __init__(self, mentor_id, mentor_name, mentor_title, mentor_photo, mentor_bio, mentor_email, mentor_phone, subject_id):
        self.mentor_id = mentor_id  # 导师ID
        self.mentor_name = mentor_name  # 导师姓名
        self.mentor_title = mentor_title  # 导师职称
        self.mentor_photo = mentor_photo  # 导师照片
        self.mentor_bio = mentor_bio  # 导师简介
        self.mentor_email = mentor_email  # 导师邮箱
        self.mentor_phone = mentor_phone  # 导师电话
        self.subject_id = subject_id  # 所在学科ID

    def __repr__(self):
        return f"SubjectMentor(mentor_id={self.mentor_id}, mentor_name={self.mentor_name}, mentor_title={self.mentor_title}, " \
               f"mentor_photo={self.mentor_photo}, mentor_bio={self.mentor_bio}, mentor_email={self.mentor_email}, " \
               f"mentor_phone={self.mentor_phone}, subject_id={self.subject_id})"
class Student:
    def __init__(self, name, dob, id_card_number, source_location, undergraduate_major, email, phone, undergraduate_school, school_type, resume, preliminary_scores, interview_scores, student_id=None):
        self.student_id = student_id  # student_id 可以为空，因为它由数据库自动生成
        self.name = name
        self.dob = dob
        self.id_card_number = id_card_number
        self.source_location = source_location
        self.undergraduate_major = undergraduate_major
        self.email = email
        self.phone = phone
        self.undergraduate_school = undergraduate_school
        self.school_type = school_type
        self.resume = resume
        self.preliminary_scores = preliminary_scores
        self.interview_scores = interview_scores

    def __repr__(self):
        return f"Student(student_id={self.student_id}, name={self.name}, dob={self.dob}, id_card_number={self.id_card_number}, " \
               f"source_location={self.source_location}, undergraduate_major={self.undergraduate_major}, email={self.email}, " \
               f"phone={self.phone}, undergraduate_school={self.undergraduate_school}, school_type={self.school_type}, " \
               f"resume={self.resume}, preliminary_scores={self.preliminary_scores}, interview_scores={self.interview_scores})"

class InterviewCandidate:
    def __init__(self, candidate_id, student_id, student_name, gender, candidate_type, graduation_school, major, contact_phone, emergency_contact_phone, first_choice_mentor, second_choice_mentor, third_choice_mentor, research_direction, accepts_direction_adjustment, direction_adjustment_order, signature):
        self.candidate_id = candidate_id  # 复试考生ID
        self.student_id = student_id  # 学生ID
        self.student_name = student_name  # 学生姓名
        self.gender = gender  # 性别
        self.candidate_type = candidate_type  # 考生类型
        self.graduation_school = graduation_school  # 毕业学校
        self.major = major  # 毕业专业
        self.contact_phone = contact_phone  # 联系电话
        self.emergency_contact_phone = emergency_contact_phone  # 紧急联系人电话
        self.first_choice_mentor = first_choice_mentor  # 第一志愿导师
        self.second_choice_mentor = second_choice_mentor  # 第二志愿导师
        self.third_choice_mentor = third_choice_mentor  # 第三志愿导师
        self.research_direction = research_direction  # 拟报研究方向
        self.accepts_direction_adjustment = accepts_direction_adjustment  # 是否接受方向调整
        self.direction_adjustment_order = direction_adjustment_order  # 其他方向调整优先顺序
        self.signature = signature  # 考生签名确认

    def __repr__(self):
        return f"InterviewCandidate(candidate_id={self.candidate_id}, student_id={self.student_id}, student_name={self.student_name}, gender={self.gender}, " \
               f"candidate_type={self.candidate_type}, graduation_school={self.graduation_school}, major={self.major}, " \
               f"contact_phone={self.contact_phone}, emergency_contact_phone={self.emergency_contact_phone}, " \
               f"first_choice_mentor={self.first_choice_mentor}, second_choice_mentor={self.second_choice_mentor}, " \
               f"third_choice_mentor={self.third_choice_mentor}, research_direction={self.research_direction}, " \
               f"accepts_direction_adjustment={self.accepts_direction_adjustment}, direction_adjustment_order={self.direction_adjustment_order}, " \
               f"signature={self.signature})"


class InterviewScore:
    def __init__(self, score_id, student_id, interview_time, interview_location, foreign_language_score, professional_knowledge_score, comprehensive_ability_score, interview_total_score, interview_evaluation, interview_group_members, proposed_mentor_signatures):
        self.score_id = score_id  # 成绩ID
        self.student_id = student_id  # 学生ID
        self.interview_time = interview_time  # 复试时间
        self.interview_location = interview_location  # 复试地点
        self.foreign_language_score = foreign_language_score  # 外语分数
        self.professional_knowledge_score = professional_knowledge_score  # 专业知识分数
        self.comprehensive_ability_score = comprehensive_ability_score  # 综合能力分数
        self.interview_total_score = interview_total_score  # 复试总成绩
        self.interview_evaluation = interview_evaluation  # 复试评价
        self.interview_group_members = interview_group_members  # 复试小组成员
        self.proposed_mentor_signatures = proposed_mentor_signatures  # 拟录取导师签字

    def __repr__(self):
        return f"InterviewScore(score_id={self.score_id}, student_id={self.student_id}, interview_time={self.interview_time}, " \
               f"interview_location={self.interview_location}, foreign_language_score={self.foreign_language_score}, " \
               f"professional_knowledge_score={self.professional_knowledge_score}, comprehensive_ability_score={self.comprehensive_ability_score}, " \
               f"interview_total_score={self.interview_total_score}, interview_evaluation={self.interview_evaluation}, " \
               f"interview_group_members={self.interview_group_members}, proposed_mentor_signatures={self.proposed_mentor_signatures})"

import pyodbc

class DBConnection:
    @staticmethod
    def get_connection():
        # 配置 SQL Server 连接字符串
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=keshe;'  # 你的数据库名称
            'UID=sa;'           # SQL Server 用户名
            'PWD=123456'        # SQL Server 密码
        )
        connection = pyodbc.connect(connection_string)
        return connection
