from flask import Blueprint, render_template, request, session, redirect, flash

admin_login_bp = Blueprint("admin_login", __name__, url_prefix="/admin")

# Temporary Admin Login
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


@admin_login_bp.route("/login", methods=["GET", "POST"])
def login():

    if "admin" in session:
        return redirect("/admin/dashboard")

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = True
            session["admin_username"] = username

            return redirect("/admin/dashboard")

        flash("Invalid Username or Password", "danger")

    return render_template("admin/login.html")


@admin_login_bp.route("/logout")
def logout():

    session.pop("admin", None)
    session.pop("admin_username", None)

    return redirect("/admin/login")
