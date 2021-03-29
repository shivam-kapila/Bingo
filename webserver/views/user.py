from flask_login.utils import login_required
from webserver.views.api_tools import validate_auth_header
from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

import db.lucky_draw as db_lucky_draw


user_bp = Blueprint('user', __name__)


@user_bp.route('/draw-ticket', methods=["POST", "OPTIONS"])
def draw_ticket():
    """ Draw a new ticket for the given user.
    Headers:
        Authoirzation: "Token auth_token"
    Returns:
        - ticket_no: the ticket no. of the newly drawn ticket.
    """
    user = validate_auth_header()
    ticket_no = db_lucky_draw.draw_ticket(user_id=user.id)
    return jsonify({'ticket_no': ticket_no})


@user_bp.route('/get-tickets', methods=["GET", "OPTIONS"])
def get_tickets_for_user():
    """ Get a given user's tickets.
    Headers:
        Authoirzation: "Token auth_token"
    Returns:
        - tickets: the tickets of the given user.
    """
    user = validate_auth_header()
    tickets = db_lucky_draw.get_tickets_for_user(user_id=user.id)
    return jsonify({'tickets': tickets})


@user_bp.route('/enter-raffle/<int:raffle_id>', methods=["POST", "OPTIONS"])
@login_required
def enter_raffle(raffle_id):
    """ Create an entry for the given user for the raffle ``raffle_id``.
    The earliest valid non-redeemed ticket is used to enter the raffle.
    Headers:
        Authoirzation: "Token auth_token"
    Status:
        - BadRequest(404): The user has no valid non-redeemed tickets
        - Conflict(404): The user has already entered the raffle
        - OK(200): The entry was successfully created.
    """
    user = validate_auth_header()
    ticket_no = db_lucky_draw.get_next_vaild_ticket_for_user(user_id=user.id)
    if ticket_no is None:
        return jsonify({"status": 404, "message": "You don't have any tickets left."})

    try:
        db_lucky_draw.enter_raflle(raffle_id=raffle_id, ticket_no=ticket_no, user_id=user.id)
    except IntegrityError:
        return jsonify({"status": 409, "message": "You have already signed up for this raffle."})

    return jsonify({'status': 'ok'})
