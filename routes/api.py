from flask import Blueprint, request, jsonify, session
from models.unlock_sessions import unlock_sessions
from models.links import links
from datetime import datetime
import uuid

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/watch-ad", methods=["POST"])
def watch_ad():

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401

    data = request.json

    code = data.get("code")
    ad_number = int(data.get("ad"))

    link = links.find_one({"code": code})

    if not link:
        return jsonify({"success": False, "message": "Invalid link"}), 404

    unlock = unlock_sessions.find_one({
        "user_id": session["user_id"],
        "code": code
    })

    if not unlock:

        unlock = {
            "session_id": str(uuid.uuid4()),
            "user_id": session["user_id"],
            "code": code,
            "completed_ads": 0,
            "total_ads": link["ads"],
            "created_at": datetime.utcnow()
        }

        unlock_sessions.insert_one(unlock)

    if ad_number != unlock["completed_ads"] + 1:
        return jsonify({
            "success": False,
            "message": "Invalid ad sequence"
        })

    unlock_sessions.update_one(
        {
            "user_id": session["user_id"],
            "code": code
        },
        {
            "$set": {
                "completed_ads": ad_number
            }
        }
    )

    completed = ad_number
    total = link["ads"]

    return jsonify({
        "success": True,
        "completed": completed,
        "total": total,
        "finished": completed >= total
    })


@api_bp.route("/api/unlock", methods=["POST"])
def unlock_link():

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    code = request.json.get("code")

    unlock = unlock_sessions.find_one({
        "user_id": session["user_id"],
        "code": code
    })

    if not unlock:
        return jsonify({"success": False})

    link = links.find_one({"code": code})

    if unlock["completed_ads"] < link["ads"]:
        return jsonify({
            "success": False,
            "message": "Complete all ads first"
        })

    return jsonify({
        "success": True,
        "url": link["destination_url"]
    })
