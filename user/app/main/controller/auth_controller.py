import logging
from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto

LOG = logging.getLogger('app')
api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        LOG.info('=================---------------------- logging in..')
        post_data = request.json
        result = Auth.login_user(api, data=post_data)
        if isinstance(result, dict):
            return result
        else:
            api.abort(401, result)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        LOG.info('=================---------------------- logging out..')
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            api.abort(403, 'Provide a valid auth token.')

        return Auth.logout_user(api, auth_header)
