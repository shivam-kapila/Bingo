from datetime import timedelta, datetime
import logging
from typing import Optional
import sqlalchemy

import db
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_raffle(title: str, description: str, prize: str, prize_picture_url: str, scheduled_at: str) -> int:
    """Create a new lucky draw raffle.
    Args:
        title: the title of he raffle
        description (optional): the description of the raffle
        prize: the prize for the raffle winner
        prize_picture_url (optional): The URL for the cover picture of the prize
        scheduled_at: The date and time when the raffle will and and its results will be declared
    Returns:
        ID of newly created raffle.
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            INSERT INTO lucky_draw.raffle (title, description, prize, prize_picture_url, scheduled_at)
                 VALUES (:title, :description, :prize, :prize_picture_url, :scheduled_at)
              RETURNING id
        """), {
            "title": title,
            "description": description,
            "prize":  prize,
            "prize_picture_url":  prize_picture_url,
            "scheduled_at": scheduled_at,
        })
        logger.error(scheduled_at)
        return result.fetchone()["id"]


def enter_raflle(raffle_id: int, ticket_no: int, user_id: int):
    """Add an entry into the raffle for the given user with with the given user ticket.
    Args:
        raffle_id: The DB ID of the raffle
        ticket_no: The user ticket with which they enter the raffle
        user_id: The DB ID of the user.
    """
    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO lucky_draw.entry (raffle_id, ticket_no, user_id)
                 VALUES (:raffle_id, :ticket_no, :user_id)
        """), {
            "raffle_id": raffle_id,
            "tickey_no": ticket_no,
            "user_id": user_id,
        })


def get_raffle(id: int, show_email: bool = False) -> Optional[dict]:
    """Get the details for a given raffle.
    Args:
        raffle_id: The DB ID of the raffle
        show_email (optional): Show the email of the winner, in case the details are being accessed by an admin.
    Returns:
        Dictionary with the following structure:
        {
            "title": <raffle title>,
            "description": <raffle description>,
            "prize": <prize for the raffle winner>
            "prie_picture_url": <cover picture URL for the prize>
            "scheduled_at": <date and time when the raffle will and and its results will be declared>,
            "winner_name": <name of the raffle winner> (if result is declared)
            "winner_ticket_no": <winning ticket no.> (if result is declared)
            "winner_email_id": <email ID of the raffle winner> (if result is declared, visible only to admins)
        }
    """
    cols = "title, description, prize, prize_picture_url, scheduled_at, name AS winner_name, ticket_no AS winner_ticket_no"
    if show_email:
        cols += ", email_id AS winner_email_id"

    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT {cols}
              FROM lucky_draw.raffle AS raffle
         LEFT JOIN lucky_draw.result AS result
                ON raffle.id = result.raffle_id
         LEFT JOIN "user"
                ON result.user_id = "user".id
             WHERE raffle.scheduled_at < NOW()
        """.format(cols=cols)), {"id": id})

        row = result.fetchone()
        return dict(row) if row else None


def get_raffle_applicants(id: int) -> list:
    """Get a list of applicants for a given raffle.
    Args:
        raffle_id: The DB ID of the raffle   Returns:
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                name" <name of the raffle applicant>
                "ticket_no": <ticket no. of the applicant>
                email_id": <email ID of the applicant>
            },
        ...
        ]
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT name, email_id, ticket_no
              FROM lucky_draw.entry AS entry
         LEFT JOIN "user"
                ON entry.user_id = "user".id
             WHERE raffle.scheduled_at < NOW()
        """, {"id": id}))

        row = result.fetchone()
        return dict(row) if row else None


def get_past_raffles(show_email: bool = False) -> list:
    """Get the details for a given raffle.
    Args:
        show_email (optional): Show the email of the winner, in case the details are being accessed by an admin.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "title": <raffle title>,
                "description": <raffle description>,
                "prize": <prize for the raffle winner>
                "prie_picture_url": <cover picture URL for the prize>
                "scheduled_at": <date and time when the raffle will and and its results will be declared>,
                "winner_name": <name of the raffle winner> (if result is declared)
                "winner_ticket_no": <winning ticket no.> (if result is declared)
                "winner_email_id": <email ID of the raffle winner> (if result is declared, visible only to admins)
            },
            ...
        ]
    """
    cols = "title, description, prize, prize_picture_url, scheduled_at, name AS winner_name, ticket_no"
    if show_email:
        cols += ", email_id AS winner_email"

    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT {cols}
              FROM lucky_draw.raffle AS raffle
         LEFT JOIN lucky_draw.result AS result
                ON raffle.id = result.raffle_id
         LEFT JOIN "user"
                ON result.user_id = "user".id
             WHERE raffle.scheduled_at < NOW()
        """.format(cols=cols)))

        return [dict(row) for row in result.fetchall()]


def get_upcoming_raffles() -> list:
    """Get a list of upcoming raffles.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "title": <raffle title>,
                "description": <raffle description>,
                "prize": <prize for the raffle winner>
                "prie_picture_url": <cover picture URL for the prize>
                "scheduled_at": <date and time when the raffle will and and its results will be declared>,
            },
            ...
        ]
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT title, description, prize, prize_picture_url, scheduled_at
              FROM lucky_draw.raffle AS raffle
             WHERE raffle.scheduled_at > NOW()
        """))

        return [dict(row) for row in result.fetchall()]


def draw_ticket(user_id: int) -> int:
    """Insert a new ticket for the given user.
    Args:
        user_id (int): the DB ID of the user.
    Returns:
        ID of newly created ticket.
    """
    valid_upto = datetime.now() + timedelta(days=config.TICKET_VALIDITY)
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            INSERT INTO lucky_draw.ticket (user_id, valid_upto)
                 VALUES (:user_id, :valid_upto)
              RETURNING id
        """), {
            "user_id": user_id,
            "valid_upto": valid_upto,
        })

        return result.fetchone()["id"]


def get_tickets_for_user(user_id: int) -> list:
    """Get list of tickets drawn by a given user.
    Args:
        user_id (int): The DB ID of a user.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "ticket_no": <ticket no.>,
                "valid_upto": <date and time till which the ticket is valid>,
                "redeemed": <True if the user has used the given ticket, else Flase>
            },
            ...
        ]
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
              WITH (SELECT ticket_no FROM lucky_draw.entry where user_id = :user_id) AS redeemed_tickets
            SELECT ticket_no, valid_upto, ticket_no IN redeemed_tickets AS redeemed
              FROM lucky_draw.ticket
             WHERE user_id = :user_id
        """), {"user_id": user_id})

        return [dict(row) for row in result.fetchall()]


def get_next_vaild_ticket_for_user(user_id: int) -> Optional[int]:
    """Get the earliest valid and non-redeemed ticket for the user.
    Args:
        id (int): The DB ID of a user.
    Returns:
        The ticket number of the earliest valid and non-redeemed ticket.
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
              WITH (SELECT ticket_no FROM lucky_draw.entry where user_id = :user_id) AS redeemed_tickets
            SELECT ticket_n
              FROM lucky_draw.ticket
             WHERE user_id = :user_id
               AND  ticket_no NOT IN redeemed_tickets AS redeemed
               AND valid_upto > NOW()
           SORT BY created
        """), {"user_id": user_id})

        row = result.fetchone()
        return dict(row) if row else None
