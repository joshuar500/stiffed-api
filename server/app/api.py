from app import app
from flask import request
from flask_cors import CORS
from datetime import datetime, timedelta, date
from auth import auth_user
from validators import valid_request_json
import error_messages
import v1

CORS(app)
@app.route('/')
def v1_home():
    return 'testing home'

###
### Accounts
###

@app.route('/v1/sign_up', methods=['POST'])
def v1_sign_up():
    required_params = ['name', 'email', 'password']
    params = request.get_json()
    if not valid_request_json(params, required_params):
        return error_messages.json_400()

    email = params['email']
    name = params.get('name', '')
    password = params['password']
    return v1.users.sign_up(name, email, password)

@app.route('/v1/login', methods=['POST'])
def v1_login():
    required_params = ['email', 'password']
    params = request.get_json()
    if not valid_request_json(params, required_params):
        return error_messages.json_400()
    email = params['email']
    password = params['password']
    return v1.users.login(email, password)

@app.route('/v1/logout', methods=['POST'])
@auth_user
def v1_logout(current_user):
    return v1.users.logout(current_user)

###
### Tips
###
@app.route('/v1/<uid>/tips/all', methods=['GET'])
@auth_user()
def v1_all_tips(current_user, uid):
    return v1.tips.get_all_tips(uid)

@app.route('/v1/<uid>/tips/summary', methods=['GET'])
@auth_user()
def v1_summary(current_user, uid):
    return v1.tips.get_summary(uid)

@app.route('/v1/<uid>/tips/bydate', methods=['POST'])
@auth_user()
def v1_tips_by_date(current_user, uid):
    required_params = ['start_date', 'end_date']
    params = request.get_json()
    if not valid_request_json(params, required_params):
        return error_messages.json_400()
    start_date = params['start_date']
    end_date = params['end_date']
    return v1.tips.amount_by_dates(uid, start_date, end_date)

@app.route('/v1/<uid>/tips/add', methods=['POST'])
@auth_user()
def v1_add_tips(current_user, uid):
    required_params = ['amount', 'tip_date']
    params = request.get_json()
    if not valid_request_json(params, required_params):
        return error_messages.json_400()
    tip_amount = params['amount']
    date = params['tip_date']
    return v1.tips.add_tips(uid, tip_amount, date)

@app.route('/v1/<uid>/tips/update', methods=['POST'])
@auth_user()
def v1_update_tips(current_user, uid):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    return v1.tips.update_tips(uid, str(today), str(seven_days_ago))

@app.route('/v1/<uid>/tips/delete', methods=['POST'])
@auth_user()
def v1_delete_tips(current_user, uid):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    return v1.tips.delete_tips(uid, str(today), str(seven_days_ago))

###
### Tip Outs
###
@app.route('/v1/<uid>/tips/out', methods=['POST'])
@auth_user()
def v1_tip_out(current_user, uid):
    required_params = ['amount', 'tip_date']
    params = request.get_json()
    if not valid_request_json(params, required_params):
        return error_messages.json_400()
    tip_out = params['amount']
    date = params['tip_date']
    return v1.tips.tip_out(uid, tip_out, date)

###
### Income
###
@app.route('/v1/<uid>/income/weekly', methods=['GET'])
@auth_user()
def v1_weekly_income(current_user, uid):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    return v1.income.amount_by_dates(uid, str(today), str(seven_days_ago))

###
### Feed
###
@app.route('/v1/<uid>/feed', methods=['GET'])
@auth_user()
def v1_feed(current_user, uid):
    return v1.users.get_feed(current_user, uid)

###
### Earnings
###
@app.route('/v1/<uid>/earnings', methods=['GET'])
@auth_user()
def v1_earnings(current_user, uid, start_date, end_date):
    return v1.users.get_earnings(current_user, uid)