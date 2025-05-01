from dynaconf import Dynaconf, Validator

from page_analyzer.core.Base.singleton import Singleton


class Configuration(Singleton):
    settings = Dynaconf(
        envvar_prefix=False,
        environments=True,
        settings_files=["config/settings.yaml"],
        validators=[
            Validator("SECRET_KEY", default='ddddddddddddddddddddddddddddddd'),
            Validator("DATABASE_URL", default="postgresql+asyncpg://pa_pan:pa_pass@pa_db:5432/pa_db"),
            Validator("TIME_ZONE", default="Europe/Moscow"),
            Validator("STATIC_DIR", default="../static_files"),
            Validator("TEMPLATES_DIR", default="../templates"),
        ],
    )


def get_settings() -> Dynaconf:
    return Configuration.settings
