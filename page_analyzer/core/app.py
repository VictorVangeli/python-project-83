from flask import Flask

from page_analyzer.core.settings import get_settings
from page_analyzer.domain.pa_routes import app_route


def run_app():
    app = Flask(__name__, template_folder=get_settings().TEMPLATES_DIR, static_folder=get_settings().STATIC_DIR)

    app.config['SECRET_KEY'] = get_settings().SECRET_KEY
    app.config['TIMEZONE'] = get_settings().TIME_ZONE
    app.register_blueprint(app_route)
    return app


app = run_app()
