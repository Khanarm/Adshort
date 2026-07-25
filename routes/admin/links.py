from flask import Blueprint, render_template, session, redirect
from bson import ObjectId

from models.links import links
from models.users import users

admin_links_bp = Blueprint(
    "admin_links",
    __name__,
    url_prefix="/admin"
)


@admin_links_bp.route("/links")
def links_page():

    if "admin" not in session:
        return redirect("/admin/login")

    data = []

    for link in links.find().sort("_id", -1):

        user = users.find_one({"_id": link["user_id"]})

        data.append({
            "_id": str(link["_id"]),
            "username": user.get("username", "Unknown") if user else "Unknown",
            "action_name": link.get("action_name", ""),
            "short_code": link.get("code", ""),
            "destination_url": link.get("destination_url", ""),
            "ads": link.get("ads", 0),
            "cpm": link.get("cpm", 0),
            "clicks": link.get("clicks", 0),
            "earnings": round(link.get("earnings", 0), 2),
            "status": link.get("status", "Active")
        })

    return render_template(
        "admin/links.html",
        links=data
    )


@admin_links_bp.route("/link/delete/<link_id>")
def delete_link(link_id):

    if "admin" not in session:
        return redirect("/admin/login")

    links.delete_one({
        "_id": ObjectId(link_id)
    })

    return redirect("/admin/links")
