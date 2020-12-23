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
    def __init__(self, id, firstname, lastname, subject, classes):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.sub = subject
        self.classes = classes


def get_user_byID(id):
    return Account.query.filter(Account.id == id).first()


def getuser(username, password):
    return Account.query.filter(Account.username == username.strip(), Account.password == password).first()


def get_teacher():
    return Account.query.filter(Account.admin == 0).all()


def get_all_student():
    return Student.query.order_by(Student.class_id).all()


def Age(birthday):
    date_format = "%Y-%m-%d"
    age = date.today().year - datetime.strptime(birthday, date_format).year
    return age


def get_class10_first():
    return Class.query.filter(Class.grade == '10').first()


def get_student_in_class(id):
    return Student.query.filter(Student.class_id == id).order_by(Student.lastname).all()


def get_student(name):
    return Student.query.filter(Student.fullname.contains(name)).order_by(Student.class_id).all()


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
        x = i.grade + 'A' + i.name
        classes += x + ' '
    return InfoTeacher(id, acc.firstname, acc.lastname, acc.subject, classes)


def get_all_scores(stu_id, semester):
    student = get_student_byid(stu_id)
    sub = Subject.query.all()
    res = []
    for s in sub:
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
        temp = AllScoresStudent(student.fullname, subject, scores_15.strip(), scores_1h.strip(), scores_final.strip(),
                                scores_avg.strip())
        res.append(temp)
    return res
