from app import db
from app.models.user import User, Admin, Employee
from app.models.tip import Tip
from sqlalchemy.exc import IntegrityError
import dateutil.parser
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

    print "Finished populating database!"

    exit()