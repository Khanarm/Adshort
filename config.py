import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "adshort")

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://ainularma65_db_user:575751an@cluster0.ryckrzu.mongodb.net/?appName=Cluster0"
    )

    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

    # 👇 Add these
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
