from flask import request, jsonify

import db.user as db_user


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
        return jsonify({"status": 401, "message": "You need to provide an Authorization header."})
    try:
        auth_token = auth_token.split(" ")[1]
    except IndexError:
        return jsonify({"status": 401, "message": "Provided Authorization header is invalid."})

    user = db_user.get_by_token(auth_token=auth_token)
    if user is None:
        return jsonify({"status": 401, "message": "Invalid authorization token."})

    return user
