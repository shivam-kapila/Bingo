from flask import Blueprint, jsonify
from flask_login import current_user

import db.lucky_draw as db_lucky_draw


lucky_draw_bp = Blueprint('lucky_draw', __name__)


@lucky_draw_bp.route('/get-raffle/<int:id>')
def get_raffle(id):
    """ Get raffle with the givem ``id``. Returns the raffle applicants too, in case the current_user is an admin.
    Redirects:
    Returns:
        - raffle: the raffle record for the given ``id``.
    Status:
        - NotFound(204): if the raffle record doesn't exist.
    """
    show_email = False
    if current_user and current_user.is_admin:
        show_email = True
        raffle_applicants = db_lucky_draw.get_raffle_applicants(id=id)

    raffle = db_lucky_draw.get_raffle(id=id, show_email=show_email)
    if not raffle:
        return(jsonify({"status": 204}))

    raffle["applicants"] = raffle_applicants
    return jsonify({"raffle": raffle})


@lucky_draw_bp.route('/get-past-raffles')
def get_past_raffles():
    """ Get a list of past raffles. Returns the winner email ID too, in case the current_user is an admin.
    Redirects:
    Returns:
        - raffles: the list of raffles.
    """
    show_email = False
    if current_user and current_user.is_admin:
        show_email = True

    raffles = db_lucky_draw.get_past_raffles(show_email=show_email)
    return jsonify({"raffles": raffles})


@lucky_draw_bp.route('/get-upcoming-raffles')
def get_upcoming_raffles():
    """ Get a list of upcoming raffles.
    Redirects:
    Returns:
        - raffles: the list of raffles.
    """
    raffles = db_lucky_draw.get_upcoming_raffles()
    return jsonify({"raffles": raffles})
