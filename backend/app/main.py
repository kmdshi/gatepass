from fastapi import FastAPI
from app.routers.person import router as person_router
import uvicorn

app = FastAPI()

app.include_router(person_router)
