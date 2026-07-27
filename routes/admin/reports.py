from flask import Blueprint, render_template
from models.reports import reports

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
