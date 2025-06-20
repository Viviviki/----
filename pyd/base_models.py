from pydantic import BaseModel, Field
from datetime import date
import decimal

class BaseCar(BaseModel):
    id:int=Field(example=1)
    year:int=Field(example=2011)
    price_per_day:decimal=Field(example=200)

class BaseMark(BaseModel):
    id:int=Field(example=1)
    name_mark:str=Field(example="Лада")

class BaseModel(BaseModel):
    id:int=Field(example=1)
    name_model:str=Field(example="Гранта")

class BaseType(BaseModel):
    id:int=Field(example=1)
    name_type:str=Field(example="Седан")

class BaseRent(BaseModel):
    id:int=Field(example=1)
    start_date:date=Field(example="2025-06-21")
    end_date:date=Field(example="2025-06-24")
    cost:decimal=Field(example=1000)


class BaseUser(BaseModel):
    id:int=Field(example=1)
    firstname:str=Field(example="Иван")
    lastname:str=Field(example="Иванов")
    username:str=Field(example="1v4n")


class BaseRole(BaseModel):
    id:int=Field(example=1)
    role_name:str=Field(example="Клиент")

class BaseStatus(BaseModel):
    id:int=Field(example=1)
    status_name:str=Field(example="Доступен")


class BaseReview(BaseModel):
    id:int=Field(example=1)
    rating:float=Field(example=4.5)
    description:str|None=Field(example="Лада крутая")
