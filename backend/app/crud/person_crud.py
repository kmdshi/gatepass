from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.models.person import Person


def db_create_person(db: Session, first_name: str, last_name: str, email: EmailStr, password_hash: str, jwt: str, refresh: str):
    existing_person = db.query(Person).filter(
        Person.email == email).first()

    if existing_person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    db_person = Person(first_name=first_name, last_name=last_name,
                       email=email, password_hash=password_hash, jwt=jwt, refresh_token=refresh)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)


def db_get_all_persons(db: Session):
    return db.query(Person).all()


def db_add_person_in_organization(db: Session, person_id: int, organization_id: int):
    db_person = db.query(Person).filter(Person.id == person_id).first()

    if db_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_person.organization_id = organization_id

    db.commit()
    db.refresh(db_person)

    return db_person

def get_person_by_id(db: Session, id: int):
    db_person = db.query(Person).filter(Person.id == id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


def delete_person_by_id(db: Session, id: int):
    db_person = db.query(Person).filter(Person.id == id).first()

    if not db_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {id} not found"
        )

    db.delete(db_person)
    db.commit()

    return {"detail": f"Person with id {id} has been deleted successfully"}


def update_person_by_id(
    db: Session,
    id: int,
    new_first_name: Optional[str] = None,
    new_last_name: Optional[str] = None,
    new_email: Optional[EmailStr] = None,
    new_password_hash: Optional[str] = None
):
    db_person = db.query(Person).filter(Person.id == id).first()

    if not db_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {id} not found"
        )
    if new_first_name:
        db_person.first_name = new_first_name
    if new_last_name:
        db_person.last_name = new_last_name
    if new_email:
        db_person.email = new_email
    if new_password_hash:
        db_person.password_hash = new_password_hash

    db.commit()
    db.refresh(db_person)

    return db_person
