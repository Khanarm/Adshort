from flask import Blueprint, render_template, request, redirect, session
from models.users import users
from datetime import timedelta
import bcrypt
import random
import string
import secrets

auth_bp = Blueprint("auth", __name__)


def generate_referral_code(length=8):

    chars = string.ascii_uppercase + string.digits

    while True:

        code = "".join(random.choice(chars) for _ in range(length))

        if not users.find_one({"referral_code": code}):
            return code

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

            session.permanent = True   # 👈 Ye line add karo

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

        ref = request.args.get("ref")

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if users.find_one({"email": email}):
            return "Email already exists"

        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        referral_code = generate_referral_code()

        referred_by = None

        if ref:
            ref_user = users.find_one({"referral_code": ref})
            if ref_user:
                referred_by = ref_user["_id"]

        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
            "balance": 0,
            "referral_code": referral_code,
            "referred_by": referred_by,
            "referral_earnings": 0
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
