from app import db
from flask import Response, json
from app.models.user import Employee
from app.models.tip import Tip
from sqlalchemy import desc
from datetime import datetime

def amount_by_dates(uid, start_date, end_date):
    try:
        found_tips = Tip.query.filter(Tip.employee_id==uid, Tip.tip_date<=start_date, Tip.tip_date>=end_date).order_by(desc(Tip.tip_date)).all()
        if found_tips is None:
            reason = 'There is no tips with this users ID'
            print reason
        tips = [tip.json_dict() for tip in found_tips]
        contents = json.dumps({'tips': tips})
        print contents
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')