from flask import Blueprint, redirect
from bson import ObjectId

from models.links import links
from models.users import users
from utils.referral import give_referral_commission

go_bp = Blueprint("go", __name__)


@go_bp.route("/go/<track_code>")
def go(track_code):

    link = links.find_one({"track_code": track_code})

    if not link:
        return "Invalid Link"

    earning = link["cpm"] / 1000

    # Link stats
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

    # Owner balance
    users.update_one(
        {"_id": ObjectId(link["user_id"])},
        {
            "$inc": {
                "current_balance": earning
            }
        }
    )

    # 5% Referral Commission
    give_referral_commission(link["user_id"], earning)

    return redirect(link["destination_url"])
