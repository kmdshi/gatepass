from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.db import get_db
from app.models.person import Person
from app.schemas import person, token
from typing import Annotated, List
from passlib.context import CryptContext
from app.utils.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/persons/", response_model=person.Person)
def create_person(person: person.PersonCreate, db: Session = Depends(get_db)):
    existing_person = db.query(Person).filter(
        Person.email == person.email).first()

    if existing_person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    else:
        hashed_password = pwd_context.hash(person.password_hash)
        db_person = Person(first_name=person.first_name, last_name=person.last_name,
                           email=person.email, password_hash=hashed_password, organization_id=person.organization_id)
        db.add(db_person)
        db.commit()
        db.refresh(db_person)
        return db_person


@router.get("/persons/", response_model=List[person.Person])
def get_all_persons(db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    db_persons = db.query(Person).all()
    return db_persons


@router.get("/persons/{person_id}", response_model=person.Person)
def get_person(person_id: int, db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@router.post("/token", response_model=token.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = db.query(Person).filter(
        Person.email == form_data.username).first()
    if db_user is None or not pwd_context.verify(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
