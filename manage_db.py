#!/usr/bin/env python3
"""
Database management CLI script.

A simple command-line interface for managing the SQLite database.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.setup.database_setup import (
    create_all_tables,
    reset_database,
    check_database_status,
    execute_sql_script,
    discover_models
)


def main():
    parser = argparse.ArgumentParser(description="Database management utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create all database tables")
    create_parser.add_argument("--drop", action="store_true",
                              help="Drop existing tables before creating")

    # Reset command
    subparsers.add_parser("reset", help="Reset database (drop and recreate all tables)")

    # Status command
    subparsers.add_parser("status", help="Check database status")

    # Discover command
    subparsers.add_parser("discover", help="Discover all models in the project")

    # Execute SQL script command
    sql_parser = subparsers.add_parser("sql", help="Execute a SQL script file")
    sql_parser.add_argument("script", help="Path to SQL script file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "create":
            success = create_all_tables(drop_existing=args.drop)
            if success:
                print("✅ Database tables created successfully!")
            else:
                print("❌ Failed to create database tables")
                sys.exit(1)

        elif args.command == "reset":
            print("⚠️  This will delete all existing data!")
            confirm = input("Are you sure? (y/N): ")
            if confirm.lower() == 'y':
                success = reset_database()
                if success:
                    print("✅ Database reset successfully!")
                else:
                    print("❌ Failed to reset database")
                    sys.exit(1)
            else:
                print("Operation cancelled.")

        elif args.command == "status":
            check_database_status()

        elif args.command == "discover":
            models = discover_models()
            print(f"Found {len(models)} model(s):")
            for model in models:
                print(f"  📋 {model.__name__} -> {getattr(model, '__tablename__', 'N/A')}")

        elif args.command == "sql":
            script_path = Path(args.script)
            if not script_path.exists():
                print(f"❌ Script file not found: {script_path}")
                sys.exit(1)
            execute_sql_script(script_path)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
