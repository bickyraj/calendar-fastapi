from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from reservations import Reservation

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Reservations).all()


@router.get("/{reservation_id}")
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_model = db.query(models.Reservations).filter(models.Reservations.id == reservation_id).first()
    return reservation_model



@router.post("/")
def create_reservation(reservation: Reservation, db: Session = Depends(get_db)):
    availability = db.query(models.Availabilities).filter(models.Availabilities.id == reservation.availability_id).first()
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    reservation_model = models.Reservations()
    reservation_model.title = reservation.title
    reservation_model.email = reservation.email
    reservation_model.start = reservation.start
    reservation_model.end = reservation.end
    reservation_model.availability_id = reservation.availability_id
    db.add(reservation_model)
    db.commit()

    availability.is_available = 1
    db.add(availability)
    db.commit()

    return reservation


@router.put("/{reservation_id}")
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


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_model = db.query(models.Reservations).filter(models.Reservations.id == reservation_id).first()
    if reservation_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {reservation_id} : Reservation does not exist"
        )

    db.query(models.Reservations).filter(models.Reservations.id == reservation_id).delete()
    db.commit()
