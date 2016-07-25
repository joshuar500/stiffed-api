from app import app
from flask import request
from flask_cors import CORS
from datetime import datetime, timedelta
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
@app.route('/v1/<uid>/tips/weekly', methods=['GET'])
@auth_user()
def v1_weekly_tips(current_user, uid):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    return v1.tips.amount_by_dates(uid, str(today), str(seven_days_ago))

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
@app.route('/v1/<uid>/tip_outs/weekly', methods=['GET'])
@auth_user()
def v1_weekly_tip_outs(current_user, uid):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    return v1.tips.tip_outs_by_dates(uid, str(today), str(seven_days_ago))