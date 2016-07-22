from app import db
from app.models.user import User, Admin, Employee
from app.models.tip import Tip
from app.validators import valid_email, valid_password
from flask import Response, json
from sqlalchemy.exc import IntegrityError
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