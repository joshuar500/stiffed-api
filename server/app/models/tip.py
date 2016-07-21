from app import db
from datetime import datetime
import uuid
from random import randint, choice
import string

class Tip(db.Model):
    __tablename__ = 'tips'
    id = db.Column('id', db.String(length=64), unique=True, nullable=False,
            primary_key=True)
    employee_id = db.Column('employee_id', db.String(length=64),
            db.ForeignKey('employees.id'), nullable=False)
    tip_date = db.Column('tip_date', db.DateTime(), nullable=False)
    amount = db.Column('amount', db.Integer, nullable=False)
    tip_out_amount = db.Column('tip_out_amount', db.Integer, nullable=False)

    def __init__(self, employee_id, tip_date, amount, tip_out_amount):
        self.id = str(uuid.uuid4())
        self.employee_id = employee_id
        self.tip_date = tip_date
        self.amount = amount
        self.tip_out_amount = tip_out_amount

    def __repr__(self):
        return '<Tip {}>'.format(self.id)

    def json_dict(self):
        ret = {
                'uid' : self.id,
                'tip_date' : self.tip_date,
                'amount' : self.amount,
                'tip_out_amount' : self.tip_out_amount
                }
        return ret