from app import db
from flask import Response, json
from app.models.user import Employee
from app.models.tip import Tip
from sqlalchemy import desc
from datetime import datetime
import app.error_messages as error_messages
import dateutil.parser

###
### Tip logic
###
def amount_by_dates(uid, start_date, end_date):
    try:
        found_tips = Tip.query.filter(Tip.employee_id==uid, Tip.tip_date<=start_date, Tip.tip_date>=end_date).order_by(desc(Tip.tip_date)).all()
        if found_tips is None:
            reason = 'There are no tips with this users ID'
            print reason
        tips = [tip.json_dict() for tip in found_tips]
        contents = json.dumps({'tips': tips})        
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')

def add_tips(uid, tip_amount, date):
    try:
        date = dateutil.parser.parse(date)
        print date
        print date
        print date
        new_tip = Tip(employee_id=uid, amount=tip_amount, tip_date=date, tip_out_amount=None)
        print new_tip
        print new_tip
        db.session.add(new_tip)
        db.session.commit()
        contents = json.dumps(new_tip.json_dict())
    except Exception as e:
        print 'add_tips ', e.message
        reason = 'Could not add tip'
        db.session.rollback()
        return error_messages.json_403(reason)
    # Return success
    return Response(contents, 200, mimetype='application/json')

def update_tips(uid, tip_amount, date):
    try:
        date = dateutil.parser.parse(date)
        new_tip = Tip(employee_id=uid, amount=tip_amount, tip_date=date)
        db.session.add(new_tip)
        db.session.commit()
        contents = json.dumps(new_tip.json_dict())
    except Exception as e:
        print 'add_tips ', e.message
        reason = 'Could not add tip'
        db.session.rollback()
        return error_messages.json_403(reason)
    # Return success
    return Response(contents, 200, mimetype='application/json')

def delete_tips(uid, tip_amount, date):
    try:
        date = dateutil.parser.parse(date)
        new_tip = Tip(employee_id=uid, amount=tip_amount, tip_date=date)
        db.session.add(new_tip)
        db.session.commit()
        contents = json.dumps(new_tip.json_dict())
    except Exception as e:
        print 'add_tips ', e.message
        reason = 'Could not add tip'
        db.session.rollback()
        return error_messages.json_403(reason)
    # Return success
    return Response(contents, 200, mimetype='application/json')

###
### Tip Out logic
###
def tip_outs_by_dates(uid, start_date, end_date):
    try:
        found_tip_outs = Tip.query.filter(Tip.employee_id==uid, Tip.tip_date<=start_date, Tip.tip_date>=end_date).order_by(desc(Tip.tip_date)).all()
        if found_tip_outs is None:
            reason = 'There are no tip outs with this users ID'
            print reason
        tip_outs = [tip_out.json_dict() for tip_out in found_tip_outs]
        contents = json.dumps({'tip_outs': tip_outs})
        print contents
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')