from app import db
from flask import Response, json
from app.models.user import Employee
from app.models.income import Income
from sqlalchemy import desc
from datetime import datetime
import app.error_messages as error_messages
import dateutil.parser

###
### Income logic
###
def amount_by_dates(uid, start_date, end_date):
    try:
        found_income = Income.query.filter(Income.employee_id==uid, Income.start_date<=start_date, Income.end_date.tip_date>=end_date).order_by(desc(Income.start_date)).all()
        if found_income is None:
            reason = 'There is no income with this users ID'
            print reason
        income = [income.json_dict() for income in found_income]
        contents = json.dumps({'income': income})        
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')