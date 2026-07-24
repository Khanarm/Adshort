from flask import Blueprint, render_template, session, redirect
from mongo import db

wallet_bp = Blueprint("wallet", __name__)


@wallet_bp.route("/wallet")
def wallet():

    if "user_id" not in session:
        return redirect("/login")

    user = db.users.find_one({"_id": session["user_id"]})

    links = list(
        db.links.find(
            {"user_id": session["user_id"]}
        ).sort("created_at", -1)
    )

    total_links = len(links)
    total_clicks = sum(link.get("clicks", 0) for link in links)
    total_earned = round(sum(link.get("earnings", 0) for link in links), 2)

    current_balance = user.get("current_balance", 0)

    return render_template(
        "wallet.html",
        current_balance=current_balance,
        total_earned=total_earned,
        total_links=total_links,
        total_clicks=total_clicks,
        links=links
  )
