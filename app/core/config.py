from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = (
        "Coral Bleaching Prediction API"
    )

    app_version: str = "0.1.0"

    environment: str = "development"

    model_path: str = (
        "models/"
        "coral_bleaching_pipeline.joblib"
    )

    model_metadata_path: str = (
        "models/"
        "model_metadata.json"
    )


settings = Settings()