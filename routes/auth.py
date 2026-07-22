from flask import Blueprint, render_template, request, redirect, session
from models.users import users
import bcrypt

auth_bp = Blueprint("auth", __name__)


# ==========================
# Login
# ==========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({"email": email})

        if user and bcrypt.checkpw(
            password.encode(),
            user["password"].encode()
        ):

            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# ==========================
# Register
# ==========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if users.find_one({"email": email}):
            return "Email already exists"

        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        return redirect("/login")

    return render_template("register.html")


# ==========================
# Logout
# ==========================
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
