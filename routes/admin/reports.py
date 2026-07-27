from flask import Blueprint, render_template
from models.reports import reports
from flask import redirect
from bson import ObjectId

admin_reports_bp = Blueprint("admin_reports", __name__)


@admin_reports_bp.route("/admin/reports")
def admin_reports():

    all_reports = list(
        reports.find().sort("reported_at", -1)
    )

    return render_template(
        "admin/reports.html",
        reports=all_reports
    )

# ==========================
# Resolve Report
# ==========================
@admin_reports_bp.route("/admin/report/resolve/<id>")
def resolve_report(id):

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
