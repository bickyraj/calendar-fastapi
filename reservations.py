from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
import models
from datetime import datetime, time

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


class Reservation(BaseModel):
    title: str = Field(min_length=1)
    email: EmailStr
    start: time
    end: time
    created_at: datetime = Field(default_factory=datetime.now)
    availability_id: int

    # @field_validator("email")
    # def validate_email(cls, value: str, info: FieldValidationInfo) -> str:
    #     if "admin" in value:
    #         raise ValueError("This email is not allowed")
    #     return value
