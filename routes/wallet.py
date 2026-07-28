from flask import Blueprint, render_template, session, redirect, request, flash
from bson import ObjectId
from mongo import db
import uuid
from datetime import datetime

wallet_bp = Blueprint("wallet", __name__)


@wallet_bp.route("/wallet")
def wallet():

    if "user_id" not in session:
        return redirect("/login")

    user = db.users.find_one({
        "_id": ObjectId(session["user_id"])
    })

    links = list(
        db.links.find({
            "user_id": session["user_id"]
        }).sort("_id", -1)
    )

    total_links = len(links)
    total_clicks = sum(link.get("clicks", 0) for link in links)
    total_earned = round(sum(link.get("earnings", 0) for link in links), 2)
    current_balance = round(user.get("current_balance", 0), 2)

    withdrawals = list(
        db.withdraw_requests.find({
            "user_id": session["user_id"]
        }).sort("_id", -1)
    )

    return render_template(
        "wallet.html",
        current_balance=current_balance,
        total_earned=total_earned,
        total_links=total_links,
        total_clicks=total_clicks,
        links=links,
        withdrawals=withdrawals
    )


@wallet_bp.route("/withdraw", methods=["POST"])
def withdraw():

    if "user_id" not in session:
        return redirect("/login")

    user = db.users.find_one({
        "_id": ObjectId(session["user_id"])
    })

    method = request.form.get("method")
    amount = float(request.form.get("amount", 0))

    upi_id = request.form.get("upi_id")

    holder_name = request.form.get("holder_name")
    bank_name = request.form.get("bank_name")
    account_number = request.form.get("account_number")
    confirm_account = request.form.get("confirm_account")
    ifsc = request.form.get("ifsc")

    if amount <= 0:
        flash("Invalid amount")
        return redirect("/wallet")

    if amount > user.get("current_balance", 0):
        flash("Insufficient Balance")
        return redirect("/wallet")

    if method == "bank":

        if account_number != confirm_account:
            flash("Account Number and Confirm Account Number do not match.")
            return redirect("/wallet")

    withdraw = {

        "request_id": "WD-" + uuid.uuid4().hex[:8].upper(),

        "user_id": session["user_id"],

        "amount": amount,

        "method": method,

        "upi_id": upi_id,

        "holder_name": holder_name,

        "bank_name": bank_name,

        "account_number": account_number,

        "ifsc": ifsc,

        "status": "Pending",

        "created_at": datetime.utcnow(),

        "completed_at": None

    }

    db.withdraw_requests.insert_one(withdraw)

    db.users.update_one(
        {
            "_id": ObjectId(session["user_id"])
        },
        {
            "$inc": {
                "current_balance": -amount
            }
        }
    )

    flash("Withdrawal request submitted successfully.")

    return redirect("/wallet")
