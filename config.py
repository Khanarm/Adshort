class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "adshort")
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://Bikash:Bikash@bikash.yl2nhcy.mongodb.net/unlock2earn?retryWrites=true&w=majority"
    )
