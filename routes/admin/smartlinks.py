from flask import Blueprint, render_template, request, redirect, session
from models.smartlinks import smartlinks
from bson import ObjectId
from datetime import datetime

admin_smartlinks_bp = Blueprint(
    "admin_smartlinks",
    __name__,
    url_prefix="/admin"
)


@admin_smartlinks_bp.route("/smartlinks")
def smartlinks_page():

    if "admin" not in session:
        return redirect("/admin/login")

    data = list(
        smartlinks.find().sort("_id", -1)
    )

    return render_template(
        "admin/smartlinks.html",
        smartlinks=data
    )


@admin_smartlinks_bp.route("/smartlinks/add", methods=["POST"])
def add_smartlink():

    if "admin" not in session:
        return redirect("/admin/login")

    smartlinks.insert_one({

        "name": request.form.get("name"),

        "url": request.form.get("url"),

        "status": True,

        "clicks": 0,

        "created_at": datetime.utcnow()

    })

    return redirect("/admin/smartlinks")


@admin_smartlinks_bp.route("/smartlinks/toggle/<id>")
def toggle(id):

    if "admin" not in session:
        return redirect("/admin/login")

    link = smartlinks.find_one({
        "_id": ObjectId(id)
    })

    smartlinks.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": {
                "status": not link["status"]
            }
        }
    )

    return redirect("/admin/smartlinks")


@admin_smartlinks_bp.route("/smartlinks/delete/<id>")
def delete(id):

    if "admin" not in session:
        return redirect("/admin/login")

    smartlinks.delete_one({
        "_id": ObjectId(id)
    })

    return redirect("/admin/smartlinks")
