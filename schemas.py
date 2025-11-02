from pydantic import BaseModel, Field, field_validator, computed_field, StrictInt
from typing import Annotated, Optional

class CarBase(BaseModel):
    name: Annotated[str, Field(..., min_length=3)]
    price: Annotated[float, Field(..., ge=0)]

    @field_validator('name')
    @classmethod
    def name_title(cls, value) -> str:
        return value.upper()
    
    @computed_field
    @property
    def price_rs(self) -> float:
        return self.price*85
    
class CarCreate(CarBase):
    pass 

class CarUpdate(CarBase):
    name: Annotated[Optional[str], Field(None, min_length=3)]
    price: Annotated[Optional[float], Field(None, ge=0)]

    @field_validator('name')
    @classmethod
    def name_title(cls, value) -> str:
        return value.upper() if value else value
    
    @computed_field
    @property
    def price_rs(cls) -> float:
        return cls.price*85 if cls.price else cls.price


class CarOut(CarBase):
    id: int

    class Config:
        from_attributes = True

class PredictionInputSchema(BaseModel):
    Model_Year: Annotated[StrictInt, Field(..., gt=1950,le=2026,description='Manufacture year of car')]
    Mileage: Annotated[int, Field(...,ge=0, description='Miles driven by the car')]
    Accidents_or_Damage: Annotated[bool, Field(..., description='whether car meet any accident or not (True or False)')]
    Clean_Title: Annotated[bool, Field(..., description='Car has Clean title or not (True or False)')]
    One_Owner_Vehicle: Annotated[bool, Field(..., description='Car is owner by more than 1 person or not? (True or False)')]

class PredictionOutputSchema(BaseModel):
    Price: Annotated[float, Field(...,ge=0, description='Price Predicted by model')]