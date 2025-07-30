from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship, declarative_base
from app.models.crop.crop_models import Season
from enum import Enum

class IrrigationSource(str, Enum):
    canal = "Canal"
    groundwater = "Groundwater"
    rainfed = "Rainfed"
    tank = "Tank"
    mixed = "Mixed"

class WaterDependency(BaseModel):
    __tablename__ = "water_dependency"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crop.id"), nullable=False)
    water_requirement_mm = Column(Float)
    irrigation_source = Optional[IrrigationSource] = Field(None, description="Source of irrigation water")
    season = Column(SAEnum(Season))
    water_use_efficiency = Column(Float)
    drought_prone = Column(Boolean, default=False)
    recommended_irrigation_method = Column(String)
    water_quality_notes = Column(String)
    region_states = Column(String)
    avg_water_cost_per_ha = Column(Float)
    extra_info = Column(String)

    # Relationships with Crop model
    crop = relationship("Crop", back_populates="water_dependencies")
