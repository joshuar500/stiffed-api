import unittest, os, sys
from config import BASEDIR
from app import app, db
from app.models.tip import Tip
from app.models.user import User, Admin, Employee
from datetime import datetime, timedelta
from sqlalchemy.exc import StatementError, IntegrityError
import app.v1 as v1
import dateutil.parser

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(BASEDIR, 'tests/datatest.db')
        self.app = app.test_client()
        db.create_all()

        # Create dummy Employee
        employee = Employee(name='Employee', email='employ@employ.com', password='Pass1234')
        db.session.add(employee)        
        # Create tip test cases
        today = datetime.now().date()        
        tip1 = Tip(employee_id=employee.id, tip_date=dateutil.parser.parse(str(today)), amount=12.40, tip_out_amount=None)
        db.session.add(tip1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_tip_by_date(self):        
        today = datetime.now().date()
        tip = Tip.query.filter_by(tip_date=today).one()
        assert tip.tip_date == today



if __name__ == '__main__':
    unittest.main()