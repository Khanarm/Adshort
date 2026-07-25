from flask import Blueprint, render_template, session, redirect
from models.users import users
from models.links import links
from bson import ObjectId
from flask import Blueprint, render_template, session, redirect, url_for, flash

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

@admin_users_bp.route("/user/<user_id>")
def user_profile(user_id):

    if "admin" not in session:
        return redirect("/admin/login")

    user = users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return "User Not Found", 404

    user_links = list(
        links.find({"user_id": user["_id"]})
    )

    total_links = len(user_links)
    total_clicks = sum(i.get("clicks", 0) for i in user_links)
    total_earnings = sum(i.get("earnings", 0) for i in user_links)

    return render_template(
        "admin/user_profile.html",
        user=user,
        links=user_links,
        total_links=total_links,
        total_clicks=total_clicks,
        total_earnings=round(total_earnings, 2)
    )

@admin_users_bp.route("/user/block/<user_id>")
def block_user(user_id):

    if "admin" not in session:
        return redirect("/admin/login")

    users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "status": "Blocked"
            }
        }
    )

    return redirect("/admin/users")



@admin_users_bp.route("/user/unblock/<user_id>")
def unblock_user(user_id):

    if "admin" not in session:
        return redirect("/admin/login")

    users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "status": "Active"
            }
        }
    )

    return redirect("/admin/users")

@admin_users_bp.route("/user/delete/<user_id>")
def delete_user(user_id):

    if "admin" not in session:
        return redirect("/admin/login")

    try:
        object_id = ObjectId(user_id)

        # Delete all links of this user
        links.delete_many({
            "user_id": object_id
        })

        # Delete user
        users.delete_one({
            "_id": object_id
        })

    except Exception:
        return "Invalid User ID", 400

    return redirect("/admin/users")
