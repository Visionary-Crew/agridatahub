"""
SQLAlchemy ORM models for Indian administrative divisions.

This module defines the hierarchical structure of Indian administrative regions:
State -> District -> Subdistrict -> City

Each model includes proper relationships, indexes for performance, and automatic
timestamp management for tracking creation and updates.
"""

from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class StateType(PyEnum):
    """Enumeration for different types of states in India."""
    STATE = "state"
    UNION_TERRITORY = "union territory"


class State(Base):
    """
    Represents a state or union territory in India.

    States are the top-level administrative divisions in India.
    This includes both states and union territories.
    """
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[StateType] = mapped_column(Enum(StateType), nullable=False)
    capital_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("cities.id", ondelete="SET NULL"),
        nullable=True,
        comment="Reference to the capital city of this state"
    )

    # Timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    districts: Mapped[List["District"]] = relationship(
        "District",
        back_populates="state",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    capital: Mapped[Optional["City"]] = relationship(
        "City",
        backref="capital_of_state",
        foreign_keys=[capital_id]
    )

    # Indexes
    __table_args__ = (
        Index("ix_states_name", "name"),
        Index("ix_states_type", "type"),
        Index("ix_states_capital_id", "capital_id"),
    )

    def __repr__(self) -> str:
        return f"<State(id={self.id}, name='{self.name}', type='{self.type.value}')>"


class District(Base):
    """
    Represents a district within a state in India.

    Districts are the second-level administrative divisions.
    Each district belongs to exactly one state.
    """
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    state_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("states.id", ondelete="CASCADE"),
        nullable=False
    )

    # Timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship("State", back_populates="districts")
    subdistricts: Mapped[List["Subdistrict"]] = relationship(
        "Subdistrict",
        back_populates="district",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    cities: Mapped[List["City"]] = relationship(
        "City",
        back_populates="district",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # Indexes
    __table_args__ = (
        Index("ix_districts_name", "name"),
        Index("ix_districts_state_id", "state_id"),
        Index("ix_districts_state_name", "state_id", "name"),  # Composite index for unique constraint
    )

    def __repr__(self) -> str:
        return f"<District(id={self.id}, name='{self.name}', state_id={self.state_id})>"


class Subdistrict(Base):
    """
    Represents a subdistrict (tehsil/taluka/block) within a district.

    Subdistricts are the third-level administrative divisions.
    Each subdistrict belongs to exactly one district.
    """
    __tablename__ = "subdistricts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    district_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("districts.id", ondelete="CASCADE"),
        nullable=False
    )

    # Timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    district: Mapped["District"] = relationship("District", back_populates="subdistricts")
    cities: Mapped[List["City"]] = relationship(
        "City",
        back_populates="subdistrict",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # Indexes
    __table_args__ = (
        Index("ix_subdistricts_name", "name"),
        Index("ix_subdistricts_district_id", "district_id"),
        Index("ix_subdistricts_district_name", "district_id", "name"),  # Composite index
    )

    def __repr__(self) -> str:
        return f"<Subdistrict(id={self.id}, name='{self.name}', district_id={self.district_id})>"


class City(Base):
    """
    Represents a city/town/village within a district.

    Cities are the fourth-level administrative divisions.
    Each city belongs to exactly one district and optionally to a subdistrict.
    Some cities may be directly under a district without a subdistrict.
    """
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    district_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("districts.id", ondelete="CASCADE"),
        nullable=False
    )
    subdistrict_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("subdistricts.id", ondelete="CASCADE"),
        nullable=True,
        comment="Optional reference to subdistrict - some cities are directly under district"
    )
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Latitude coordinate")
    lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Longitude coordinate")

    # Timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    district: Mapped["District"] = relationship("District", back_populates="cities")
    subdistrict: Mapped[Optional["Subdistrict"]] = relationship(
        "Subdistrict",
        back_populates="cities"
    )

    # Indexes
    __table_args__ = (
        Index("ix_cities_name", "name"),
        Index("ix_cities_district_id", "district_id"),
        Index("ix_cities_subdistrict_id", "subdistrict_id"),
        Index("ix_cities_coordinates", "lat", "lng"),
        Index("ix_cities_district_name", "district_id", "name"),  # Composite index
        Index("ix_cities_subdistrict_name", "subdistrict_id", "name"),  # Composite index
    )

    def __repr__(self) -> str:
        subdistrict_info = f", subdistrict_id={self.subdistrict_id}" if self.subdistrict_id else ""
        return f"<City(id={self.id}, name='{self.name}', district_id={self.district_id}{subdistrict_info})>"


# Export all models for easy importing
__all__ = ["Base", "State", "District", "Subdistrict", "City", "StateType"]
