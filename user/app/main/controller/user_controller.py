import logging
from flask import request
from flask_restplus import Resource, marshal

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UserDto, fail_model
from ..service.user_service import UserService
from..worker.tasks import add as task_add

LOG = logging.getLogger('app')
api = UserDto.api
_user = UserDto.user

parser = api.parser()
parser.add_argument('Authorization', type=str,
                    location='headers',
                    help='Bearer Access Token',
                    required=True)


user_service = UserService(api)

@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required(api)
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        LOG.error('=================---------------------- getting all user..')
        LOG.warning('=================---------------------- getting all user..')
        task_add.apply_async((1, 2))
        return user_service.get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        LOG.info('=================---------------------- creating user..')
        data = request.json
        return user_service.save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user', parser=parser)
    @token_required(api)     # NOTE: this line must be above marshal_with below
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        print('aaaaaaaaaaaaaaaaaa')
        LOG.error('=================---------------------- get a user..')
        user = user_service.get_a_user(public_id)
        if not user:
            api.abort(404, 'User not found.')
        else:
            return user


@api.doc(params={'param1': 'description of param1', 'param2': 'description of param2'})
@api.response(200, 'Success', fail_model(api))
@api.response(400, 'Validation Error', fail_model(api))
@api.route('/publish')
class Publish(Resource):
    def get(self):
        return 'this is publish api'
