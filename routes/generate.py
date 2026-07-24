from flask import Blueprint, render_template, request, session, redirect
from models.links import links
from datetime import datetime
import random
import string

generate_bp = Blueprint("generate", __name__)


def generate_code(length=6):

    chars = string.ascii_letters + string.digits

    while True:

        code = "".join(
            random.choice(chars)
            for _ in range(length)
        )

        if not links.find_one({"code": code}):
            return code


@generate_bp.route("/generate", methods=["GET", "POST"])
def generate():

    if "user_id" not in session:
        return redirect("/login")

    short_url = None

    if request.method == "POST":

        platform = request.form.get("platform")
        action_name = request.form.get("action_name")
        destination_url = request.form.get("destination_url")

        ads = int(request.form.get("ads", 1))
        cpm = float(request.form.get("cpm", 0.50))

        code = generate_code()

        links.insert_one({

            "user_id": session["user_id"],

            "code": code,

            "platform": platform,

            "action_name": action_name,

            "destination_url": destination_url,

            "ads": ads,

            "cpm": cpm,

            "clicks": 0,

            "visitors": 0,

            "earnings": 0,

            "created_at": datetime.utcnow()

        })

        short_url = request.host_url + code

    return render_template(
        "generate.html",
        short_url=short_url
    )
