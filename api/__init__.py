from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

from .models.user_models.user_model import User
from .models.user_models.user_child_models.admin_model import Admin
from .models.user_models.user_child_models.student_model import Student
from .models.user_models.user_child_models.teacher_model import Teacher


from .resources import user

from flask import Flask
from flask_restful import Api


class BtecBytesAPI(Flask):
    api: Api
    db: SQLAlchemy

    def __init__(self, __name__, db_uri):
        super().__init__(__name__)
        self.api = Api(self)
        self.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.db = SQLAlchemy()
        self.db.init_app(self)

        self.define_models()
        self.register_triggers()

        with self.app_context():
            self.db.create_all()

        self.api.add_resource(user.UserResource, "/user", resource_class_kwargs={'app': self})
        self.api.add_resource(user.SpecifiedUserResource, "/user/<user_id>", resource_class_kwargs={'app': self})

        self.api.init_app(self)

    def define_models(self):
        self.UserModel = User(self.db).define_model()
        self.AdminModel = Admin(self.db).define_model()
        self.StudentModel = Student(self.db).define_model()
        self.TeacherModel = Teacher(self.db).define_model()

    def register_triggers(self):
        def prevent_multiple_user_types(mapper, connection, target):
            existing_user = self.db.session.connection().execute(
                "SELECT COUNT(*) FROM admin WHERE user_id = ? UNION ALL "
                "SELECT COUNT(*) FROM student WHERE user_id = ? UNION ALL "
                "SELECT COUNT(*) FROM teacher WHERE user_id = ?",
                (target.user_id, target.user_id, target.user_id)
            ).fetchall()

            if sum([row[0] for row in existing_user]) > 0:
                raise Exception("Attempting to assign a User to multiple roles")

        event.listen(self.AdminModel, 'before_insert', prevent_multiple_user_types)
        event.listen(self.StudentModel, 'before_insert', prevent_multiple_user_types)
        event.listen(self.TeacherModel, 'before_insert', prevent_multiple_user_types)