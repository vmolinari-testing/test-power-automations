from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MICROSOFT_APP_ID: str
    MICROSOFT_APP_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()  # type: ignore[call-arg]
