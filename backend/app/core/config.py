from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PDF 文档扫描项目"
    debug: bool = True
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 720

    database_url: str = "postgresql+psycopg2://postgres:postgres@postgres:5432/pdf_scan"

    storage_root: str = "/app/storage"
    upload_dir: str = "/app/storage/uploads"
    preview_dir: str = "/app/storage/previews"

    openai_base_url: str | None = None
    openai_api_key: str | None = None
    openai_model: str | None = None

    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 80

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
