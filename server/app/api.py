from app import app
from flask import request
from flask_cors import CORS

CORS(app)
@app.route('/')
def v1_home():
    return 'testing home'