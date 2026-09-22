from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import Base, engine
from app.models.satellite import Satellite
from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.routes.satellites import router as satellite_router
from app.routes.auth import router as auth_router
from app.routes.ask import router as ask_router

from app.core.exceptions import (
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler,
)

from rag.ingestion import ingest_documents
import logging
import time
import uuid


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

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("antellay-space-ai")


@app.middleware("http")
async def request_logging_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    logger.info(
        "%s %s - Status: %s - Request-ID: %s - Time: %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        request_id,
        process_time
    )

    return response

# Global exception handlers
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


# API v1 routers
API_VERSION = "v1"
API_V1_PREFIX = f"/api/{API_VERSION}"

app.include_router(
    satellite_router,
    prefix=API_V1_PREFIX
)

app.include_router(
    auth_router,
    prefix=API_V1_PREFIX
)

app.include_router(
    ask_router,
    prefix=API_V1_PREFIX
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "ANTELLAY Space Intelligence API is running",
        "api_version": API_VERSION,
        "docs": "/docs",
        "api_base_url": f"/api/{API_VERSION}"
    }