from flask import Blueprint, render_template, session, redirect
from models.users import users
from models.links import links

admin_users_bp = Blueprint(
    "admin_users",
    __name__,
    url_prefix="/admin"
)


@admin_users_bp.route("/users")
def users_page():

    if "admin" not in session:
        return redirect("/admin/login")

    data = []

    for user in users.find():

        user_links = list(links.find({"user_id": user["_id"]}))

        total_links = len(user_links)
        total_clicks = sum(i.get("clicks", 0) for i in user_links)
        total_earnings = sum(i.get("earnings", 0) for i in user_links)

        data.append({
            "_id": str(user["_id"]),
            "username": user.get("username", ""),
            "email": user.get("email", ""),
            "links": total_links,
            "clicks": total_clicks,
            "earnings": round(total_earnings, 2),
            "balance": user.get("balance", 0),
            "status": user.get("status", "Active")
        })

    return render_template(
        "admin/users.html",
        users=data
      )
