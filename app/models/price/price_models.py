from pydantic import BaseModel
from datetime import date
from typing import Optional


class MarketPriceDataModel(BaseModel):
    State: str
    District: str
    Market: str
    Commodity: str
    Variety: Optional[str] = None
    Grade: Optional[str] = None
    Arrival_Date: date
    Min_x0020_Price: Optional[float] = None
    Max_x0020_Price: Optional[float] = None
    Modal_x0020_Price: Optional[float] = None
