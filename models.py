from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Reservations(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=False)
    availability_id = Column(Integer, ForeignKey("availabilities.id"))
    availability = relationship("Availabilities", back_populates="reservation")
    title = Column(String)
    start = Column(Time)
    end = Column(Time)
    email = Column(String)


class Availabilities(Base):
    __tablename__ = "availabilities"
    id = Column(Integer, primary_key=True, index=False)
    is_available = Column(Integer, default=0)
    start = Column(Time)
    end = Column(Time)
    reservation = relationship("Reservations", uselist=False, back_populates="availability")
