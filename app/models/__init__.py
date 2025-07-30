"""
This package defines the core business/domain models using Pydantic.

- Use this directory to define data structures representing entities (e.g., Crop, Farmer, Field).
- Models here are used throughout the app for type safety and business logic.
- Do NOT put database or API-specific logic here.

Usage:
    from app.models.models import Crop
"""

from app.models.region import Base, State, District, Subdistrict, City, StateType

# Export all models
__all__ = [
    "Base",
    "State",
    "District",
    "Subdistrict",
    "City",
    "StateType"
]
