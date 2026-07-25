from flask import Blueprint, render_template, session, redirect
from models.users import users
from models.links import links

admin_dashboard_bp = Blueprint(
    "admin_dashboard",
    __name__,
    url_prefix="/admin"
)


@admin_dashboard_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/admin/login")

    total_users = users.count_documents({})

    total_links = links.count_documents({})

    total_clicks = 0
    total_earnings = 0

    for link in links.find():

        total_clicks += link.get("clicks", 0)

        total_earnings += link.get("earnings", 0)

    pending_withdraw = 0

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_links=total_links,
        total_clicks=total_clicks,
        total_earnings=round(total_earnings, 2),
        pending_withdraw=pending_withdraw
  )
