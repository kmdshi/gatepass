from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    jwt = Column(String)
    refresh_token = Column(String)

    organization_id = Column(Integer, ForeignKey(
        "organizations.id"), nullable=True)

    organization = relationship(
        "Organization", back_populates="persons", foreign_keys=[organization_id])
