import uuid
import datetime
import logging
from sqlalchemy import or_

from .. import db
from app.main.model.user import User

LOG = logging.getLogger('app')


class UserService(object):

    def __init__(self, api):
        self.api = api

    def save_new_user(self, data):
        user = User.query.filter(or_(User.email == data['email'], User.username == data['username'])).first()
        if not user:
            new_user = User(
                public_id=str(uuid.uuid4()),
                email=data['email'],
                username=data['username'],
                password=data['password'],
                registered_on=datetime.datetime.utcnow()
            )
            result = self.save_changes(new_user)
            if not result:
                return self.generate_token(new_user)
            else:
                self.api.abort(500, result)
        else:
            self.api.abort(409, 'Username or Email already exists. Please Log in.')

    def get_all_users(self):
        return User.query.all()

    def get_a_user(self, public_id):
        return User.query.filter_by(public_id=public_id).first()

    def generate_token(self, user):
        try:
            auth_token = User.encode_auth_token(user.id)
            return {'token': auth_token.decode()}, 201
        except Exception as e:
            LOG.exception(e)
            self.api.abort(401, e.args)

    def save_changes(self, data):
        try:
            db.session.add(data)
            db.session.commit()
            return None
        except Exception as e:
            LOG.exception(e)
            db.session.rollback()
            return e.args
