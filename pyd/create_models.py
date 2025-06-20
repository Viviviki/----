from pydantic import BaseModel, Field
from datetime import date, datetime
import re
import decimal

class CreateCar(BaseModel):
    year:int=Field(example=2011)
    price_per_day:decimal=Field(example=200)

class CreateReview(BaseModel):
    rating:float=Field(example=4.5, ge=0, le=5)
    description:str|None=Field(example="Лада лучшая", default=None)
    car_id:int=Field(example=1)
    user_id:int=Field(example=1)

class CreateRent(BaseModel):
    start_date:date=Field(example="2025-06-21")
    end_date:date=Field(example="2025-06-24")
    cost:decimal=Field(example=1000)
    user_id:int=Field(example=1)
    car_id:int=Field(example=1)
    status_id:int=Field(example=1)
