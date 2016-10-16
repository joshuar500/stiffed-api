from app import db
import uuid
from random import randint, choice
import string

class Income(db.Model):
    __tablename__ = 'tips'
    id = db.Column('id', db.String(length=64), unique=True, nullable=False,
            primary_key=True)
    employee_id = db.Column('employee_id', db.String(length=64),
            db.ForeignKey('employees.id'), nullable=False)
    start_date = db.Column('start_date', db.Date(), nullable=False)
    end_date = db.Column('end_date', db.Date(), nullable=False)
    income_amount = db.Column('income_amount', db.Float)
    zip_code = db.Column('zip_code', db.Integer)

    def __init__(self, employee_id, start_date, end_date, income_amount, zip_code):        
        self.id = str(uuid.uuid4())
        self.employee_id = employee_id
        self.start_date = start_date
        self.end_date = end_date
        self.income_amount = income_amount
        self.zip_code = zip_code

    def __repr__(self):
        return '<Tip {}>'.format(self.id)

    def json_dict(self):
        ret = {
                'uid' : self.id,
                'start_date' : self.start_date,
                'end_date' : self.end_date,
                'income_amount' : self.income_amount,
                'zip_code' : self.zip_code
                }
        return ret