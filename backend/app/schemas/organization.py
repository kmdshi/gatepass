from pydantic import BaseModel
from typing import List, Optional
from app.schemas.person import Person

from typing import List
from pydantic import BaseModel, EmailStr


class OrganizationBase(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    persons: List[Person] = []


class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int

    class Config:
        from_attributes = True
