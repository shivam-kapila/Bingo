from flask import current_app
from flask_login import LoginManager, UserMixin

import db.user as db_user


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


class User(UserMixin):
    """ The user mdel extending the flask login UserMixin. """
    def __init__(self, id, name, email_id, auth_token):
        self.id = id
        self.name = name
        self.email_id = email_id
        self.auth_token = auth_token

    @classmethod
    def from_dbrow(cls, user):
        """ Create a class object from a DB record. """
        return cls(
            id=user['id'],
            name=user['name'],
            email_id=user['email_id'],
            auth_token=user['auth_token'],
        )


@login_manager.user_loader
def load_user(id):
    """ Load the logged user. """
    try:
        user = db_user.get_by_token(auth_token=id)
    except Exception as e:
        current_app.logger.error("Error while getting user: %s", str(e), exc_info=True)
        return None
    if user:
        return User.from_dbrow(user)
    else:
        return None
