from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.satellite import Satellite
from app.models.user import User
from app.routes.satellites import router as satellite_router
from app.routes.auth import router as auth_router
from app.models.document import Document
from app.routes.ask import router as ask_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ANTELLAY Space Intelligence API",
    version="1.0.0",
    description="Mini Space Intelligence API"
)


# Register routers
app.include_router(satellite_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "ANTELLAY Space Intelligence API is running"
    }

app.include_router(ask_router)