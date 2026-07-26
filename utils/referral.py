from bson import ObjectId
from mongo import db
from datetime import datetime


def give_referral_commission(user_id, earning):

    user = db.users.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return

    referrer_id = user.get("referred_by")

    if not referrer_id:
        return

    commission = round(float(earning) * 0.05, 2)

    db.users.update_one(
        {"_id": ObjectId(referrer_id)},
        {
            "$inc": {
                "balance": commission,
                "referral_earnings": commission
            }
        }
    )

    db.referral_commissions.insert_one({
        "referrer_id": ObjectId(referrer_id),
        "referred_user_id": ObjectId(user_id),
        "earning": earning,
        "commission": commission,
        "percentage": 5,
        "created_at": datetime.utcnow()
    })
