from sqlalchemy import Column, Integer, String
from database import Base


class Reservations(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=False)
    title = Column(String)
    start = Column(String)
    end = Column(String)
    email = Column(String)