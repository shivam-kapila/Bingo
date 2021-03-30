from datetime import datetime, timedelta
from flask import Blueprint, jsonify, current_app, request
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

import db.lucky_draw as db_lucky_draw
from webserver.views.api_tools import validate_auth_header


lucky_draw_bp = Blueprint("lucky_draw", __name__)


@lucky_draw_bp.route("/get-raffle/<int:id>")
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


@lucky_draw_bp.route("/get-past-raffles")
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


@lucky_draw_bp.route("/get-upcoming-raffles")
def get_upcoming_raffles():
    """ Get a list of upcoming raffles.
    Redirects:
    Returns:
        - raffles: the list of raffles.
    """
    raffles = db_lucky_draw.get_upcoming_raffles()
    return jsonify({"raffles": raffles})


@lucky_draw_bp.route("/draw-ticket", methods=["POST", "OPTIONS"])
def draw_ticket():
    """ Draw a new ticket for the given user.
    Headers:
        Authoirzation: "Token auth_token"
    Returns:
        - ticket_no: the ticket no. of the newly drawn ticket.
    """
    user = validate_auth_header()
    ticket_no = db_lucky_draw.draw_ticket(user_id=user.id)
    return jsonify({"status": "ok", "ticket_no": ticket_no})


@lucky_draw_bp.route("/get-tickets", methods=["GET", "OPTIONS"])
def get_tickets_for_user():
    """ Get a given user"s tickets.
    Headers:
        Authoirzation: "Token auth_token"
    Returns:
        - tickets: the tickets of the given user.
    """
    user = validate_auth_header()
    tickets = db_lucky_draw.get_tickets_for_user(user_id=user.id)
    return jsonify({"tickets": tickets})


@lucky_draw_bp.route("/enter-raffle/<int:raffle_id>", methods=["POST", "OPTIONS"])
def enter_raffle(raffle_id):
    """ Create an entry for the given user for the raffle ``raffle_id``.
    The earliest valid non-redeemed ticket is used to enter the raffle.
    Headers:
        Authoirzation: "Token auth_token"
    Status:
        - BadRequest(404): The user has no valid non-redeemed tickets
        - BadRequest(404): The raffle doesn't exist
        - BadRequest(404): The raffle entries are closed
        - Conflict(409): The user has already entered the raffle
        - OK(200): The entry was successfully created.
    """
    user = validate_auth_header()
    ticket_no = db_lucky_draw.get_next_vaild_ticket_for_user(user_id=user.id)
    if ticket_no is None:
        return jsonify({"status": 404, "message": "You don't have any tickets left."})

    raffle = db_lucky_draw.get_raffle(raffle_id=raffle_id)

    if not raffle:
        return jsonify({"status": 404, "message": "The raffle with id %s doesn't exist." % raffle_id})

    if datetime.now() + timedelta(hours=current_app.config["TIME_TO_STOP_ACCEPTING_SUBMISSIONS"]) > raffle["submission_time"]:
        return jsonify({"status": 404, "message": "Entries for raffle with id %s are closed." % raffle_id})

    try:
        db_lucky_draw.enter_raflle(raffle_id=raffle_id, ticket_no=ticket_no, user_id=user.id)
    except IntegrityError:
        return jsonify({"status": 409, "message": "You have already signed up for this raffle."})

    return jsonify({"status": "ok"})


@lucky_draw_bp.route("/create-raffle", methods=["POST"])
def create_raffle():
    """ Create a new raffle. This view is admin only.
        Headers:
        Authoirzation: "Token auth_token"
    Status:
        - BadRequest(401): The user is not an authorized admin
        - BadRequest(404): Incomplete form POSTed
        - OK(200): The raffle was successfully created.
    """
    user = validate_auth_header()
    if user["email_id"] not in current_app.config["ADMINS"]:
        return jsonify({"status": 401, "message": "You are not allowed to access admin APIs."})

    title = request.form.get("title")
    description = request.form.get("description")
    prize = request.form.get("prize")
    prize_picture_url = request.form.get("prize_picture_url")
    scheduled_at = request.form.get("scheduled_at")

    if not title or not prize or not scheduled_at:
        return jsonify({"status": 404, "message": "Title, Prize and Scheduled on are required."})

    raffle_id = db_lucky_draw.create_raffle(title=title, description=description, prize=prize,
                                            prize_picture_url=prize_picture_url, scheduled_at=scheduled_at)

    return jsonify({"status": "ok", "raffle_id": raffle_id})
