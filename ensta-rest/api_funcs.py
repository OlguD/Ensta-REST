import os
from flask import jsonify
from functools import wraps

def login_required(f):
    # User must be logged in to use other features
    @wraps(f)
    def decorated_function(*args, **kwargs):
        file_path = os.path.join('ensta/', 'ensta-session.txt')
        if os.path.exists(file_path):
            return jsonify({'status': 'fail', 'message': 'Login required'}), 401
        return f(*args, **kwargs)

    return decorated_function
