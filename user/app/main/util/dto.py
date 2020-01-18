from flask_restplus import Namespace, fields


class UserDto():
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

    formated_user = api.model('formated_user', {
        'status': fields.String(required=True, description='status of this message'),
        'data': fields.Nested(user)
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


def fail_model(api):
    return api.model('Model', {
        'message': fields.String,
    })
