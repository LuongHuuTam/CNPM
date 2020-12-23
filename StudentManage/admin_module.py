from StudentManage import admin, db
from StudentManage.Models import Scores, Subject, Test, Student, Class, Rule, Account
from flask_admin.contrib.sqla import ModelView
from flask import redirect, render_template
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user


class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class StudentModelView(BaseModelView):
    pass


class SubjectModelView(BaseModelView):
    pass


class TestModelView(BaseModelView):
    pass


class AccountModelView(BaseModelView):
    column_exclude_list = ('password', )
    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatisticView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/statistic.html')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AccountModelView(Account, db.session))
admin.add_view(BaseModelView(Class, db.session))
admin.add_view(StudentModelView(Student, db.session))
admin.add_view(SubjectModelView(Subject, db.session))
admin.add_view(TestModelView(Test, db.session))
admin.add_view(BaseModelView(Scores, db.session))
admin.add_view(BaseModelView(Rule, db.session))
admin.add_view(StatisticView(name="Statistic"))
admin.add_view(LogoutView(name="Logout"))

