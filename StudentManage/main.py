import hashlib

from flask import request, flash, json, jsonify
from flask_login import login_user

from StudentManage import app, login
from StudentManage.Controller import *


@app.route('/')
def index():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            return redirect('/manage')
        else:
            return redirect('/teacher')
    search = request.args.get('search')
    if search == None or search == '' or search == ' ':
        res = None
    else:
        res = get_student(search)
    return render_template('index.html', res=res, search=search)


@app.route('/view-scores/<id>')
def viewscores(id):
    semester = request.args.get('semester')
    if semester == None:
        semester = 1
    res = get_all_scores(id, semester)
    avg = 0
    avg_all = 0
    if semester == '2':
        avg = get_avg_semester(id, 2)
        avg_all = get_avg_full_course(id)

    else:
        avg = get_avg_semester(id, 1)

    return render_template('viewscores.html', res=res, semester=semester, avg=avg, avg_all=avg_all)


@login.user_loader
def user_loader(user_id):
    return Account.query.get(user_id)


@app.route('/login-admin', methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        user = getuser(username, password)
        if user and user.admin == 1:
            login_user(user=user)

    return redirect('/admin')


@app.route('/login', methods=["post", "get"])
def login():
    if request.method == "GET":
        flash('')
        return render_template('login.html')
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        user = Account.query.filter(Account.username == username.strip(), Account.password == password).first()
        if user and user.admin == 1:
            login_user(user=user)
            return redirect('/manage')
        elif user and user.admin == 0:
            login_user(user=user)
            return redirect('/teacher')
        else:
            flash('Tài khoản hoặc mật khẩu sai')
            return redirect('/login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/statistic-admin', methods=['GET'])
def data_statistic():
    labels = ['2015', '2016', '2017', '2018', '2019', '2020']
    data = [98, 99, 100, 99, 98, 100]
    return json.dumps({'labels': labels, 'data': data})


@app.route('/manage')
def manage():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            return redirect('/manage/student')
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/manage/student')
def managestudent():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            search = request.args.get("search")
            if search == None:
                student = get_all_student()
                return render_template('manageStudent.html', ac=1, student=student, search=search)
            student = get_student(search)
            return render_template('manageStudent.html', ac=1, student=student, search=search)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/manage/student/add', methods=["post", "get"])
def addstudent():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            cl = get_class_to_add_student()
            if request.method == "GET":
                return render_template('addStudent.html', ac=1, student=None, cl=cl)
            if request.method == "POST":
                birthday = request.form.get("birthday")
                age = Age(birthday)
                minAge = get_min_age()
                maxAge = get_max_age()
                student = Student(
                    firstname=request.form.get("firstname").title(),
                    lastname=request.form.get("lastname").title(),
                    fullname=request.form.get("firstname").title() + ' ' + request.form.get("lastname").title(),
                    male=request.form.get("sex"),
                    birthday=birthday,
                    address=request.form.get("address"),
                    email=request.form.get("email"),
                    class_id=request.form.get("class")
                )
                if age >= minAge and age <= maxAge:
                    db.session.add(student)
                    db.session.commit()
                    flash('Thêm thành công')
                    return render_template('addStudent.html', ac=1, student=None, cl=cl)
                else:
                    flash('Tuổi phải từ ' + str(minAge) + ' đến ' + str(maxAge))
                    return render_template('addStudent.html', ac=1, student=student, cl=cl)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')


    else:
        return redirect('/login')


@app.route('/manage/student/edit<id>', methods=["post", "get"])
def editStudent(id):
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            student = Student.query.get(id)
            cl = get_class_to_add_student()
            if request.method == "GET":
                return render_template('editStudent.html', ac=1, student=student, cl=cl)
            if request.method == "POST":
                birthday = request.form.get("birthday")
                age = Age(birthday)
                minAge = get_min_age()
                maxAge = get_max_age()
                if age >= minAge and age <= maxAge:
                    student.firstname = request.form.get("firstname").title()
                    student.lastname = request.form.get("lastname").title()
                    student.fullname = request.form.get("firstname").title() + ' ' + request.form.get("lastname").title(),
                    student.male = request.form.get("sex")
                    student.birthday = birthday
                    student.address = request.form.get("address")
                    student.email = request.form.get("email")
                    student.class_id = request.form.get("class")
                    db.session.commit()
                    flash('Sửa thành công')
                    return redirect('/manage/student')
                else:
                    flash('Tuổi phải từ ' + str(minAge) + ' đến ' + str(maxAge))
                    return render_template('editStudent.html', ac=1, student=student, cl=cl)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')


    else:
        return redirect('/login')


@app.route('/manage/teacher')
def manageteacher():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            teacher = get_teacher()
            res = []
            for i in teacher:
                temp = get_info_teacher(i.id)
                res.append(temp)
            return render_template('manageTeacher.html', ac=2, teacher=res)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/manage/teacher/edit<id>', methods=['get', 'post'])
def editClassTeach(id):
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            if request.method == 'GET':
                cl = get_all_class()
                teach = get_class_teach(id)
                return render_template('editTeacher.html', ac=2, cl=cl, id=id, teach=teach)
            if request.method == 'POST':
                i = request.form.getlist('class')
                temp = Teach.query.filter(Teach.teacher_id == id).all()
                for x in temp:
                    db.session.delete(x)
                db.session.commit()
                for j in i:
                    n = Teach(
                        teacher_id=id,
                        class_id=j
                    )
                    db.session.add(n)
                db.session.commit()
                return redirect('/manage/teacher')
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/manage/teacher/add', methods=["post", "get"])
def addteacher():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            sub = Subject.query.all()
            if request.method == "GET":
                return render_template('addTeacher.html', ac=2, sub=sub, acc=None)
            if request.method == "POST":
                acc = Account(
                    username=request.form.get('username'),
                    password=hashlib.md5(request.form.get('password').strip().encode("utf-8")).hexdigest(),
                    firstname=request.form.get('firstname').title(),
                    lastname=request.form.get('lastname').title(),
                    admin=0,
                    active=1,
                    subject_id=request.form.get('subject')
                )
                temp = Account.query.filter(Account.username == acc.username).first()
                if temp:
                    flash('Tên đăng nhập đã được sử dụng')
                    return render_template('addTeacher.html', ac=2, sub=sub, acc=acc)
                db.session.add(acc)
                db.session.commit()
                return redirect('/manage/teacher')
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/manage/class')
def manageclass():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            cl = get_all_class()
            i = get_class10_first()
            student = Student.query.filter(Student.class_id == i.id).order_by(Student.lastname).all()
            count = len(student)
            return render_template('manageClass.html', ac=3, cl=cl, count=count, i=i.id, student=student,
                                   course=cl[0].course)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/manage/class/<id>', methods=["get"])
def manageclassID(id):
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            if id == '1':
                return redirect('/manage/class')
            cl = get_all_class()
            if id == '-1':
                student = get_student_in_class(None)
                count = len(student)
                return render_template('manageClass.html', ac=3, cl=cl, i=id, count=count, student=student,
                                       course=cl[0].course)
            student = get_student_in_class(id)
            count = len(student)
            return render_template('manageClass.html', ac=3, cl=cl, i=id, count=count, student=student,
                                   course=cl[0].course)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/drawReportSubject')
def drawReportSubject():
    subject = request.args.get('subject')
    semester = request.args.get('semester')
    report = report_subject(subject, semester)
    labels = []
    data = []
    for i in report:
        labels.append(str(i.cl))
        data.append(i.rate)
    return json.dumps({'labels': labels, 'data': data})


@app.route('/manage/reportsubject')
def reportsubject():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            sub = Subject.query.all()
            subject = request.args.get('subject')
            semester = request.args.get('semester')
            if subject == None:
                subject = 1
            if semester == None:
                semester = 1
            report = report_subject(subject, semester)
            return render_template('reportSubject.html', ac=4, sub=sub, report=report, subject=subject,
                                   semester=semester)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/drawReportSemester')
def drawReportSemester():
    semester = request.args.get('semester')
    report = report_semester(semester)
    labels = []
    data = []
    for i in report:
        labels.append(str(i.cl))
        data.append(i.rate)
    return json.dumps({'labels': labels, 'data': data})


@app.route('/manage/reportyear')
def reportyear():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            sub = Subject.query.all()
            semester = request.args.get('semester')
            if semester == None:
                semester = 1
            report = report_semester(semester)
            return render_template('reportYear.html', ac=4, sub=sub, report=report, semester=semester)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/manage/rule')
def managerule():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            rule = get_all_rule()
            return render_template('manageRule.html', ac=5, rule=rule)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/manage/rule/edit<id>', methods=["post", "get"])
def editRule(id):
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 1:
            rule = Rule.query.get(id)
            if request.method == "GET":
                return render_template('editRule.html', ac=5, rule=rule)
            if request.method == "POST":
                rule.value = request.form.get('value')
                db.session.commit()
                flash('Sửa thành công')
                return redirect('/manage/rule')

        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')


    else:
        return redirect('/login')


@app.route('/changePassword', methods=['post'])
def changePassword():
    user = get_user_byID(current_user.get_id())
    oldpassword = request.form.get('oldpass')
    if hashlib.md5(oldpassword.strip().encode("utf-8")).hexdigest() != user.password:
        return jsonify('false')
    password = request.form.get('newpass')
    user.password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    db.session.commit()
    return jsonify('true')


@app.route('/teacher')
def teacher():
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 0:
            cl = get_class_teach(user.id)
            return render_template('teacher.html', cl=cl)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/teacher/class<id>')
def teach(id):
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 0:
            semester = request.args.get('semester')
            if semester == None:
                semester = 1
            cl = get_class_teach(user.id)
            student = get_student_in_class(id)
            sub = Subject.query.get(user.subject_id)
            res = []
            for i in student:
                temp = get_scores_student_in_sub(sub_id=sub.id, stu_id=i.id, semester=semester)
                res.append(temp)
            return render_template('teacherClass.html', cl=cl, scores=res, sub=sub, ac=id, semester=semester)
        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


@app.route('/teacher/scores/<stu_id>ki<semester>', methods=["post", "get"])
def editoraddscores(stu_id, semester):
    if current_user.is_authenticated:
        user = get_user_byID(current_user.get_id())
        if user.admin == 0:
            cl = get_class_teach(user.id)
            student = get_student_byid(stu_id)
            if request.method == 'GET':
                res = get_scores_student_in_sub(sub_id=user.subject_id, stu_id=student.id, semester=semester)
                return render_template('teacherScores.html', cl=cl, scores=res, ac=student.class_id, semester=semester)
            if request.method == 'POST':
                sc_15 = request.form.get('scores_15').strip()
                sc_1h = request.form.get('scores_1h').strip()
                sc_final = request.form.get('scores_final').strip()
                if sc_15 == '' or sc_1h == '' or sc_final == '':
                    flash('Vui lòng nhập đủ thông tin')
                    res = get_scores_student_in_sub(sub_id=user.subject_id, stu_id=student.id, semester=semester)
                    res.scores_15 = sc_15
                    res.scores_1h = sc_1h
                    res.scores_final = sc_final
                    return render_template('teacherScores.html', cl=cl, scores=res, ac=student.class_id,
                                           semester=semester)
                scores_15 = sc_15.split(' ')
                scores_1h = sc_1h.split(' ')
                scores_final = sc_final.split(' ')
                all_scores = get_scores_in_sub(user.subject_id, stu_id, semester)
                sum = 0
                count = 0
                # Thêm điểm
                if len(all_scores) != 0:
                    for i in all_scores:
                        db.session.delete(i)
                db.session.commit()
                for x in scores_15:
                    if x != '':
                        res = Scores(
                            student_id=stu_id,
                            subject_id=user.subject_id,
                            test_id=1,
                            scores=float(x),
                            semester=semester
                        )
                        sum += float(x)
                        count += 1
                        db.session.add(res)
                for x in scores_1h:
                    if x != '':
                        res = Scores(
                            student_id=stu_id,
                            subject_id=user.subject_id,
                            test_id=2,
                            scores=float(x),
                            semester=semester
                        )
                        sum += (float(x) * 2)
                        count += 2
                        db.session.add(res)
                for x in scores_final:
                    if x != '':
                        res = Scores(
                            student_id=stu_id,
                            subject_id=user.subject_id,
                            test_id=3,
                            scores=float(x),
                            semester=semester
                        )
                        sum += (float(x) * 3)
                        count += 3
                        db.session.add(res)
                res = Scores(
                    student_id=stu_id,
                    subject_id=user.subject_id,
                    test_id=4,
                    scores=round(sum / count, 1),
                    semester=semester
                )
                db.session.add(res)
                db.session.commit()
                return redirect('/teacher/class' + str(student.class_id) + '?semester=' + str(semester))

        else:
            flash('Tài khoản của bạn không có quyền truy cập')
            return redirect('/login')

    else:
        return redirect('/login')


if __name__ == '__main__':
    classes_append()
    from StudentManage.admin_module import *

    get_class_to_add_student()
    app.run(debug=True, port=8888)
