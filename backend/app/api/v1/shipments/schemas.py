from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class WeightUnit(str, Enum):
    KG = "kg"
    LBS = "lbs"

class ShipmentType(str, Enum):
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"

class Address(BaseModel):
    street: Optional[str] = None
    city: str = Field(..., description="City name")
    state_province: Optional[str] = None
    country: str = Field(..., description="ISO 2-letter country code or full country name")
    postal_code: Optional[str] = None

class ShipmentRequest(BaseModel):
    origin: Address
    destination: Address
    weight: float = Field(..., gt=0, description="Package weight")
    weight_unit: WeightUnit = Field(default=WeightUnit.KG)
    shipment_type: ShipmentType = Field(default=ShipmentType.DOMESTIC)
    declared_value_usd: Optional[float] = None
    special_handling: List[str] = Field(default_factory=list)

class CarrierQuote(BaseModel):
    carrier_name: str
    service_level: str
    rate_usd: float
    estimated_days: int
    delivery_date: str
