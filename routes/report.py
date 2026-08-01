from flask import Blueprint, render_template, request, session, redirect
from bson import ObjectId
from datetime import datetime
from mongo import db

report_bp = Blueprint("report", __name__)

@report_bp.route("/report/<request_id>", methods=["GET", "POST"])
def report(request_id):

    # User login check
    if "user_id" not in session:
        return redirect("/login")

    # Check withdrawal belongs to logged-in user
    withdrawal = db.withdraw_requests.find_one({
        "request_id": request_id,
        "user_id": session["user_id"]
    })

    if not withdrawal:
        return "Withdrawal request not found", 404

    # Report submit
    if request.method == "POST":

        reason = request.form.get("reason")
        message = request.form.get("message", "").strip()

        # Required fields check
        if not reason or not message:
            return render_template(
                "report.html",
                withdrawal=withdrawal,
                error="Please select a reason and describe your issue."
            )

        # Duplicate report check
        existing_report = db.reports.find_one({
            "request_id": request_id,
            "user_id": session["user_id"]
        })

        if existing_report:
            return render_template(
                "report.html",
                withdrawal=withdrawal,
                error="You have already submitted a report for this withdrawal."
            )

        # Save report in MongoDB
        db.reports.insert_one({
            "request_id": request_id,
            "withdrawal_id": withdrawal["_id"],
            "user_id": session["user_id"],
            "reason": reason,
            "message": message,
            "status": "Pending",
            "admin_reply": "",
            "created_at": datetime.utcnow()
        })

        return redirect("/withdraw-history")

    # Open report page
    return render_template(
        "report.html",
        withdrawal=withdrawal
      )
