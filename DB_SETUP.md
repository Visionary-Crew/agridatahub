# Database Setup Guide

This guide explains how to create and manage your SQLite database with the Indian administrative division models.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Database and Tables
```bash
python manage_db.py create
```

### 3. Check Database Status
```bash
python manage_db.py status
```

## Available Commands

### Database Management Commands

```bash
# Create all tables (discovers models automatically)
python manage_db.py create

# Create tables and drop existing ones first
python manage_db.py create --drop

# Reset entire database (WARNING: deletes all data)
python manage_db.py reset

# Check database status and existing tables
python manage_db.py status

# Discover all models in the project
python manage_db.py discover

# Execute a custom SQL script
python manage_db.py sql path/to/script.sql
```

### Alternative Usage

You can also use the setup module directly:

```bash
# Create tables
python -m app.setup.database_setup create

# Reset database
python -m app.setup.database_setup reset

# Check status
python -m app.setup.database_setup status
```

## Database Structure

The system automatically creates the following tables for Indian administrative divisions:

- **states**: State/Union Territory information
- **districts**: Districts within states
- **subdistricts**: Subdistricts/Tehsils within districts  
- **cities**: Cities/Towns/Villages within districts (optionally linked to subdistricts)

## Configuration

Database settings can be configured via environment variables:

```bash
# Database URL (default: sqlite:///./agridatahub.db)
export DB_DATABASE_URL="sqlite:///./my_database.db"

# Enable SQL query logging (default: False)
export DB_ECHO_SQL=True
```

## Using in Your Application

```python
from app.configuration.database import get_database_session
from app.models.region import State, District

# In FastAPI endpoints
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/states")
def get_states(db: Session = Depends(get_database_session)):
    return db.query(State).all()
```

## File Structure

- `app/configuration/database.py` - Database connection and settings
- `app/setup/database_setup.py` - Table creation and model discovery
- `app/models/region.py` - SQLAlchemy models for administrative divisions
- `manage_db.py` - CLI tool for database management
- `agridatahub.db` - SQLite database file (created automatically)

## Troubleshooting

1. **Import Errors**: Make sure you're running commands from the project root directory
2. **Permission Issues**: Ensure you have write permissions in the project directory
3. **Model Discovery**: New models will be automatically discovered if they inherit from `DeclarativeBase`
