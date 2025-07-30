"""
Database configuration for SQLAlchemy with SQLite.

This module handles database connection settings and engine creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from pathlib import Path


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    # SQLite database file path
    database_url: str = "sqlite:///./agridatahub.db"

    # SQLAlchemy engine settings
    echo_sql: bool = False  # Set to True for SQL query logging
    pool_pre_ping: bool = True

    class Config:
        env_prefix = "DB_"
        case_sensitive = False


# Global database settings instance
db_settings = DatabaseSettings()

# Create SQLAlchemy engine
engine = create_engine(
    db_settings.database_url,
    echo=db_settings.echo_sql,
    pool_pre_ping=db_settings.pool_pre_ping,
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database_session():
    """
    Dependency function to get database session.
    Use this in FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_database_path() -> Path:
    """Get the path to the SQLite database file."""
    if db_settings.database_url.startswith("sqlite:///"):
        db_path = db_settings.database_url.replace("sqlite:///", "")
        return Path(db_path).resolve()
    else:
        raise ValueError("Only SQLite databases are supported for path extraction")
