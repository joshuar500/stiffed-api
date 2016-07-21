import unittest, os, sys
from config import BASEDIR
from app import app, db
from app.models.user import User, Admin, Employee
from datetime import datetime, timedelta
from sqlalchemy.exc import StatementError, IntegrityError

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(BASEDIR, 'tests/datatest.db')
        self.app = app.test_client()
        db.create_all()

        # Create test cases
        user = User('User', 'user@example.com', 'userpass')
        admin = Admin('admin@example.com', 'adminpass')
        # Commit to test database
        db.session.add(user)
        db.session.add(admin)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()