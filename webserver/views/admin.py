from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user

import db.lucky_draw as db_lucky_draw


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/', methods=["GET", "POST"])
@login_required
def admin_home():
    """ Renders the admin panel home page. This view is admin only. """
    return render_template('admin/home.html')


@admin_bp.route('/create-raffle', methods=["GET", "POST"])
@login_required
def create_raffle():
    """ Create a new raffle. This view is admin only.
    Methods:
        - GET: Render the raffle creation page.
        - POST: Insert the raffle record into the DB.
                Form Data:
                - title: the title of the raffle
                - description (optional): the description of the raffle
                - prize: the prize for the raffle winner
                - prize_picture_url (optional): The URL for the cover picture of the prize
                - scheduled_at: The date and time when the raffle will and and its results will be declared.
    Redirects:
        - auth.login: The user is not logged in
        - index.index: The user is not an admin
        - admin.create_raffle: Incomplete form POSTed
        - lucky_draw.get_raffle: The raflle record was successfully inserted.
    """
    if not current_user.is_admin:
        flash(category="error", message="You are not allowed to acces admin views")
        return redirect(url_for("index.index"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        prize = request.form.get("prize")
        prize_picture_url = request.form.get("prize_picture_url")
        scheduled_at = request.form.get("scheduled_at")

        if not title or not prize or not scheduled_at:
            flash(category="error", message="Title, Prize and Scheduled on are required.")
            return redirect(url_for("admin.create_raffle"))

        raffle_id = db_lucky_draw.create_raffle(title=title, description=description, prize=prize,
                                                prize_picture_url=prize_picture_url, scheduled_at=scheduled_at)

        return redirect(url_for("lucky_dray.get_raffle", id=raffle_id))
    else:
        return render_template('admin/admin.html')
