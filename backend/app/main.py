from fastapi import FastAPI
from app.routers.person import router as person_router
from app.routers.organization import router as organization_router
from app.db.database import Base, engine
from sqlalchemy.exc import OperationalError
from app.models import Organization, Person

app = FastAPI()


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")


init_db()

app.include_router(person_router)
app.include_router(organization_router)
