from flask import Blueprint, render_template

unlock_bp = Blueprint("unlock", __name__)


@unlock_bp.route("/unlock")
def unlock():
    return render_template("unlock.html")
