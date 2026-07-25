from flask import Blueprint, render_template, request, redirect, flash, session

from models.settings import settings

admin_settings_bp = Blueprint(
    "admin_settings",
    __name__,
    url_prefix="/admin"
)


@admin_settings_bp.route("/settings", methods=["GET", "POST"])
def settings_page():

    # Admin Login Check
    if "admin" not in session:
        return redirect("/admin/login")

    # Default Settings
    default_settings = {
        "cpm_rate": 3.00,
        "minimum_withdraw": 5.00,
        "referral_commission": 5
    }

    # Create settings if not exists
    data = settings.find_one({})

    if not data:
        settings.insert_one(default_settings)
        data = settings.find_one({})

    # Save Settings
    if request.method == "POST":

        cpm_rate = float(request.form.get("cpm_rate"))
        minimum_withdraw = float(request.form.get("minimum_withdraw"))
        referral_commission = float(request.form.get("referral_commission"))

        settings.update_one(
            {},
            {
                "$set": {
                    "cpm_rate": cpm_rate,
                    "minimum_withdraw": minimum_withdraw,
                    "referral_commission": referral_commission
                }
            }
        )

        flash("Settings updated successfully!", "success")

        return redirect("/admin/settings")

    data = settings.find_one({})

    return render_template(
        "admin/settings.html",
        settings=data
      )
