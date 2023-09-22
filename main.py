from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import reservation_router, availability_router


app = FastAPI(
    title="Calendar",
    version="1.0.0",
    description="a basic application to book a meeting",
    openapi_url="/docs.json",  # Optional: Change the URL for the OpenAPI JSON
    redoc_url=None  # Optional: Disable ReDoc documentation
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reservation_router.router, prefix="/reservations", tags=["reservations"])
app.include_router(availability_router.router, prefix="/availabilities", tags=["availabilities"])