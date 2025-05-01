from asgiref.wsgi import WsgiToAsgi
from flask import Flask

from page_analyzer.core.settings import get_settings
from page_analyzer.domain.url_routes import app_route


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=get_settings().TEMPLATES_DIR,
        static_folder=get_settings().STATIC_DIR,
    )
    app.config['SECRET_KEY'] = get_settings().SECRET_KEY
    app.config['TIMEZONE'] = get_settings().TIME_ZONE
    app.register_blueprint(app_route)
    return app



asgi_app = WsgiToAsgi(create_app())


def run_app():
    import uvicorn
    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=8000,
        loop="asyncio"
    )
