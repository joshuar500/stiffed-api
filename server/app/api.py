from app import app
from flask import request
from flask_cors import CORS
import v1

CORS(app)
@app.route('/')
def v1_home():
    return 'testing home'

@app.route('/v1/tips/<uid>/weekly', methods=['GET'])
def v1_weekly_tips(uid):
    return v1.tips.weekly_amount(uid)