import re
from functools import wraps

EMAIL_REGEX = re.compile('^[a-zA-Z0-9\._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+$')
PASS_REGEX = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

def valid_email(email):
    if EMAIL_REGEX.match(email) == None:
        return False
    return True

def valid_password(password):
    if PASS_REGEX.match(password) == None:
        return False
    return True

def valid_request_json(request_json, required_params, optional_params=[]):
    if request_json == None:
        return False

    copy_json = request_json.copy()
    for key in required_params:
        if key not in request_json:
            return False
        copy_json.pop(key)

    optional_len = len(optional_params)
    if optional_len >= 1 and len(copy_json) > optional_len:
        return False

    for rkey in copy_json:
        if rkey not in optional_params:
            return False

    return True