from werkzeug.security import check_password_hash

from Connection import DBConnection
from zhaosheng.Class import Student, User
from zhaosheng.DAO import StudentDAO, UserDAO, InterviewCandidateDAO, AdminDAO
from flask import Flask, render_template, request, redirect, url_for, session
import os
from flask import flash, redirect, url_for, render_template, request


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/index')
def index():
    # 从 session 获取当前登录的用户名
    user_name = session.get('username')  # 获取存储在 session 中的用户名

    if user_name:
        # 渲染主页，传递用户名
        return render_template('index.html', user_name=user_name)
    else:
        return redirect(url_for('login'))  # 如果没有登录，跳转到登录页


# 获取所有学科信息并渲染 HTML 页面
@app.route('/subjects')
def subjects():
    conn = DBConnection.get_connection()  # 使用 DBConnection 类获取连接
    cursor = conn.cursor()
    cursor.execute("SELECT subject_id, subject_name, subject_level, subject_description, subject_type FROM subjects")
    subjects = cursor.fetchall()
    conn.close()

    # 将学科信息传递给模板渲染
    return render_template('subjects.html', subjects=subjects)


# 获取指定学科的导师信息并渲染页面
@app.route('/mentors/<int:subject_id>', methods=['GET'])
def mentors(subject_id):
    conn = DBConnection.get_connection()  # 使用 DBConnection 类获取连接
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mentor_id, mentor_name, mentor_title, mentor_photo, mentor_bio, mentor_email, mentor_phone
        FROM subject_mentors
        WHERE subject_id = ?
    """, (subject_id,))
    mentors = cursor.fetchall()
    conn.close()

    return render_template('mentors.html', mentors=mentors, subject_id=subject_id)


# 注册用户
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        user = User(username, password, email, phone)
        user_dao = UserDAO()
        user_dao.add_user(user)

        return redirect(url_for('login'))
    return render_template('register.html')


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_dao = UserDAO()
        user = user_dao.get_user_by_username_and_password(username, password)

        if user:
            # 登录成功后将用户名存入 session
            session['username'] = username
            # 登录成功后跳转到主页
            return redirect(url_for('index'))
        else:
            return "登录失败！"

    return render_template('login.html')



# 学生注册
@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        id_card_number = request.form['id_card_number']
        source_location = request.form['source_location']
        undergraduate_major = request.form['undergraduate_major']
        email = request.form['email']
        phone = request.form['phone']
        undergraduate_school = request.form['undergraduate_school']
        school_type = request.form['school_type']
        resume = request.form['resume']
        preliminary_scores = request.form['preliminary_scores']
        interview_scores = request.form['interview_scores']

        student = Student(name, dob, id_card_number, source_location, undergraduate_major, email, phone,
                          undergraduate_school, school_type, resume, preliminary_scores, interview_scores)

        student_dao = StudentDAO()
        student_dao.add_student(student)

        return redirect(url_for('dashboard'))

    return render_template('student_register.html')


@app.route('/submit_volunteer', methods=['GET', 'POST'])
def submit_volunteer():
    if request.method == 'POST':
        # 获取表单数据
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        gender = request.form['gender']
        candidate_type = request.form['candidate_type']
        graduation_school = request.form['graduation_school']
        major = request.form.get('major', None)  # major 是可选字段

        # 获取额外字段（根据报考类型的不同，字段值可能为 None 或空）
        research_direction = request.form.get('research_direction') if candidate_type == 'Computer Science' else None
        accepts_direction_adjustment = request.form.get('accepts_direction_adjustment') if candidate_type == 'Electronic Engineering' else None
        direction_adjustment_order = request.form.get('direction_adjustment_order') if candidate_type == 'Electronic Engineering' else None

        contact_phone = request.form['contact_phone']
        emergency_contact_phone = request.form['emergency_contact_phone']
        first_choice_mentor = request.form['first_choice_mentor']
        second_choice_mentor = request.form['second_choice_mentor']
        third_choice_mentor = request.form['third_choice_mentor']
        signature = request.form['signature']

        # 如果报考类型为“其他”，则处理自定义报考类型字段
        candidate_type_other = request.form.get('candidate_type_other') if candidate_type == 'Other' else None

        # 创建 InterviewCandidateDAO 实例
        interview_candidate_dao = InterviewCandidateDAO()

        try:
            # 插入数据，具体字段根据报考类型处理
            interview_candidate_dao.add_interview_candidate(
                student_id, gender, candidate_type, graduation_school, major,
                contact_phone, emergency_contact_phone,
                first_choice_mentor, second_choice_mentor, third_choice_mentor,
                research_direction, accepts_direction_adjustment,
                direction_adjustment_order, signature, student_name
            )

            # 提交成功，跳转到成功页面
            return redirect(url_for('success'))

        except Exception as e:
            # 如果出现错误，输出错误信息并返回表单页面
            print(f"错误: {e}")
            return redirect(url_for('submit_volunteer'))  # 可以改为传递错误信息显示给用户

    # GET 请求时渲染表单页面
    return render_template('submit_volunteer_form.html')

@app.route('/success')
def success():
    return render_template('success.html')  # 渲染成功页面


# 显示学生信息并提供修改功能
@app.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    dao = StudentDAO()
    student_info = dao.get_student_by_id(student_id)  # 获取学生的详细信息
    if student_info is None:
        return "学生信息未找到", 404

    # 如果是POST请求，更新学生信息
    if request.method == 'POST':
        # 获取表单提交的数据
        name = request.form['name']
        dob = request.form['dob']
        id_card_number = request.form['id_card_number']
        source_location = request.form['source_location']
        undergraduate_major = request.form['undergraduate_major']
        email = request.form['email']
        phone = request.form['phone']
        undergraduate_school = request.form['undergraduate_school']
        school_type = request.form['school_type']
        resume = request.form['resume']
        preliminary_scores = request.form['preliminary_scores']
        interview_scores = request.form['interview_scores']
        admission_status = request.form['admission_status']

        # 更新学生信息
        student = Student(
            name, dob, id_card_number, source_location, undergraduate_major,
            email, phone, undergraduate_school, school_type, resume,
            preliminary_scores, interview_scores
        )
        dao.update_student(student_id, student)  # 更新学生的基本信息

        # 更新成绩
        dao.update_student_scores(student_id, preliminary_scores, interview_scores)  # 更新成绩

        # 更新录取状态
        dao.update_admission_status(student_id, admission_status)  # 更新录取状态

        return redirect(url_for('students'))  # 更新后返回学生列表页面

    return render_template('update_student.html', student_info=student_info)

# 获取学生列表
@app.route('/students')
def students():
    dao = StudentDAO()
    students = dao.get_all_students()  # 获取所有学生的信息
    return render_template('students.html', students=students)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 创建 AdminDAO 实例
        admin_dao = AdminDAO()

        # 检查管理员登录
        admin = admin_dao.get_admin_by_username(username)

        if admin:
            # 比较密码，直接用数据库中存储的密码进行对比
            if admin[2] == password:  # admin[2] 是数据库中存储的密码字段
                flash("登录成功！", "success")
                return redirect(url_for('students'))  # 登录成功后跳转到学生管理页面
            else:
                flash("密码错误！", "danger")  # 使用 flash 返回错误消息
        else:
            flash("用户名不存在！", "danger")  # 使用 flash 返回错误消息

    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)
