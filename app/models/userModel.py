from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

# __id__, email, password, firstname, lastname, birthdate, joindate
class UserModel(UserMixin):
    def __init__(self, id, email, firstname, lastname, birthdate, joindate):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.joindate = joindate

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, birthdate, joindate
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return UserModel(*(rows[0][1:]))


    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, email, firstname, lastname, birthdate, joindate
FROM Users
WHERE id = :uid
''',
                              uid=uid)
        return UserModel(*(rows[0][0:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname)
VALUES(:email, :password, :firstname, :lastname)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return UserModel.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, birthdate, joindate
FROM Users
WHERE id = :id
""",
                              id=id)
        return UserModel(*(rows[0])) if rows else None