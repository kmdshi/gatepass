from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union


class PersonBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True

class PersonCreate(PersonBase):
    password: str


class Person(PersonBase):
    id: int
    organization_id: Optional[int]

    class Config:
        from_attributes = True
