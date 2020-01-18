import logging

from .. import db
from app.main.model.blacklist import BlacklistToken

LOG = logging.getLogger('app')


def save_blacklist_token(token):
    try:
        blacklist_token = BlacklistToken(token=token)
        # insert the token to blacklist
        db.session.add(blacklist_token)
        db.session.commit()
        return True
    except Exception as e:
        LOG.exception(e)
        return False
