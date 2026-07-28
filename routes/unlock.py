from flask import Blueprint, render_template, session
from models.links import links
from models.unlock_sessions import unlock_sessions
import uuid

unlock_bp = Blueprint("unlock", __name__)


@unlock_bp.route("/<code>")
def unlock(code):

    link = links.find_one({"code": code})

    if not link:
        return render_template("404.html"), 404

    # ==========================
    # Link Disabled Check
    # ==========================
    if link.get("status") == "disabled":
        return render_template("link_disabled.html"), 403

    # Guest visitor id
    visitor_id = session.get("visitor_id")

    if not visitor_id:
        visitor_id = str(uuid.uuid4())
        session["visitor_id"] = visitor_id

    # Purani session delete
    unlock_sessions.delete_many({
        "visitor_id": visitor_id,
        "code": code
    })

    return render_template(
        "unlock.html",
        code=link["code"],
        platform=link["platform"],
        action_name=link["action_name"],
        ads=link["ads"],
        cpm=link["cpm"],
        destination_url=link["destination_url"]
    )
