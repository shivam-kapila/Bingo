import logging
from typing import Optional
import sqlalchemy
import uuid

import db


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create(name: str, email_id: str, password: str) -> int:
    """Create a new user.
    Args:
        name : the name of the user
        email_id: the email ID of the user
        password: The password for the user.
    Returns:
        ID of newly created user.
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            INSERT INTO "user" (name, email_id, password, auth_token)
                 VALUES (:name, :email_id, CRYPT(:password, gen_salt('bf')), :token)
              RETURNING id
        """), {
            "name": name,
            "email_id": email_id,
            "password":  password,
            "token": str(uuid.uuid4()),
        })
        return result.fetchone()["id"]


def get(id: int) -> Optional[dict]:
    """Get user with a specified ID.
    Args:
        id (int): The DB ID of a user.
    Returns:
        Dictionary with the following structure:
        {
            "id": <DB ID of the user>,
            "name": <name of of the user>,
            "email_id": <email ID of the user>,
            "auth_token": <authentication token of the user>,
        }
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT id, name, email_id, auth_token
              FROM "user"
             WHERE id = :id
        """), {"id": id})
        row = result.fetchone()
        return dict(row) if row else None


def get_by_email_id_and_password(email_id: str, password: str) -> Optional[dict]:
    """Get user with a specified email ID amd password.
    Args:
        email_id: the email ID of the user
        password: The password for the user.
    Returns:
        Dictionary with the following structure:
        {
            "id": <DB ID of the user>,
            "name": <name of of the user>,
            "email_id": <email ID of the user>,
            "auth_token": <authentication token of the user>,
        }
    """
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT id, name, email_id, auth_token
              FROM "user"
             WHERE email_id = :email_id
               AND password = CRYPT(:password, password);
        """), {
            "email_id": email_id,
            "password": password
        })
        row = result.fetchone()
        return dict(row) if row else None
