from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
import models
from datetime import datetime, time, date

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


class Availability(BaseModel):
    start: time
    end: time
    is_available: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
