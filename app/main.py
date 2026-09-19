from fastapi import FastAPI

from app.database.database import Base, engine, SessionLocal
from app.models.satellite import Satellite
from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.routes.satellites import router as satellite_router
from app.routes.auth import router as auth_router
from app.routes.ask import router as ask_router

from rag.ingestion import ingest_documents


# Create database tables
Base.metadata.create_all(bind=engine)


# Automatically load knowledge base documents and chunks
try:
    ingest_documents()
except Exception as e:
    print(f"Knowledge base ingestion warning: {e}")


app = FastAPI(
    title="ANTELLAY Space Intelligence API",
    version="1.0.0",
    description="Mini Space Intelligence API"
)


# Register routers
app.include_router(satellite_router)
app.include_router(auth_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {
        "message": "ANTELLAY Space Intelligence API is running"
    }