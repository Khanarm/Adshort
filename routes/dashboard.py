from flask import Blueprint, render_template, session, redirect
from models.users import users
from models.links import links
from bson import ObjectId

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    # User profile fetch
    user = users.find_one({
        "_id": ObjectId(session["user_id"])
    })

    # Current user ke latest 10 links fetch
    recent_links = list(
        links.find({
            "user_id": session["user_id"]
        })
        .sort("created_at", -1)
        .limit(10)
    )

    return render_template(
        "dashboard.html",
        username=session["username"],
        user=user,
        links=recent_links
    )
