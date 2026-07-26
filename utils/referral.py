from bson import ObjectId
from datetime import datetime
from mongo import db


def give_referral_commission(user_id, earning):

    # Jis user ne earning ki
    user = db.users.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return

    # Agar referral se join nahi hua
    if not user.get("referred_by"):
        return

    # Referrer
    referrer = db.users.find_one({
        "_id": ObjectId(user["referred_by"])
    })

    if not referrer:
        return

    # 5% Commission
    commission = round(float(earning) * 0.05, 6)

    # Referrer balance update
    db.users.update_one(
        {"_id": referrer["_id"]},
        {
            "$inc": {
                "current_balance": commission,
                "referral_earnings": commission
            }
        }
    )

    # Referral History
    db.referral_commissions.insert_one({
        "referrer_id": referrer["_id"],
        "referred_user_id": user["_id"],
        "earning": earning,
        "commission": commission,
        "percentage": 5,
        "created_at": datetime.utcnow()
    })
