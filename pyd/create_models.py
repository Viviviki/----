from pydantic import BaseModel, Field
from datetime import date, datetime
import re
import decimal

class CreateCar(BaseModel):
    year:int=Field(example=2011)
    mark_id:int=Field(example=1)
    model_id:int=Field(example=1)
    type_id:int=Field(example=1)
    price_per_day:float=Field(example=200)
    status_id:int=Field(example=1)

class CreateReview(BaseModel):
    rating:float=Field(example=4.5, ge=0, le=5)
    description:str|None=Field(example="Лада лучшая", default=None)
    car_id:int=Field(example=1)
    user_id:int=Field(example=1)

class CreateRent(BaseModel):
    start_date:date=Field(example="2025-06-21")
    end_date:date=Field(example="2025-06-24")
    cost:float=Field(example=1000)
    user_id:int=Field(example=1)
    car_id:int=Field(example=1)
    status_id:int=Field(example=1)

class CreateUser(BaseModel):
    firstname:str=Field(example="Иван", min_length=2)
    lastname:str=Field(example="Иванов", min_length=2)
    username:str=Field(example="1v4n", min_length=2, max_length=20)
    password:str=Field(example="1v4n", min_length=8, max_length=20, pattern=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"))

class LoginUser(BaseModel):
    username:str=Field(example="1v4n", min_length=2, max_length=20)
    password:str=Field(example="1v4n", min_length=8, max_length=20, pattern=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"))
