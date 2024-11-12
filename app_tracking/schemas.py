from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusEnum(Enum):
    active = "active"
    inactive = "inactive"

# Pydantic model for Tracking_Product
class TrackingProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_available: Optional[bool] = True

class TrackingProductCreate(TrackingProductBase):
    pass

class TrackingProduct(TrackingProductBase):
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Permite que los modelos de Pydantic se integren con SQLAlchemy

# Pydantic model for Tracking_Station
class TrackingStationBase(BaseModel):
    name: str

class TrackingStationCreate(TrackingStationBase):
    pass

class TrackingStation(TrackingStationBase):
    station_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Pydantic model for Tracking_Zone
class TrackingZoneBase(BaseModel):
    name: str
    canvas_x: int
    canvas_y: int
    canvas_width: Optional[int] = 100
    canvas_height: Optional[int] = 50
    next_zone: Optional[int] = None
    preview_zone: Optional[int] = None
    station_id: int

class TrackingZoneCreate(TrackingZoneBase):
    pass

class TrackingZone(TrackingZoneBase):
    zone_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Pydantic model for Tracking (Tracking movements)
class TrackingBase(BaseModel):
    product_id: int
    zone_id: int

class TrackingCreate(TrackingBase):
    pass

class Tracking(TrackingBase):
    tracking_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



## ----------- EXAMPLE -------------
#from pydantic import BaseModel
#from enum import Enum
#
#class StatusEnum(Enum):
#    active = "active"
#    inactive = "inactive"
#
#class ItemBase(BaseModel):
#    title: str
#    description: str | None = None
#
#class Item(ItemBase):
#    id: int
#    status: StatusEnum
#
#    class Config:
#        orm_mode = True
#        use_enum_values = True
#        min_anystr_length = 3
#        max_anystr_length = 100
#        anystr_strip_whitespace = True
#        json_encoders = {
#            datetime: lambda v: v.isoformat(),
#        }
#        allow_population_by_field_name = True
