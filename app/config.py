import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/telcox")
    BSS_BASE_URL: str = os.getenv("BSS_BASE_URL", "http://localhost:8001")

settings = Settings()
