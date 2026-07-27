import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "adshort")

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://Bikash:Bikash@bikash.yl2nhcy.mongodb.net/?retryWrites=true&w=majority"
    )

    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

    # 👇 Add these
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
