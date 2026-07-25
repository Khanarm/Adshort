from datetime import datetime
from models.activity_logs import activity_logs


def add_activity(user_id, username, action, details=""):

    activity_logs.insert_one({

        "user_id": user_id,
        "username": username,
        "action": action,
        "details": details,

        "created_at": datetime.utcnow()

    })
