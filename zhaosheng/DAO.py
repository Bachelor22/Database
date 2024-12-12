import sqlite3

import pyodbc

from Class import DBConnection
from Class import User

class UserDAO:
    def __init__(self):
        self.connection = DBConnection.get_connection()

    # 注册功能：将用户数据插入到数据库
    def add_user(self, user):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO users (username, password, email, phone)
            VALUES (?, ?, ?, ?)
        """, (user.username, user.password, user.email, user.phone))
        self.connection.commit()

    # 登录功能：通过用户名和密码检查用户是否存在
    def get_user_by_username_and_password(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password = ?
        """, (username, password))
        user = cursor.fetchone()
        return user  # 如果没有找到用户，返回 None
class StudentDAO:
    def __init__(self):
        self.connection = DBConnection.get_connection()

    def add_student(self, student):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO students (name, dob, id_card_number, source_location, undergraduate_major, email, phone, undergraduate_school, school_type, resume, preliminary_scores, interview_scores)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student.name,
            student.dob,
            student.id_card_number,
            student.source_location,
            student.undergraduate_major,
            student.email,
            student.phone,
            student.undergraduate_school,
            student.school_type,
            student.resume,
            student.preliminary_scores if student.preliminary_scores is not None else None,  # 如果成绩为None, 传入NULL
            student.interview_scores if student.interview_scores is not None else None  # 同上
        ))

        self.connection.commit()
        print("学生信息已提交到数据库")

    # 添加成绩到 interview_scores 表
    def add_interview_score(self, student_id, foreign_language_score, professional_knowledge_score,
                            comprehensive_ability_score, total_score, interview_time, interview_location,
                            interview_evaluation, interview_group_members, proposed_mentor_signatures):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO interview_scores 
            (student_id, foreign_language_score, professional_knowledge_score, 
             comprehensive_ability_score, interview_total_score, interview_time, 
             interview_location, interview_evaluation, interview_group_members, 
             proposed_mentor_signatures)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id, foreign_language_score, professional_knowledge_score,
            comprehensive_ability_score, total_score, interview_time, interview_location,
            interview_evaluation, interview_group_members, proposed_mentor_signatures
        ))
        self.connection.commit()

    def update_admission_status(self, student_id, admission_status):
        cursor = self.connection.cursor()

        # 确保录取状态值是有效的
        if admission_status not in ["已录取", "未录取"]:
            raise ValueError("录取状态必须是 '已录取' 或 '未录取'")

        # 更新录取状态
        cursor.execute("""
            UPDATE students
            SET admission_status = ?
            WHERE student_id = ?
        """, (admission_status, student_id))

        self.connection.commit()
        print(f"学生ID {student_id} 的录取状态已更新为 {admission_status}！")

    # 获取所有学生的基本信息
    def get_all_students(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT student_id, name FROM students")  # 只选择学生ID和姓名
        rows = cursor.fetchall()
        return rows  # 返回所有学生的信息

    # 根据学生ID获取学生信息（详细信息）
    def get_student_by_id(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT student_id, name, dob, id_card_number, source_location, undergraduate_major, email, phone, undergraduate_school, school_type, resume, preliminary_scores, interview_scores FROM students WHERE student_id = ?", (student_id,))
        student_info = cursor.fetchone()  # 获取单个学生的信息
        return student_info  # 返回学生信息，如果没有找到则返回None

    def update_student(self, student_id, student):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE students SET name = ?, dob = ?, id_card_number = ?, source_location = ?, undergraduate_major = ?, email = ?, phone = ?, undergraduate_school = ?, school_type = ?, resume = ?, preliminary_scores = ?, interview_scores = ?
            WHERE student_id = ?
        """, (student.name, student.dob, student.id_card_number, student.source_location, student.undergraduate_major,
              student.email, student.phone, student.undergraduate_school, student.school_type, student.resume,
              student.preliminary_scores, student.interview_scores, student_id))
        self.connection.commit()

    def delete_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.connection.commit()

    def update_student_scores(self, student_id, preliminary_scores, interview_scores):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE students
            SET preliminary_scores = ?, interview_scores = ?
            WHERE student_id = ?
        """, (preliminary_scores, interview_scores, student_id))
        self.connection.commit()

class MentorDAO:
    def __init__(self):
        self.connection = DBConnection.get_connection()

    def add_mentor(self, mentor):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO subject_mentors (mentor_name, mentor_title, mentor_photo, mentor_bio, mentor_email, mentor_phone, subject_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (mentor.mentor_name, mentor.mentor_title, mentor.mentor_photo, mentor.mentor_bio, mentor.mentor_email, mentor.mentor_phone, mentor.subject_id))
        self.connection.commit()

    def get_mentor_by_id(self, mentor_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM subject_mentors WHERE mentor_id = ?", (mentor_id,))
        return cursor.fetchone()

    def update_mentor(self, mentor_id, mentor):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE subject_mentors SET mentor_name = ?, mentor_title = ?, mentor_photo = ?, mentor_bio = ?, mentor_email = ?, mentor_phone = ?, subject_id = ?
            WHERE mentor_id = ?
        """, (mentor.mentor_name, mentor.mentor_title, mentor.mentor_photo, mentor.mentor_bio, mentor.mentor_email, mentor.mentor_phone, mentor.subject_id, mentor_id))
        self.connection.commit()

    def delete_mentor(self, mentor_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM subject_mentors WHERE mentor_id = ?", (mentor_id,))
        self.connection.commit()

class InterviewCandidateDAO:
    def __init__(self):
        self.connection = DBConnection.get_connection()

    # 插入学生志愿信息
    def add_interview_candidate(self, student_id, gender, candidate_type, graduation_school, major,
                                contact_phone, emergency_contact_phone, first_choice_mentor,
                                second_choice_mentor, third_choice_mentor, research_direction,
                                accepts_direction_adjustment, direction_adjustment_order, signature, student_name):
        try:
            # 确保数据库连接是成功的
            cursor = self.connection.cursor()

            # 构建 SQL 插入语句，使用正确的表名
            sql = """
            INSERT INTO interview_candidates (student_id, gender, candidate_type, graduation_school, major, 
                                             contact_phone, emergency_contact_phone, first_choice_mentor, 
                                             second_choice_mentor, third_choice_mentor, research_direction, 
                                             accepts_direction_adjustment, direction_adjustment_order, signature, student_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # 执行 SQL 语句
            cursor.execute(sql, (student_id, gender, candidate_type, graduation_school, major,
                                 contact_phone, emergency_contact_phone, first_choice_mentor,
                                 second_choice_mentor, third_choice_mentor, research_direction,
                                 accepts_direction_adjustment, direction_adjustment_order, signature, student_name))

            # 提交事务
            self.connection.commit()
            print("志愿信息已成功提交到数据库！")

        except pyodbc.Error as e:
            print(f"数据库操作失败: {e}")
        finally:
            cursor.close()


class AdminDAO:
    def __init__(self):
        self.connection = DBConnection.get_connection()

    def get_admin_by_username(self, username):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
            admin = cursor.fetchone()  # 返回找到的管理员记录，如果没有找到返回 None
            return admin
        except sqlite3.Error as e:
            print("数据库查询出错:", e)
            return None

    def admin_login(self, username, password):
        # 查询管理员信息
        admin = self.get_admin_by_username(username)

        if admin:
            # 假设数据库表中的密码字段是 admin[2]
            stored_password = admin[2]

            # 如果数据库中的密码和输入的密码相同，则登录成功
            if stored_password == password:
                print("登录成功！")
                return True
            else:
                print("密码错误！")
                return False
        else:
            print("用户名不存在！")
            return False