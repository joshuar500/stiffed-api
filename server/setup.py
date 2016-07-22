from app import db
from app.models.user import User, Admin, Employee
from app.models.tip import Tip
from sqlalchemy.exc import IntegrityError
import dateutil.parser
from datetime import datetime, timedelta
import os

# Delete all tables if database exists
if os.environ.get('CHP_MODE', None) == 'PRODUCTION':
    db.create_all()
    exit()
else:
    try:
        User.query.delete()
        Admin.query.delete()
        Employee.query.delete()
    except:
        print "Database doesn't exist..."
        print "Creating database..."

    db.create_all()

    print "Populating database..."

    # Create dummy user
    user = User(name='Josh', email='asdf@asdf.com', password='User1234')
    db.session.add(user)
    db.session.commit()

    # Create dummy admin
    admin = Admin(name='Admin', email='admin@admin.com', password='Admin1234')
    db.session.add(admin)
    db.session.commit()

    # Create dummy Employee
    employee = Employee(name='Employee', email='employ@employ.com', password='Pass1234')
    db.session.add(employee)
    db.session.commit()

    # Add tips for dummy employee
    get_employee = Employee.query.filter_by(name='Employee').one()
    employee_id = get_employee.id
    tip1 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-01-10'), amount=12.40, tip_out_amount=None)
    db.session.add(tip1)
    db.session.commit()

    # Add more tips
    tip2 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-02-10'), amount=5.15, tip_out_amount=None)
    db.session.add(tip2)
    db.session.commit()

    # Add more tips
    tip3 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-02-15'), amount=155.25, tip_out_amount=None)
    db.session.add(tip3)
    db.session.commit()

    # Add more tips
    tip4 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-05'), amount=15.05, tip_out_amount=None)
    db.session.add(tip4)
    db.session.commit()

    # Add more tips (same date as above)
    tip5 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-05'), amount=5.95, tip_out_amount=None)
    db.session.add(tip5)
    db.session.commit()

    # Add more tips (day 1/7)
    tip6 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-05'), amount=8.12, tip_out_amount=None)
    db.session.add(tip6)
    db.session.commit()

    # Add more tips (day 2/7)
    tip7 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-06'), amount=101.12, tip_out_amount=None)
    db.session.add(tip7)
    db.session.commit()

    # Add more tips (day 3/7)
    tip8 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-07'), amount=221.06, tip_out_amount=None)
    db.session.add(tip8)
    db.session.commit()

    # Add more tips (day 4/7)
    tip9 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-08'), amount=0.0, tip_out_amount=None)
    db.session.add(tip9)
    db.session.commit()

    # Add more tips (day 5/7)
    tip10 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-09'), amount=12.12, tip_out_amount=None)
    db.session.add(tip10)
    db.session.commit()

    # Add more tips (day 6/7)
    tip11 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-10'), amount=190.27, tip_out_amount=None)
    db.session.add(tip11)
    db.session.commit()

    # Add more tips (day 7/7)
    tip12 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-11'), amount=207.00, tip_out_amount=None)
    db.session.add(tip12)
    db.session.commit()

    # Add more tips (day 7/7 + 3)
    tip13 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse('2016-03-16'), amount=100.99, tip_out_amount=None)
    db.session.add(tip13)
    db.session.commit()

    # Add more tips
    today = datetime.now().date()
    tip14 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse(str(today)), amount=100.99, tip_out_amount=None)
    db.session.add(tip14)
    db.session.commit()

    # Add more tips
    dates_ago = today - timedelta(days=4)
    tip15 = Tip(employee_id=employee_id, tip_date=dateutil.parser.parse(str(dates_ago)), amount=100.99, tip_out_amount=None)
    db.session.add(tip15)
    db.session.commit()

    print '============================='
    print 'Employee ID: '
    print employee_id
    print '============================='

    print "Finished populating database!"

    exit()