from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import organization
from typing import Annotated, List
from passlib.context import CryptContext
from app.models.organization import Organization
from sqlalchemy import or_
from sqlalchemy import update
from app.schemas.person import Person
from app.models.person import Person as dbPerson
from app.utils.auth import get_current_user
from app.crud.organization_crud import *

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/organizations/", response_model=organization.Organization)
def create_organization(organization: organization.OrganizationCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(organization.password)
    return db_create_organization(db, organization.title, organization.email,
                                  hashed_password, organization.head_person)


@router.get("/organizations/", response_model=List[organization.Organization])
def get_all_organizations(db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    return db_get_all_organizations(db)


@router.get("/organizations/{organization_title}", response_model=organization.Organization)
def get_organization(
    organization_title: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db_get_all_organization_by_title(db, organization_title)
