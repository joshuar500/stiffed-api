from app import db
from flask import Response, json
from app.models.user import Employee
from app.models.tip import Tip
from sqlalchemy import desc

def weekly_amount(uid):
    try:
        found_tips = Tip.query.filter_by(employee_id=uid).order_by(desc(Tip.tip_date)).limit(7)
        if found_tips is None:
            reason = 'There is no tips with this users ID'
            print reason
        
        tips = [tip.json_dict() for tip in found_tips]
        contents = json.dumps({'tips': tips})
        print contents
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')