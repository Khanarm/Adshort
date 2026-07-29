from flask import Blueprint, render_template, session, redirect
from mongo import db

history_bp = Blueprint("history", __name__)


@history_bp.route("/withdraw-history")
def withdraw_history():

    if "user_id" not in session:
        return redirect("/login")

    history = list(
        db.withdraw_requests.find(
            {"user_id": session["user_id"]}
        ).sort("created_at", -1)
    )

    return render_template(
        "history.html",
        history=history
    )
