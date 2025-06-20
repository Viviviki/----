from .base_models import *
from typing import List

class SchemeCar(BaseCar):
    mark: BaseMark
    model: BaseModel
    type: BaseType
    status: BaseStatus

class SchemeReview(BaseReview):
    user: BaseUser
    car: SchemeCar

class SchemeRent(BaseRent):
    user: BaseUser
    car: SchemeCar
    status: BaseStatus

class SchemeUser(BaseUser):
    role: BaseRole