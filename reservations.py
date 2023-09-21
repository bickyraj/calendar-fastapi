from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
import models

from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(
    title="Calendar",
    version="1.0.0",
    description="a basic application to book a meeting",
    openapi_url="/docs.json",  # Optional: Change the URL for the OpenAPI JSON
    redoc_url=None  # Optional: Disable ReDoc documentation
)
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Reservation(BaseModel):
    title: str = Field(min_length=1)
    email: str = Field(min_length=1)
    start: str = Field(min_length=1)
    end: str = Field(min_length=1)


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Reservations).all()


@app.post("/")
def create_reservation(reservation: Reservation, db: Session = Depends(get_db)):
    reservation_model = models.Reservations()
    reservation_model.title = reservation.title
    reservation_model.email = reservation.email
    reservation_model.start = reservation.start
    reservation_model.end = reservation.end

    db.add(reservation_model)
    db.commit()

    return reservation


@app.put("/{reservation_id}")
def update_reservation(reservation_id: int, reservation: Reservation, db: Session = Depends(get_db)):
    reservation_model = db.query(models.Reservations).filter(models.Reservations.id == reservation_id).first()
    if reservation_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {reservation_id} : Reservation does not exist"
        )

    reservation_model.title = reservation.title
    reservation_model.start = reservation.start
    reservation_model.end = reservation.end
    reservation_model.email = reservation.email

    db.add(reservation_model)
    db.commit()

    return reservation


@app.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_model = db.query(models.Reservations).filter(models.Reservations.id == reservation_id).first()
    if reservation_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {reservation_id} : Reservation does not exist"
        )

    db.query(models.Reservations).filter(models.Reservations.id == reservation_id).delete()
    db.commit()
