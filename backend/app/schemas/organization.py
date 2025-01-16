from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from app.schemas.person import Person, PersonBase

from typing import List
from pydantic import BaseModel, EmailStr


class OrganizationBase(BaseModel):
    title: str
    email: EmailStr


class OrganizationCreate(OrganizationBase):
    password: str
    head_person: Person


class Organization(OrganizationBase):
    id: int
    head_person: Person
    persons: List[Person] = []

    class Config:
        from_attributes = True

class OrganizationPerson(OrganizationBase):
    id: int
    head_person: Person
    persons: List[Person] = []

    class Config:
        from_attributes = True

class OrganizationHead(OrganizationBase):
    id: int
    head_person: Person
    persons: List[Person] = []
    hashed_pass: str

    class Config:
        from_attributes = True