import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:root@localhost/apotheke"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    FLASK_APP = os.environ.get("FLASK_APP", "barcode_scanner")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True  # Logs SQL statements


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root@localhost/apotheke"  # In-memory database for tests
    )


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    # You might set a more secure database URI in production via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+mysqldb://root:root@localhost/apotheke"
    )


# Configuration dictionary for easy access
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
