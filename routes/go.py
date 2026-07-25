from flask import Blueprint, redirect

from models.links import links

go_bp = Blueprint("go", __name__)


@go_bp.route("/go/<track_code>")
def go(track_code):

    link = links.find_one({"track_code": track_code})

    if not link:
        return "Invalid Link"

    earning = link["cpm"] / 1000

links.update_one(
    {"_id": link["_id"]},
    {
        "$inc": {
            "clicks": 1,
            "visitors": 1,
            "earnings": earning
        }
    }
)

    return redirect(link["destination_url"])
