import logging
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import or_, update
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models.organization import Organization
from app.models.person import Person
from sqlalchemy.exc import SQLAlchemyError
from app.utils.crypto import generate_hash

logger = logging.getLogger(__name__)


def db_create_organization(db: Session, title: str, email: EmailStr, hashed_password: str, head_person: Person):
    logger.info(f"Creating organization: {title}")

    existing_organization = db.query(Organization).filter(
        or_(Organization.title == title, Organization.email == email)
    ).first()

    head_person_record = db.query(Person).filter(
        Person.id == head_person.id).first()

    if not head_person_record:
        logger.error(f"Head person with ID {head_person.id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Head person not found"
        )

    if existing_organization:
        logger.warning(
            f"Organization with title '{title}' or email '{email}' already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this title or email already exists"
        )

    org_hash = generate_hash(title, email)

    db_organization = Organization(
        title=title,
        email=email,
        hashed_password=hashed_password,
        head_person_id=head_person.id,
        hash=org_hash
    )

    db.add(db_organization)

    try:
        db.commit()
        logger.info(
            f"Organization '{title}' created successfully with ID {db_organization.id}")

        db.execute(
            update(Person)
            .where(Person.id == head_person.id)
            .values(organization_id=db_organization.id)
        )
        db.commit()

        db.refresh(db_organization)
        return db_organization

    except SQLAlchemyError as e:
        logger.error(f"Error creating organization '{title}': {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}"
        )


def db_get_all_organizations(db: Session):
    logger.info(f"Fetching all organizations")
    return db.query(Organization).all()


def db_get_all_organization_by_title(db: Session, organization_title: str):
    logger.info(
        f"Searching for organizations with title starting with '{organization_title}'")
    db_organizations = db.query(Organization).filter(
        Organization.title.ilike(f"{organization_title}%")
    ).all()

    if not db_organizations:
        logger.warning(
            f"No organizations found with title prefix: {organization_title}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No organizations found with the given title prefix"
        )

    return db_organizations


def db_get_all_users_in_organization(db: Session, organization_id: int):
    logger.info(f"Fetching users for organization ID {organization_id}")

    db_organization = db.query(Organization).filter(
        Organization.id == organization_id).first()

    if not db_organization:
        logger.error(f"Organization with ID {organization_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {organization_id} not found"
        )

    db_head_person = db.query(Person).filter(
        Person.id == db_organization.head_person_id).first()

    return {
        "head": db_head_person,
        "users": db_organization.persons
    }


def update_organization_by_id(
    db: Session,
    organization_id: int,
    title: Optional[str] = None,
    new_email: Optional[EmailStr] = None,
    new_password_hash: Optional[str] = None
):
    logger.info(f"Updating organization ID {organization_id}")

    db_organization = db.query(Organization).filter(
        Organization.id == organization_id).first()

    if not db_organization:
        logger.error(f"Organization with ID {organization_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {organization_id} not found"
        )

    if title:
        db_organization.title = title
    if new_email:
        db_organization.email = new_email
    if new_password_hash:
        db_organization.hashed_password = new_password_hash

    db.commit()
    db.refresh(db_organization)

    logger.info(f"Organization ID {organization_id} updated successfully")
    return db_organization
