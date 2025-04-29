from dynaconf import Dynaconf, Validator

from page_analyzer.core.Base.singleton import Singleton


class Configuration(Singleton):
    settings = Dynaconf(
        envvar_prefix=False,
        environments=True,
        settings_files=["config/settings.yaml"],
        validators=[
            Validator("SECRET_KEY", must_exist=True),
            Validator("DATABASE_URL", must_exist=True),
            Validator("TIME_ZONE", default="Europe/Moscow"),
            Validator("STATIC_DIR"),
            Validator("TEMPLATES_DIR"),
        ],
    )


def get_settings() -> Dynaconf:
    return Configuration.settings
