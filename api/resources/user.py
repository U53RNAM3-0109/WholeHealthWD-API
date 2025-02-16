from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser

class UserResource(Resource):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def get(self):
        parser = RequestParser()

        parser.add_argument('detailed', type=bool, location='args')

        detailed = parser.parse_args()['detailed']

        users = self.app.UserModel.query.all()
        data = []
        for user in users:
            child, child_type = get_user_child(self.app, user)
            if detailed:
                new_data = user.to_dict(detailed)
                if child:
                    new_data.update(child.to_dict(detailed))

                data.append(new_data)
            else:
                new_data = user.to_dict()
                if child:
                    new_data["usertype"] = child_type

                data.append(user.to_dict())

        if data:
            return data
        else:
            return {'message': 'No users found'}

    def post(self):
        parser = RequestParser()

        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('usertype', type=str, required=True)

        data = parser.parse_args(strict=False)
        try:
            usertype = data['usertype']
            if usertype == 'Student':
                pass
            elif usertype == 'Teacher':
                pass
            elif usertype == 'Admin':
                parser.add_argument('accessrank', type=str)
            else:
                raise ValueError(f"Usertype {usertype} is not accepted.")

            data = parser.parse_args()

            new_user = self.app.UserModel(
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'],
                password=data['password'])

            if usertype == 'Student':
                print("NEW STUDENT")
                new_student = self.app.StudentModel(
                    user_id=new_user.id,
                )
                self.app.db.session.add(new_user, new_student)

            elif usertype == 'Teacher':
                new_teacher = self.app.StudentModel(
                    user_id=new_user.id,
                )
                self.app.db.session.add(new_user, new_teacher)

            elif usertype == 'Admin':
                new_admin = self.app.AdminModel(
                    user_id=new_user.id,
                    access_rank=data['accessrank']
                )
                self.app.db.session.add(new_user, new_admin)

            else:
                raise ValueError(f"User type {usertype} is not accepted.")
            self.app.db.session.commit()
        except Exception as exc:
            print(exc)
            return "Error occurred, see console"

        if new_user:

            child, child_type = get_user_child(self.app, new_user)
            data = new_user.to_dict(True)
            if child:
                data.update(child.to_dict(True))

            return data
        else:
            return "No new user created"


class SpecifiedUserResource(Resource):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def get(self, user_id):
        user = self.app.db.get_or_404(self.app.UserModel, user_id)

        if user:
            return user.to_dict()
        else:
            return {'message': 'User not found'}

def get_user_child(app, user):

    student = app.StudentModel.query.filter_by(user_id=user.id).first()
    teacher = app.TeacherModel.query.filter_by(user_id=user.id).first()
    admin = app.AdminModel.query.filter_by(user_id=user.id).first()

    if student:
        print(student)
        return student, "student"
    if teacher:
        return teacher, "teacher"
    if admin:
        return admin, "admin"
    return None, None