from flask import Blueprint, request, jsonify, session
from models.unlock_sessions import unlock_sessions
from models.links import links
from models.smartlinks import smartlinks
from datetime import datetime
from models.reports import reports
import random
import uuid


api_bp = Blueprint("api", __name__)


# ===========================
# START AD
# ===========================
@api_bp.route("/api/start-ad", methods=["POST"])
def start_ad():

    # Guest visitor support
    visitor_id = session.get("visitor_id")

    if not visitor_id:
        visitor_id = str(uuid.uuid4())
        session["visitor_id"] = visitor_id

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

    # ===========================
    # GET ACTIVE SMARTLINK
    # ===========================
    active_links = list(
        smartlinks.find({
            "status": True
        })
    )

    if not active_links:
        return jsonify({
            "success": False,
            "message": "No Smart Links Available"
        }), 404

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

    # ===========================
    # CHECK UNLOCK SESSION
    # ===========================
    unlock = unlock_sessions.find_one({
        "visitor_id": visitor_id,
        "code": code
    })

    # Sequence check
    if unlock:

        expected_ad = unlock["completed_ads"] + 1

        if ad_number != expected_ad:

            return jsonify({
                "success": False,
                "message": "Please complete previous ads first"
            })

    # ===========================
    # CREATE NEW SESSION
    # ===========================
    if not unlock:

        unlock_sessions.insert_one({

            "session_id": str(uuid.uuid4()),

            "visitor_id": visitor_id,

            "code": code,

            "completed_ads": 0,

            "current_ad": ad_number,

            "total_ads": link["ads"],

            "status": "waiting",

            "start_time": datetime.utcnow(),

            "created_at": datetime.utcnow()

        })

    # ===========================
    # UPDATE EXISTING SESSION
    # ===========================
    else:

        unlock_sessions.update_one(

            {
                "visitor_id": visitor_id,
                "code": code
            },

            {
                "$set": {

                    "current_ad": ad_number,

                    "status": "waiting",

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

    visitor_id = session.get("visitor_id")

    if not visitor_id:
        return jsonify({
            "success": False,
            "message": "Session expired"
        })

    data = request.json
    code = data.get("code")

    unlock = unlock_sessions.find_one({

        "visitor_id": visitor_id,

        "code": code

    })

    if not unlock:

        return jsonify({

            "success": True,

            "completed": 0,

            "finished": False

        })

    # Active ad check

    if unlock["status"] != "waiting":

        return jsonify({

            "success": False,

            "message": "No active ad"

        })

    start_time = unlock["start_time"]

    elapsed = (
        datetime.utcnow() - start_time
    ).total_seconds()

    # 15 second timer

    if elapsed < 15:

        return jsonify({

            "success": False,

            "remaining": int(15 - elapsed)

        })

    # Ad completed

    completed = unlock["completed_ads"] + 1

    unlock_sessions.update_one(

        {
            "_id": unlock["_id"]
        },

        {
            "$set": {

                "completed_ads": completed,

                "status": "idle",

                "start_time": None,

                "current_ad": None

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

    visitor_id = session.get("visitor_id")

    if not visitor_id:
        return jsonify({

            "success": False,

            "message": "Session expired"

        })

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

        "visitor_id": visitor_id,

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

    # Delete unlock session

    unlock_sessions.delete_one({

        "_id": unlock["_id"]

    })

    return jsonify({

        "success": True,

        "url": f"/go/{link['track_code']}"

    })

# ===========================
# REPORT LINK
# ===========================
@api_bp.route("/api/report", methods=["POST"])
def report_link():

    data = request.json

    code = data.get("code")
    reason = data.get("reason", "")

    link = links.find_one({
        "code": code
    })

    if not link:
        return jsonify({
            "success": False,
            "message": "Invalid Link"
        })

    reports.insert_one({

        "code": code,
        "destination_url": link["destination_url"],
        "platform": link["platform"],
        "action_name": link["action_name"],
        "reason": reason,
        "reported_at": datetime.utcnow(),
        "status": "pending"

    })

    return jsonify({

        "success": True,
        "message": "Report submitted"

    })
