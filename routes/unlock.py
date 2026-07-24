from flask import Blueprint, render_template
from models.links import links

unlock_bp = Blueprint("unlock", __name__)


@unlock_bp.route("/<code>")
def unlock(code):

    # Database se link search karo
    link = links.find_one({"code": code})

    # Agar link nahi mila
    if not link:
        return render_template("404.html"), 404

    # Unlock page show karo
    return render_template(
        "unlock.html",
        code=link["code"],
        platform=link["platform"],
        action_name=link["action_name"],
        ads=link["ads"],
        cpm=link["cpm"],
        destination_url=link["destination_url"]
    )
