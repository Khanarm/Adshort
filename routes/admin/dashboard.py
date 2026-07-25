from flask import Blueprint, render_template, session, redirect
from models.users import users
from models.links import links
from models.activity_logs import activity_logs

admin_dashboard_bp = Blueprint(
    "admin_dashboard",
    __name__,
    url_prefix="/admin"
)


@admin_dashboard_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/admin/login")

    # Total Users
    total_users = users.count_documents({})

    # Total Links
    total_links = links.count_documents({})

    # Clicks & Earnings
    total_clicks = 0
    total_earnings = 0

    for link in links.find():
        total_clicks += link.get("clicks", 0)
        total_earnings += link.get("earnings", 0)

    # Pending Withdraw
    pending_withdraw = 0


    # Recent Activity
    recent_activity = list(
        activity_logs.find()
        .sort("created_at", -1)
        .limit(10)
    )


    # Top Performing Links
    top_links = list(
        links.find()
        .sort("clicks", -1)
        .limit(10)
    )


    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_links=total_links,
        total_clicks=total_clicks,
        total_earnings=round(total_earnings, 2),
        pending_withdraw=pending_withdraw,
        recent_activity=recent_activity,
        top_links=top_links
    )
