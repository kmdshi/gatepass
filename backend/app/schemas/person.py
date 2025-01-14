from pydantic import BaseModel
from typing import List, Optional, Union


class PersonBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password_hash: str
    organization_id: Optional[int]


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True
