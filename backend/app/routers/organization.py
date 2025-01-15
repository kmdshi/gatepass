from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import organization
from typing import Annotated, List
from passlib.context import CryptContext
from app.models.organization import Organization
from sqlalchemy import or_

from app.schemas.person import Person
from app.utils.auth import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/organization/", response_model=organization.Organization)
def crete_organization(organization:  organization.OrganizationCreate, db: Session = Depends(get_db)):
    existing_organization = db.query(Organization).filter(
        or_(Organization.name == organization.name,
            Organization.email == organization.email)
    ).first()

    if existing_organization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization already exists"
        )
    else:
        hashed_password = pwd_context.hash(organization.password_hash)
        db_organization = Organization(
            name=organization.name, email=organization.email, hashed_password=hashed_password)
        db.add(db_organization)
        db.commit()
        db.refresh(db_organization)
        return db_organization


@router.get("/organizations/", response_model=List[organization.Organization])
def get_all_organizations(db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    db_organizations = db.query(Organization).all()
    return db_organizations


@router.get("/organizations/{organization_name}", response_model=organization.Organization)
def get_organizations(organization_name: str, db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):

    db_person = db.query(Organization).filter(
        Organization.name == organization_name).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_person
