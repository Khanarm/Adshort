from flask import Blueprint, render_template, session, redirect
from models.users import users
from bson import ObjectId

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    # User not logged in
    if "user_id" not in session:
        return redirect("/login")

    user = users.find_one({
    "_id": ObjectId(session["user_id"])
})

return render_template(
    "dashboard.html",
    username=session["username"],
    user=user
)
