from flask import Blueprint, render_template, request, redirect, session
from models.users import users
import bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Future:
        # Login Logic

        pass

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check Email
        if users.find_one({"email": email}):
            return "Email already exists."

        # Hash Password
        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        # Save User
        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        return redirect("/login")

    return render_template("register.html")
