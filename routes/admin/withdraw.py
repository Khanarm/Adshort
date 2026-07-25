from flask import Blueprint, render_template, session, redirect
from bson import ObjectId
from mongo import db

admin_withdraw_bp = Blueprint(
    "admin_withdraw",
    __name__,
    url_prefix="/admin"
)


@admin_withdraw_bp.route("/withdraw")
def withdraw_requests():

    if "admin" not in session:
        return redirect("/admin/login")

    requests = list(
        db.withdraw_requests.find().sort("_id", -1)
    )

    for req in requests:

        user = db.users.find_one({
            "_id": ObjectId(req["user_id"])
        })

        if user:
            req["username"] = user.get("username", "Unknown")
            req["email"] = user.get("email", "")
        else:
            req["username"] = "Unknown"
            req["email"] = ""

    return render_template(
        "admin/withdraw.html",
        requests=requests
    )


@admin_withdraw_bp.route("/withdraw/approve/<id>")
def approve(id):

    if "admin" not in session:
        return redirect("/admin/login")

    db.withdraw_requests.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": "Success"
            }
        }
    )

    return redirect("/admin/withdraw")


@admin_withdraw_bp.route("/withdraw/reject/<id>")
def reject(id):

    if "admin" not in session:
        return redirect("/admin/login")

    req = db.withdraw_requests.find_one({
        "_id": ObjectId(id)
    })

    if req:

        db.users.update_one(
            {
                "_id": ObjectId(req["user_id"])
            },
            {
                "$inc": {
                    "current_balance": req["amount"]
                }
            }
        )

        db.withdraw_requests.update_one(
            {
                "_id": ObjectId(id)
            },
            {
                "$set": {
                    "status": "Rejected"
                }
            }
        )

    return redirect("/admin/withdraw")
