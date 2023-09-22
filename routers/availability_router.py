from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from availabilities import Availability

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Availabilities).all()


@router.get("/{availability_id}")
def get_reservation(availability_id: int, db: Session = Depends(get_db)):
    data_model = db.query(models.Availabilities).filter(models.Availabilities.id == availability_id).first()
    return data_model


@router.post("/")
def create_reservation(availability: Availability, db: Session = Depends(get_db)):
    data_model = models.Availabilities()
    data_model.start = availability.start
    data_model.end = availability.end

    db.add(data_model)
    db.commit()

    return availability


@router.put("/{availability_id}")
def update_reservation(availability_id: int, availability: Availability, db: Session = Depends(get_db)):
    data_model = db.query(models.Availabilities).filter(models.Availabilities.id == availability_id).first()
    if data_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {availability_id} : Reservation does not exist"
        )

    data_model.start = availability.start
    data_model.end = availability.end

    db.add(data_model)
    db.commit()

    return availability


@router.delete("/{availability_id}")
def delete_reservation(availability_id: int, db: Session = Depends(get_db)):
    data_model = db.query(models.Availabilities).filter(models.Availabilities.id == availability_id).first()
    if data_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {availability_id} : Reservation does not exist"
        )

    # test

    db.query(models.Availabilities).filter(models.Availabilities.id == availability_id).delete()
    db.commit()
