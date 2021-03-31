from flask import request
from werkzeug.exceptions import Unauthorized
import db.user as db_user
from webserver.login import User


def validate_auth_header():
    """
    Examine the current request headers for an Authorization: Token <uuid>
    header that identifies a user and then load the corresponding user
    object from the database and return it, if successful. Otherwise return 401.
    Returns:
        - user: the user record for the given token.
    Status:
        - Unauthorized(401): if the authorization token is missing or invalid.
    """

    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise Unauthorized("You need to provide an Authorization header.")
    try:
        auth_token = auth_token.split(" ")[1]
    except IndexError:
        raise Unauthorized("Provided Authorization header is invalid.")

    user = db_user.get_by_token(auth_token=auth_token)
    if user is None:
        raise Unauthorized("Invalid authorization token.")

    return User.from_dbrow(user)
