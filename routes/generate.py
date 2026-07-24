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

    plan = request.args.get("plan", 1)

    if request.method == "POST":

        platform = request.form.get("platform")
        platform_name = request.form.get("platform_name")
        destination_url = request.form.get("destination_url")

        code = generate_code()

        links.insert_one({

            "user_id": session["user_id"],

            "code": code,

            "plan": int(plan),

            "platform": platform,

            "platform_name": platform_name,

            "destination_url": destination_url,

            "clicks": 0,

            "visitors": 0,

            "earnings": 0,

            "created_at": datetime.utcnow()

        })

        return redirect("/dashboard")

    return render_template(
        "generate.html",
        plan=plan
    )
