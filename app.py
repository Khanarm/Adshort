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
from routes.wallet import wallet_bp
from routes.api import api_bp
from routes.admin.login import admin_login_bp
from routes.admin.dashboard import admin_dashboard_bp
from routes.admin.users import admin_users_bp
from routes.admin.withdraw import admin_withdraw_bp
from routes.admin.links import admin_links_bp
from routes.admin.settings import admin_settings_bp
from routes.go import go_bp
from routes.admin.smartlinks import admin_smartlinks_bp
from routes.admin.reports import admin_reports_bp
from routes.links import links_bp
from routes.history import history_bp
from routes.report import report_bp

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
app.register_blueprint(wallet_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_login_bp)
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(admin_users_bp)
app.register_blueprint(admin_withdraw_bp)
app.register_blueprint(admin_links_bp)
app.register_blueprint(admin_settings_bp)
app.register_blueprint(go_bp)
app.register_blueprint(admin_smartlinks_bp)
app.register_blueprint(admin_reports_bp)
app.register_blueprint(links_bp)
app.register_blueprint(history_bp)
app.register_blueprint(report_bp)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
