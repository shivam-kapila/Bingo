from flask import Blueprint, redirect, render_template, url_for, flash
from flask.globals import current_app
from flask_login import login_required, current_user


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/', methods=["GET", "POST"])
@login_required
def admin_home():
    if current_user.email_id not in current_app.config["ADMINS"]:
        flash(category="error", message="You are not allowed to acces admin views")
        return redirect(url_for("index.index"))

    """ Renders the admin panel home page. This view is admin only. """
    return render_template('admin/home.html')
