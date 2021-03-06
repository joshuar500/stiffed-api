from app import db
from app.models.user import User, Admin, Employee
from app.models.tip import Tip
from app.validators import valid_email, valid_password
from flask import Response, json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from datetime import datetime, timedelta
import app.error_messages as error_messages

def sign_up(name, email, password):
    try:
        if not valid_email(email):
            raise ValueError('Cannot create an account with an invalid email.')
        if not valid_password(password):
            raise ValueError('Passwords must be 8 characters long, have one upper case and one number.')
        employee = Employee(name, email, password)
        employee.set_auth_token()
        db.session.add(employee)
        db.session.commit()
        contents = json.dumps(employee.json_dict(authed=True))
        # tasks.email_signup_confirmation(email, name)
        # tasks.signup_subscribe(email, name)
    except ValueError as ve:
        return error_messages.json_400(ve.message)
    except IntegrityError as ie:
        message = 'An account with this email already exists.'
        return error_messages.json_403(message)
    except Exception as e:
        print e
        return error_messages.json_499(e.message)

    return Response(contents, 200, mimetype='application/json')

def login(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            reason = 'There is no account associated with this email.'
            return error_messages.json_410(reason)

        if not user.verify_password(password):
            reason = 'This email/password is not valid.'
            return error_messages.json_401(reason)

        user.set_auth_token()
        db.session.add(user)
        db.session.commit()
        contents = json.dumps(user.json_dict(True))
    except Exception as e:
        print 'login', e.message
        db.session.rollback()
        return error_messages.json_403()

    return Response(contents, 200, mimetype='application/json')

def logout(current_user):
    try:
        User.unset_auth_token(current_user)
        db.session.add(current_user)
        db.session.commit()
        contents = json.dumps({})
    except Exception as e:
        return error_messages.json_499(e.message)

    return Response(contents, 204, mimetype='application/json')

def get_feed(current_user, uid):
    try:
        found_tips = Tip.query.filter(Tip.employee_id==uid).order_by(desc(Tip.tip_date))
        tips = [tip.json_dict() for tip in found_tips]
        contents = json.dumps({'tips': tips})
    except Exception as e:
        print e.message
        return error_messages.json_499(e.message)

    return Response(contents, 200, mimetype='application/json')

def get_earnings(current_user, uid, start_date, end_date):
    try:
        found_tips = tips.amount_by_dates(start_date, end_date)
        found_income = income.amount_by_dates(start_date, end_date)            
        contents = {}
        contents['tips'] = [tip.json_dict() for tip in found_tips]
        contents['income'] = [income.json_dict() for income in found_income]
        contents = json.dumps(contents)
    except Exception as e:
        print e.message
        return error_messages.json_499(e.message)

    return Response(contents, 200, mimetype='application/json')