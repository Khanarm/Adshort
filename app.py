from flask import Flask, render_template
from config import Config

# Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.plans import plans_bp
from routes.generate import generate_bp
from routes.unlock import unlock_bp
from routes.profile import profile_bp
from routes.analytics import analytics_bp
from routes.settings import settings_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(generate_bp)
app.register_blueprint(unlock_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(settings_bp)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
