from flask import Blueprint, render_template, request, session, redirect

generate_bp = Blueprint("generate", __name__)


@generate_bp.route("/generate", methods=["GET", "POST"])
def generate():

    if "user_id" not in session:
        return redirect("/login")

    plan = request.args.get("plan", 1)

    if request.method == "POST":

        # Future
        # Platform
        # Platform Name
        # Destination URL
        # Short Link Generate
        # MongoDB Save

        pass

    return render_template(
        "generate.html",
        plan=plan
    )
