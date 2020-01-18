import logging
from app.main.util.error_msg import INTERNAL_SERVER_ERROR
from app.main.model.user import User
from ..service.blacklist_service import save_blacklist_token

LOG = logging.getLogger('app')


class Auth:

    @staticmethod
    def login_user(api, data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    return {'token': auth_token.decode()}
            else:
                return 'Email or Password does not match'
        except Exception as e:
            LOG.exception(e)
            api.abort(500, INTERNAL_SERVER_ERROR)

    @staticmethod
    def logout_user(api, auth_token):
        result = User.decode_auth_token(auth_token)
        if not isinstance(result, str):
            if save_blacklist_token(auth_token):
                return "Logout successfully"
            else:
                api.abort(500, INTERNAL_SERVER_ERROR)
        else:
            print(result)
            api.abort(401, result)

    @staticmethod
    def get_logged_in_user(api, new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            result = User.decode_auth_token(auth_token)
            if not isinstance(result, str):
                user = User.query.filter_by(id=result).first()

                if not user:
                    api.abort(401, "Not found user with provided token")

                data = {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': str(user.registered_on)
                }
                return data
            api.abort(401, result)
        else:
            api.abort(401, 'Provide a valid auth token.')
