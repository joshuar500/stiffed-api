from flask import request, session
from models.user import User
from putil import optional_arg_decorator
from functools import wraps
import error_messages

@optional_arg_decorator
def auth_user(func, roles=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Stiffed-Token', None)
        if token is None:
            return error_messages.json_401()
        user = User.query.filter_by(auth_token=token).first()        
        if user is None:
            return error_messages.json_401()
        if roles is not None:
            valid_role = False
            for role in roles:
                if role == user.role:
                    valid_role = True
                    break

            if not valid_role:
                return error_messages.json_401()

        # Pass found user as current_user to wrapped func
        kwargs['current_user'] = user
        return func(*args, **kwargs)
    return wrapper