import os

from dotenv import load_dotenv
from dynaconf import Dynaconf, Validator

from page_analyzer.core.Base.singleton import Singleton

load_dotenv()


class Configuration(Singleton):
    settings = Dynaconf(
        envvar_prefix=False,
        environments=True,
        settings_files=["config/settings.yaml"],
        validators=[
            Validator("SECRET_KEY", default="ddddddddddddddddddddddddddddddd"),
            Validator(
                "DATABASE_URL",
                default=os.environ.get("DATABASE_URL"),
            ),
            Validator("TIME_ZONE", default="Europe/Moscow"),
            Validator("STATIC_DIR", default="../static_files"),
            Validator("TEMPLATES_DIR", default="../templates"),
        ],
    )


def get_settings() -> Dynaconf:
    return Configuration.settings


def get_db_settings() -> str:
    db_url = Configuration.settings.DATABASE_URL
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://")
    return db_url
