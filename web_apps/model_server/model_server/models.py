from typing import Union
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr


class AddressIn(BaseModel):
    address_string: str
    country_code: str

class GeoOut(BaseModel):
    latitude: float
    longitude: float
