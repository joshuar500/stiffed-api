from app import db
from flask import Response, json
from app.models.user import Employee
from app.models.tip import Tip
from sqlalchemy import desc
from datetime import datetime, timedelta, date
import app.error_messages as error_messages
import dateutil.parser

###
### Tip logic
###
def amount_by_dates(uid, start_date, end_date):    
    try:
        found_tips = Tip.query.filter(Tip.employee_id==uid, Tip.tip_date<=start_date, Tip.tip_date>=end_date).order_by(desc(Tip.tip_date)).all()
    except Exception as e:
        print e.message
    
    return found_tips

def get_all_tips(uid):
    try:
        found_tips = Tip.query.filter(Tip.employee_id==uid).all()
        if found_tips is None:
            reason = 'There are no tips with this users ID'
            print reason
        tips = [tip.json_dict() for tip in found_tips]
        contents = json.dumps({'tips': tips})        
    except Exception as e:
        print e.message

    return Response(contents, 200, mimetype='application/json')

def get_summary(uid):
    try:
        # this week
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=7)
        this_week = amount_by_dates(uid, str(today), str(seven_days_ago))
        if this_week is None:
            reason = 'There are no tips with this users ID'
            print reason        

        # last week
        today = date.today().toordinal()
        lastWeek = today-7
        sunday = lastWeek - (lastWeek % 7)
        saturday = sunday + 6
        last_week = amount_by_dates(uid, str(date.fromordinal(sunday)), str(date.fromordinal(saturday)))
        if last_week is None:
            reason = 'There are no tips with this users ID'
            print reason

        # get last 6 months
        # current day
        today = date.today()
        first = today.replace(day=1)        
        # current month
        last_month_last_day = first - timedelta(days=1)
        last_month_first_day = last_month_last_day.replace(day=1)
        last_month_tips = amount_by_dates(uid, str(last_month_last_day), str(last_month_first_day))

        # current month - 1
        two_month_last_day = last_month_first_day - timedelta(days=1)
        two_month_first_day = two_month_last_day.replace(day=1)
        two_month_tips = amount_by_dates(uid, str(two_month_last_day), str(two_month_first_day))

        # current month - 2
        three_month_last_day = two_month_first_day - timedelta(days=1)
        three_month_first_day = three_month_last_day.replace(day=1)
        three_month_tips = amount_by_dates(uid, str(three_month_last_day), str(three_month_first_day))

        # current month - 3
        four_month_last_day = three_month_first_day - timedelta(days=1)
        four_month_first_day = four_month_last_day.replace(day=1)
        four_month_tips = amount_by_dates(uid, str(four_month_last_day), str(four_month_first_day))

        # current month - 4
        five_month_last_day = four_month_first_day - timedelta(days=1)
        five_month_first_day = five_month_last_day.replace(day=1)
        five_month_tips = amount_by_dates(uid, str(five_month_last_day), str(five_month_first_day))
        # current month - 5
        six_month_last_day = five_month_first_day - timedelta(days=1)
        six_month_first_day = six_month_last_day.replace(day=1)
        six_month_tips = amount_by_dates(uid, str(six_month_last_day), str(six_month_first_day))

        # create json            
        contents = {}
        contents['this_week'] = [tip.json_dict() for tip in this_week]
        contents['last_week'] = [tip.json_dict() for tip in last_week]
        contents['last_month'] = [tip.json_dict() for tip in last_month_tips]
        contents['two_month'] = [tip.json_dict() for tip in two_month_tips]
        contents['three_month'] = [tip.json_dict() for tip in three_month_tips]
        contents['four_month'] = [tip.json_dict() for tip in four_month_tips]
        contents['five_month'] = [tip.json_dict() for tip in five_month_tips]
        contents['six_month'] = [tip.json_dict() for tip in six_month_tips]
        contents = json.dumps(contents)
    except Exception as e:
        print e.message
    
    return Response(contents, 200, mimetype='application/json')

def add_tips(uid, tip_amount, date):
    try:
        date = dateutil.parser.parse(date)
        new_tip = Tip(employee_id=uid, amount=tip_amount, tip_date=date, tip_out_amount=None)
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
def tip_out(uid, tip_amount, date):
    try:
        date = dateutil.parser.parse(date)
        tip_out = Tip(employee_id=uid, amount=None, tip_date=date, tip_out_amount=tip_amount)
        db.session.add(tip_out)
        db.session.commit()
        contents = json.dumps(tip_out.json_dict())
        print contents
    except Exception as e:
        print 'tip_out ', e.message
        reason = 'Could not tip out'
        db.session.rollback()
        return error_messages.json_403(reason)
    
    return Response(contents, 200, mimetype='application/json')