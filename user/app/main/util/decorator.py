from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth


def token_required(api):
    def callable(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            _ = Auth.get_logged_in_user(api, request)

            return f(*args, **kwargs)

        return decorated
    return callable


def admin_token_required(api):
    def callable(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            data = Auth.get_logged_in_user(api, request)
            admin = data.get('admin')

            if not admin:
                api.abort(401, 'admin token required')

            return f(*args, **kwargs)

        return decorated
    return callable
