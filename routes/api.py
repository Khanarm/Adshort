from flask import Blueprint, request, jsonify, session
from models.unlock_sessions import unlock_sessions
from models.links import links
from models.smartlinks import smartlinks
from datetime import datetime
from datetime import timedelta
import random
import uuid

api_bp = Blueprint("api", __name__)


# ===========================
# START AD
# ===========================
@api_bp.route("/api/start-ad", methods=["POST"])
def start_ad():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    data = request.json

    code = data.get("code")
    ad_number = int(data.get("ad"))

    link = links.find_one({
        "code": code
    })

    if not link:
        return jsonify({
            "success": False,
            "message": "Invalid link"
        }), 404

    # Random Active SmartLink
    active_links = list(
        smartlinks.find({
            "status": True
        })
    )

    if not active_links:
        return jsonify({
            "success": False,
            "message": "No Smart Links Available"
        })

    selected = random.choice(active_links)

    smartlinks.update_one(
        {
            "_id": selected["_id"]
        },
        {
            "$inc": {
                "clicks": 1
            },
            "$set": {
                "last_used": datetime.utcnow()
            }
        }
    )

    unlock = unlock_sessions.find_one({
        "user_id": session["user_id"],
        "code": code
    })

    # Existing session hai to sequence check karo
    if unlock:

        expected_ad = unlock["completed_ads"] + 1

        if ad_number != expected_ad:
            return jsonify({
                "success": False,
                "message": "Please complete previous ads first"
            })

    # First Time
    if not unlock:

        unlock_sessions.insert_one({

            "session_id": str(uuid.uuid4()),

            "user_id": session["user_id"],

            "code": code,

            "completed_ads": 0,

            "current_ad": ad_number,

            "total_ads": link["ads"],

            "status": "watching",

            "start_time": datetime.utcnow(),

            "created_at": datetime.utcnow()

        })

    # Existing Session
    else:

        unlock_sessions.update_one(

            {
                "user_id": session["user_id"],
                "code": code
            },

            {
                "$set": {
                    "current_ad": ad_number,
                    "status": "watching",
                    "start_time": datetime.utcnow()
                }
            }

        )

    return jsonify({

        "success": True,

        "smartlink": selected["url"]

    })
# ===========================
# CHECK AD
# ===========================
@api_bp.route("/api/check-ad", methods=["POST"])
def check_ad():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    data = request.json
    code = data.get("code")

    unlock = unlock_sessions.find_one({
        "user_id": session["user_id"],
        "code": code
    })

    # Koi session nahi hai
    if not unlock:
        return jsonify({
            "success": True,
            "completed": 0,
            "finished": False
        })

    # Agar previous ad already complete hai
    if unlock["status"] == "completed":

        return jsonify({

            "success": True,

            "completed": unlock["completed_ads"],

            "finished": unlock["completed_ads"] >= unlock["total_ads"]

        })

    # Ad abhi watch ho raha hai
    start_time = unlock["start_time"]

    elapsed = (datetime.utcnow() - start_time).total_seconds()

    if elapsed < 15:

        return jsonify({

            "success": False,

            "remaining": int(15 - elapsed)

        })

    # 15 second complete
    completed = unlock["completed_ads"] + 1

    unlock_sessions.update_one(

        {
            "_id": unlock["_id"]
        },

        {
            "$set": {

                "completed_ads": completed,

                "status": "completed"

            }

        }

    )

    return jsonify({

        "success": True,

        "completed": completed,

        "finished": completed >= unlock["total_ads"]

    })
# ===========================
# FINAL UNLOCK
# ===========================
@api_bp.route("/api/unlock", methods=["POST"])
def unlock_link():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    data = request.json

    code = data.get("code")

    link = links.find_one({
        "code": code
    })

    if not link:
        return jsonify({
            "success": False,
            "message": "Invalid link"
        })

    unlock = unlock_sessions.find_one({
        "user_id": session["user_id"],
        "code": code
    })

    if not unlock:
        return jsonify({
            "success": False,
            "message": "Unlock session not found"
        })

    if unlock["completed_ads"] < unlock["total_ads"]:
        return jsonify({
            "success": False,
            "message": "Complete all ads first"
        })

    # Session Delete
    unlock_sessions.delete_one({
        "_id": unlock["_id"]
    })

    return jsonify({
        "success": True,
        "url": link["destination_url"]
    })
