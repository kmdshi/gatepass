from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.db import get_db
from app.models.person import Person
from app.schemas import person, token
from typing import Annotated, List
from passlib.context import CryptContext
from app.utils.auth import create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from app.models.organization import Organization
from app.crud.person_crud import *


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/persons/", response_model=token.Token)
def create_person(person: person.PersonCreate, db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(person.password)

    access_token = create_access_token(data={
        "first_name": person.first_name,
        "last_name": person.last_name,
        "email": person.email
    })

    refresh_token = create_refresh_token(data={
        "first_name": person.first_name,
        "last_name": person.last_name,
        "email": person.email
    })

    db_create_person(db, person.first_name, person.last_name,
                     person.email, hashed_password, access_token, refresh_token)

    answer = token.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='Bearer'
    )

    return answer


@router.get("/persons/", response_model=List[person.Person])
def get_all_persons(db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    return db_get_all_persons(db)


@router.get("/persons/{person_id}", response_model=person.Person)
def get_person(person_id: int, db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    return get_person_by_id(db, person_id)
