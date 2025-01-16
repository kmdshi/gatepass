from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.person import Person


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    current_qr = Column(String)
    hash = Column(String)


    head_person_id = Column(Integer, ForeignKey('persons.id'))
    head_person = relationship(
        "Person", backref="organization_head", foreign_keys=[head_person_id], remote_side=[Person.id]
    )

    persons = relationship(
        "Person",
        back_populates="organization",
        foreign_keys=[Person.organization_id],
    )
