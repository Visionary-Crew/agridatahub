from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from app.models.water_dependency import WaterDependency

class CropType(str, Enum):
    food = "Food"
    cash = "Cash"
    oilseed = "Oilseed"
    pulse = "Pulse"
    horticultural = "Horticultural"
    spices = "Spices"

class Season(str, Enum):
    kharif = "Kharif"
    rabi = "Rabi"
    zaid = "Zaid"
    perennial = "Perennial"

class IrrigationNeeds(str, Enum):
    rainfed = "Rainfed"
    irrigated = "Irrigated"
    both = "Both"

class CropMOdel(BaseModel
):
    name: str
    scientific_name: Optional[str] = None
    crop_type: CropType
    season: Season
    sowing_period: Optional[str] = None
    harvesting_period: Optional[str] = None
    duration_days: Optional[int] = None
    climate_preference: Optional[str] = None
    avg_temp_min_c: Optional[float] = None
    avg_temp_max_c: Optional[float] = None
    avg_rainfall_min_mm: Optional[float] = None
    avg_rainfall_max_mm: Optional[float] = None
    soil_types: Optional[str] = None
    ph_range: Optional[str] = None
    nutrient_n: Optional[float] = None
    nutrient_p: Optional[float] = None
    nutrient_k: Optional[float] = None
    major_states: Optional[str] = None
    yield_q_per_ha: Optional[float] = None
    irrigation_needs: Optional[IrrigationNeeds] = None
    recommended_varieties: Optional[str] = None
    diseases: Optional[str] = None
    pests: Optional[str] = None
    market_value: Optional[float] = None
    other_uses: Optional[str] = None
    image_url: Optional[str] = None
    extra_info: Optional[str] = None

    # Nest water dependencies as a list of WaterDependency (optional)
    water_dependencies: Optional[List[WaterDependency]] = None
