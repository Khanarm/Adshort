from flask import Blueprint, render_template, redirect
from bson import ObjectId

from models.reports import reports
from models.users import users
from models.links import links

admin_reports_bp = Blueprint("admin_reports", __name__)


# ==========================
# Reports
# ==========================
@admin_reports_bp.route("/admin/reports")
def admin_reports():

    all_reports = list(
        reports.find().sort("reported_at", -1)
    )

    for report in all_reports:

        report["link"] = None
        report["owner"] = None

        link = links.find_one({
            "code": report.get("code")
        })

        if link:

            report["link"] = link

            try:

                owner = users.find_one({
                    "_id": ObjectId(link["user_id"])
                })

                report["owner"] = owner

            except Exception:
                report["owner"] = None

    return render_template(
        "admin/reports.html",
        reports=all_reports
    )


# ==========================
# Resolve Report
# ==========================
@admin_reports_bp.route("/admin/report/resolve/<id>")
def resolve_report(id):

    report = reports.find_one({
        "_id": ObjectId(id)
    })

    if report:

        reports.update_one(

            {
                "_id": ObjectId(id)
            },

            {
                "$set": {
                    "status": "resolved"
                }
            }

        )

        links.update_one(

            {
                "code": report.get("code")
            },

            {
                "$set": {
                    "status": "disabled"
                }
            }

        )

    return redirect("/admin/reports")


# ==========================
# Delete Report
# ==========================
@admin_reports_bp.route("/admin/report/delete/<id>")
def delete_report(id):

    reports.delete_one({

        "_id": ObjectId(id)

    })

    return redirect("/admin/reports")
