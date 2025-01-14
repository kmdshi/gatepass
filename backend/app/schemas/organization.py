from pydantic import BaseModel
from typing import List, Optional
from app.schemas.person import Person

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    persons: List[Person] = []

    class Config:
        from_attributes  = True
