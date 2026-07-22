from flask import Blueprint, render_template

plans_bp = Blueprint("plans", __name__)


@plans_bp.route("/plans")
def plans():
    return render_template("plans.html")
