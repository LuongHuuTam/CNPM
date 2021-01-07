from StudentManage.Models import *
from datetime import date


class StudentScores:
    def __init__(self, id, firstname, lastname, birthday, scores_15, scores_1h, scores_final, avg_scores):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.scores_15 = scores_15
        self.scores_1h = scores_1h
        self.scores_final = scores_final
        self.avg_scores = avg_scores


class AllScoresStudent:
    def __init__(self, fullname, subject, scores_15, scores_1h, scores_final, avg_scores):
        self.fullname = fullname
        self.subject = subject
        self.scores_15 = scores_15
        self.scores_1h = scores_1h
        self.scores_final = scores_final
        self.avg_scores = avg_scores


class InfoTeacher:
    def __init__(self, id, username, firstname, lastname, subject, classes):
        self.id = id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.sub = subject
        self.classes = classes


class ReportSubject:
    def __init__(self, cl, amount, countpass, rate):
        self.cl = cl
        self.amount = amount
        self.countpass = countpass
        self.rate = rate


def get_min_age():
    res = Rule.query.filter(Rule.name == 'MinAge').first()
    return int(res.value)


def get_max_age():
    res = Rule.query.filter(Rule.name == 'MaxAge').first()
    return int(res.value)


def get_population():
    res = Rule.query.filter(Rule.name == 'MaxPopulation').first()
    return int(res.value)


def check_class_id(id,list_class):
    for i in list_class:
        if i.id == id:
            return True
    return False



def get_class_to_add_student():
    max = get_population()
    res = []
    b = db.session.query(Class).join(Student).group_by(Class.id).having(func.count(Student.class_id) >= max).all()
    temp = get_all_class()
    for i in temp:
        if check_class_id(i.id,b) == False:
            res.append(i)

    return res


def get_user_byID(id):
    return Account.query.filter(Account.id == id).first()


def get_all_class():
    return Class.query.order_by(Class.grade, Class.name).all()


def getuser(username, password):
    return Account.query.filter(Account.username == username.strip(), Account.password == password).first()


def get_teacher():
    return Account.query.filter(Account.admin == 0).all()


def get_all_student():
    return Student.query.order_by(Student.class_id, Student.lastname).all()


def Age(birthday):
    date_format = "%Y-%m-%d"
    age = date.today().year - datetime.strptime(birthday, date_format).year
    return age


def get_class10_first():
    return Class.query.filter(Class.grade == '10').first()


def get_student_in_class(id):
    return Student.query.filter(Student.class_id == id).order_by(Student.lastname).all()


def get_student(name):
    return Student.query.filter(Student.fullname.contains(name)).order_by(Student.class_id, Student.lastname).all()


def get_student_byid(id):
    return Student.query.get(id)


def get_all_rule():
    return Rule.query.all()


def get_class_teach(id):
    temp = Teach.query.filter(Teach.teacher_id == id).all()
    res = []
    for x in temp:
        i = Class.query.get(x.class_id)
        res.append(i)
    return res


def get_scores_student_in_sub(sub_id, stu_id, semester):
    student = get_student_byid(stu_id)
    scores = Scores.query.filter(Scores.subject_id == sub_id, Scores.student_id == stu_id,
                                 Scores.semester == semester).all()
    scores_15 = ''
    scores_1h = ''
    scores_final = ''
    scores_avg = ''
    for i in scores:
        if i.test_id == 1:
            scores_15 += str(i.scores) + ' '
        if i.test_id == 2:
            scores_1h += str(i.scores) + ' '
        if i.test_id == 3:
            scores_final += str(i.scores) + ' '
        if i.test_id == 4:
            scores_avg += str(i.scores) + ' '
    res = StudentScores(student.id, student.firstname, student.lastname, student.birthday, scores_15, scores_1h,
                        scores_final,
                        scores_avg)
    return res


def get_scores_in_sub(sub_id, stu_id, semester):
    return Scores.query.filter(Scores.subject_id == sub_id, Scores.student_id == stu_id,
                               Scores.semester == semester).all()


def get_test15(arr):
    res = []
    for i in arr:
        if i.test_id == 1:
            res.append(i)
    return res


def get_test1h(arr):
    res = []
    for i in arr:
        if i.test_id == 2:
            res.append(i)
    return res


def get_testfinal(arr):
    res = []
    for i in arr:
        if i.test_id == 3:
            res.append(i)
    return res


def get_testavg(arr):
    res = []
    for i in arr:
        if i.test_id == 4:
            res.append(i)
    return res


def get_info_teacher(id):
    acc = Account.query.get(id)
    cl = get_class_teach(id)
    classes = ''
    for i in cl:
        x = str(i)
        classes += x + ' '
    return InfoTeacher(id, acc.username, acc.firstname, acc.lastname, acc.subject, classes)


def get_all_scores(stu_id, semester):
    student = get_student_byid(stu_id)
    sub = Subject.query.all()
    res = []
    for s in sub:
        temp = get_scores_detail_in_subject(s.id, stu_id, semester)
        res.append(temp)
    return res


def get_scores_detail_in_subject(sub_id, stu_id, semester):
    s = Subject.query.filter(Subject.id == sub_id).first()
    student = get_student_byid(stu_id)
    scores = Scores.query.filter(Scores.subject_id == s.id, Scores.student_id == stu_id,
                                 Scores.semester == semester).all()
    subject = s.name
    scores_15 = ''
    scores_1h = ''
    scores_final = ''
    scores_avg = ''
    for i in scores:
        if i.test_id == 1:
            scores_15 += str(i.scores) + ' '
        if i.test_id == 2:
            scores_1h += str(i.scores) + ' '
        if i.test_id == 3:
            scores_final += str(i.scores) + ' '
        if i.test_id == 4:
            scores_avg += str(i.scores) + ' '
    return AllScoresStudent(student.fullname, subject, scores_15.strip(), scores_1h.strip(), scores_final.strip(),
                            scores_avg.strip())


def get_avg_full_course(stu_id):
    return round((get_avg_semester(stu_id, 1) + get_avg_semester(stu_id, 2)) / 2, 1)


def get_avg_semester(stu_id, semester):
    res = get_all_scores(stu_id, semester)
    avg = 0
    for i in res:
        temp = 0
        if i.avg_scores != '':
            temp = float(i.avg_scores)
        avg += temp
    avg = round(avg / len(res), 1)
    return avg


def report_subject(sub_id, semester):
    cl = Class.query.all()
    res = []
    for c in cl:
        stu = get_student_in_class(c.id)
        amount = len(stu)
        tempamount = 1
        if amount != 0:
            tempamount = amount
        countpass = 0
        for s in stu:
            temp = get_scores_detail_in_subject(sub_id, s.id, semester)
            if temp.avg_scores == '':
                temp.avg_scores = 0
            if float(temp.avg_scores) >= 5:
                countpass += 1
        resp = ReportSubject(c, amount, countpass, round((countpass / tempamount) * 100, 2))
        res.append(resp)
    return res


def report_semester(semester):
    cl = Class.query.all()
    res = []
    for c in cl:
        stu = get_student_in_class(c.id)
        amount = len(stu)
        tempamount = 1
        if amount != 0:
            tempamount = amount
        countpass = 0
        for s in stu:
            temp = get_avg_semester(s.id, semester)
            if temp >= 5:
                countpass += 1
        resp = ReportSubject(c, amount, countpass, round((countpass / tempamount) * 100, 2))
        res.append(resp)
    return res


def check_class(name, list_class):
    for i in list_class:
        if i.name == name:
            return True
    return False


def classes_append():
    for i in ['10', '11', '12']:
        c = Class.query.filter(Class.grade == i).order_by(Class.name).all()
        constraint = Rule.query.filter(Rule.name == 'Class' + i + 'Amount').first()
        if len(c) != constraint.value:
            for x in range(1, constraint.value + 1):
                if check_class(str(x), c) == False:
                    temp = Class(
                        course=2020,
                        grade=i,
                        name=str(x)
                    )
                    db.session.add(temp)
                    db.session.commit()
