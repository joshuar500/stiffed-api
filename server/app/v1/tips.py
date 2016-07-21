from app import db
from flask import Response, json
from app.models.user import Employee
from app.models.tip import Tip

def weekly_amount(employee):
    try:
        tips = Tip.query.filter_by(employee_id=employee.id).first()
        if tips is None:
            reason = 'There are no tips for this user'
            print reason
        
        contents = json.dumps({'tips' : tips.json_dict()})
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')