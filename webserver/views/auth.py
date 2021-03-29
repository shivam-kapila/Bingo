from datetime import timedelta
from flask import Blueprint, redirect, render_template, url_for, session, current_app, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from webserver.login import User
from sqlalchemy.exc import IntegrityError

import db.user as db_user


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():

    if current_user and current_user.is_authenticated:
        return redirect(url_for("index.index"))

    if request.method == "POST":
        email_id = request.form.get("email_id")
        password = request.form.get("password")

        user = db_user.get_by_email_id_and_password(email_id=email_id, password=password)
        if user:
            user = User.from_dbrow(user)
            login_user(user, remember=True, duration=timedelta(current_app.config['SESSION_REMEMBER_ME_DURATION']))
            return redirect(url_for("index.index"))
        else:
            flash(category="error", message="No user with the given details found")
            return redirect(url_for("auth.login"))
    else:
        return render_template('auth/auth.html')


@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
    """ Signs up a new user.
    Methods:
        - GET: Render the signup page.
        - POST: Insert the raffle record into the DB.
                Form Data:
                - name: the name of the user
                - email_id: the email ID of the user
                - password: the password of the user.
    Redirects:
        - index.index: The user is already logged in
        - auth.signup: Incomplete form POSTed
        - index.index: The user is successfully signed in
        - auth.login: A user with the POSTed email already exists.
    """
    if current_user and current_user.is_authenticated:
        return redirect(url_for("index.index"))

    if request.method == "POST":
        name = request.form.get("name")
        email_id = request.form.get("email_id")
        password = request.form.get("password")

        if not name or not email_id or not password:
            flash(category="error", message="Name, Email ID and Password are required")
            return redirect(url_for("auth.signup"))

        try:
            user_id = db_user.create(name=name, email_id=email_id, password=password)
        except IntegrityError:
            flash(category="error", message="Email ID already registered. Try logging in instead.")
            return redirect(url_for("auth.login"))

        user = User.from_dbrow(db_user.get(id=user_id))
        if user:
            login_user(user, remember=True, duration=timedelta(current_app.config['SESSION_REMEMBER_ME_DURATION']))
            return redirect(url_for("index.index"))
    else:
        return render_template('auth/auth.html')


@auth_bp.route('/logout/', methods=["POST"])
@login_required
def logout():
    """ Logs out the logged in user.

    Redirects:
        - index.index: The user is already logged out.
    """
    session.clear()
    logout_user()
    return redirect(url_for('index.index'))
