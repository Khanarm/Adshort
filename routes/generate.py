from flask import Blueprint, render_template

generate_bp = Blueprint("generate", __name__)


@generate_bp.route("/generate")
def generate():
    return render_template("generate.html")
