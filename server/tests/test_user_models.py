import unittest, os, sys
from config import BASEDIR
from app import app, db
from app.models.user import User, Admin, Employee
from datetime import datetime, timedelta
from sqlalchemy.exc import StatementError, IntegrityError

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(BASEDIR, 'tests/datatest.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_base_user(self):
        assert User.query.count() == 0
        user = User('Test', 'user@example.com', 'testpass')
        assert user.last_login == None
        user.set_auth_token()
        db.session.add(user)
        db.session.commit()

        assert User.query.count() == 1
        u_user = User.query.first()
        assert u_user.email == 'user@example.com'
        assert u_user.id == user.id
        assert user.auth_token != None
        assert user.last_login != None

    def test_create_admin(self):
        assert User.query.count() == 0
        assert Admin.query.count() == 0

        admin = Admin('Stiffed Admin', 'admin@example.com', 'adminpass')
        db.session.add(admin)
        db.session.commit()

        assert admin.name == 'Stiffed Admin'
        assert User.query.count() == 1
        assert Admin.query.count() == 1
        assert admin.email == 'admin@example.com'

    def test_create_employee(self):
        assert User.query.count() == 0
        assert Employee.query.count() == 0

        employee = Employee('Stiffed Employee', 'employee@example.com', 'employeepass')
        db.session.add(employee)
        db.session.commit()

        assert employee.name == 'Stiffed Employee'
        assert User.query.count() == 1
        assert Employee.query.count() == 1
        assert employee.email == 'employee@example.com'
        assert employee.last_login == None
        assert employee.auth_token == None
        assert employee.tips.count() == 0

        employee.set_auth_token()
        db.session.add(employee)
        db.session.commit()

        assert employee.last_login != None
        assert employee.auth_token != None

if __name__ == '__main__':
    unittest.main()