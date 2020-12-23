from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey, Enum, or_
from sqlalchemy.orm import relationship
from StudentManage import db
from datetime import datetime
from flask_login import UserMixin


class Subject(db.Model):
    __tablename__ = 'Subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    Account = relationship('Account', backref='subject', lazy=True)
    scores = relationship('Scores', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class Account(db.Model, UserMixin):
    __tablename__ = 'Account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    subject_id = Column(Integer, ForeignKey(Subject.id))

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Test(db.Model):
    __tablename__ = 'Test'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    scores = relationship('Scores', backref='test', lazy=True)

    def __str__(self):
        return self.name


class Class(db.Model):
    __tablename__ = 'Class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course = Column(Integer, nullable=False)
    grade = Column(Enum('10', '11', '12'))
    name = Column(String(10), nullable=False)
    students = relationship('Student', backref='class', lazy=True)

    def __str__(self):
        return self.grade + 'A' + self.name


class Teach(db.Model):
    teacher_id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    class_id = Column(Integer, ForeignKey(Class.id), primary_key=True)


class Student(db.Model):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    fullname = Column(String(200), nullable=False)
    male = Column(Enum('Male', 'Female'))
    birthday = Column(Date)
    address = Column(String(100))
    email = Column(String(100))
    class_id = Column(Integer, ForeignKey(Class.id))
    scores = relationship('Scores', backref='student', lazy=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Scores(db.Model):
    __tablename__ = 'Scores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    test_id = Column(Integer, ForeignKey(Test.id), nullable=False)
    scores = Column(Float, nullable=False)
    semester = Column(Enum('1', '2'))
    date_create = Column(Date, default=datetime.now())


class Rule(db.Model):
    __tablename__ = 'regulation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    value = Column(Integer, nullable=False)


if __name__ == '__main__':
    db.create_all()
