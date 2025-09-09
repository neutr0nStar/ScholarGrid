from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite:///test.db"
    UPLOADS_DIR: str = "uploads"
    GRIDS_STORAGE_DIR: str = "grids"


settings = Settings()
