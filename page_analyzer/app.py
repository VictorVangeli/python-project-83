from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask
from sqlalchemy import create_engine

from page_analyzer.core.settings import get_settings, get_db_settings
from page_analyzer.domain.url_routes import app_route


def run_migrations_if_needed():
    alembic_cfg = Config("alembic.ini")
    print(get_db_settings())
    engine = create_engine(get_db_settings())
    with engine.connect() as conn:
        current_rev = MigrationContext.configure(conn).get_current_revision()
        script = ScriptDirectory.from_config(alembic_cfg)
        head_rev = script.get_current_head()
        if current_rev != head_rev:
            print(f"Upgrading DB from {current_rev} → {head_rev}")
            alembic_cfg.attributes["connection"] = conn
            command.upgrade(alembic_cfg, "head")
        else:
            print("DB already up-to-date.")


def run_app():
    app = Flask(
        __name__,
        template_folder=get_settings().TEMPLATES_DIR,
        static_folder=get_settings().STATIC_DIR,
    )
    app.config["SECRET_KEY"] = get_settings().SECRET_KEY
    app.config["TIMEZONE"] = get_settings().TIME_ZONE
    run_migrations_if_needed()
    app.register_blueprint(app_route)
    # ДЛЯ ЗАПУСКА ЮВИКОРНА
    # asgi_app = WsgiToAsgi(app)
    # uvicorn.run(
    #     asgi_app, host="0.0.0.0", port=8000, loop="asyncio",
    # )
    return app


app = run_app()
