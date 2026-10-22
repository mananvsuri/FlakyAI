"""FlakeGuard AI - Main FastAPI Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.core.config import settings
from app.core.database import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="An Explainable AI Framework for Flaky Test Detection in CI/CD Pipelines",
)

# CORS middleware - allow all localhost ports for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": "FlakeGuard AI"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "FlakeGuard AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# API routes
from app.api import datasets, predictions
app.include_router(datasets.router, prefix=f"{settings.API_V1_PREFIX}/datasets", tags=["datasets"])
app.include_router(predictions.router, prefix=f"{settings.API_V1_PREFIX}/predictions", tags=["predictions"])
