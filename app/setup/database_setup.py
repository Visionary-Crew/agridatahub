"""
Database setup and table creation utilities.

This module provides functions to automatically discover models and create
all database tables. It scans the models directory for SQLAlchemy models
and creates the corresponding tables in the database.
"""

import importlib
import inspect
from pathlib import Path
from typing import List, Type

from sqlalchemy import MetaData, text
from sqlalchemy.orm import DeclarativeBase

from app.configuration.database import engine, get_database_path
from app.models.region import Base


def discover_models(models_dir: Path = None) -> List[Type[DeclarativeBase]]:
    """
    Automatically discover all SQLAlchemy model classes in the models directory.

    Args:
        models_dir: Path to the models directory. If None, uses default app/models.

    Returns:
        List of SQLAlchemy model classes.
    """
    if models_dir is None:
        models_dir = Path(__file__).parent.parent / "models"

    models = []

    # Walk through all Python files in the models directory
    for py_file in models_dir.rglob("*.py"):
        if py_file.name.startswith("__"):
            continue

        # Convert file path to module path
        relative_path = py_file.relative_to(Path(__file__).parent.parent.parent)
        module_path = str(relative_path.with_suffix("")).replace("/", ".").replace("\\", ".")

        try:
            # Import the module
            module = importlib.import_module(module_path)

            # Find all classes that inherit from DeclarativeBase
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (hasattr(obj, "__tablename__") and
                    issubclass(obj, DeclarativeBase) and
                    obj is not DeclarativeBase):
                    models.append(obj)
                    print(f"Discovered model: {module_path}.{name}")

        except ImportError as e:
            print(f"Could not import {module_path}: {e}")
        except Exception as e:
            print(f"Error processing {module_path}: {e}")

    return models


def create_database():
    """
    Create the SQLite database file if it doesn't exist.
    """
    db_path = get_database_path()

    if not db_path.exists():
        print(f"Creating database at: {db_path}")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db_path.touch()
    else:
        print(f"Database already exists at: {db_path}")


def create_all_tables(drop_existing: bool = False):
    """
    Create all database tables for discovered models.

    Args:
        drop_existing: If True, drop existing tables before creating new ones.
    """
    try:
        # Discover all models
        models = discover_models()

        if not models:
            print("No models found to create tables for.")
            return

        # Create database file if it doesn't exist
        create_database()

        # Drop tables if requested
        if drop_existing:
            print("Dropping existing tables...")
            Base.metadata.drop_all(bind=engine)

        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)

        print(f"Successfully created {len(models)} table(s):")
        for model in models:
            if hasattr(model, "__tablename__"):
                print(f"  - {model.__tablename__}")

        return True

    except Exception as e:
        print(f"Error creating tables: {e}")
        return False


def check_database_status():
    """
    Check the current status of the database and tables.
    """
    try:
        db_path = get_database_path()

        if not db_path.exists():
            print("Database file does not exist.")
            return False

        print(f"Database file exists at: {db_path}")
        print(f"Database file size: {db_path.stat().st_size} bytes")

        # Check which tables exist
        metadata = MetaData()
        metadata.reflect(bind=engine)

        if metadata.tables:
            print(f"Existing tables ({len(metadata.tables)}):")
            for table_name in metadata.tables.keys():
                print(f"  - {table_name}")
        else:
            print("No tables found in database.")

        return True

    except Exception as e:
        print(f"Error checking database status: {e}")
        return False


def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    """
    print("Resetting database...")
    return create_all_tables(drop_existing=True)


def execute_sql_script(script_path: Path):
    """
    Execute a SQL script file against the database.

    Args:
        script_path: Path to the SQL script file.
    """
    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()

        with engine.connect() as connection:
            # Split script into individual statements
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

            for statement in statements:
                print(f"Executing: {statement[:50]}...")
                connection.execute(text(statement))
                connection.commit()

        print(f"Successfully executed SQL script: {script_path}")

    except Exception as e:
        print(f"Error executing SQL script: {e}")


if __name__ == "__main__":
    # Command line interface for database operations
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m app.setup.database_setup create    # Create tables")
        print("  python -m app.setup.database_setup reset     # Reset database")
        print("  python -m app.setup.database_setup status    # Check status")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "create":
        success = create_all_tables()
        sys.exit(0 if success else 1)
    elif command == "reset":
        success = reset_database()
        sys.exit(0 if success else 1)
    elif command == "status":
        success = check_database_status()
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
