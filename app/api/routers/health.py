import logging
import os
import time
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check() -> dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "EDD Cloud Run Backend Resource",
        "version": "1.0.0",
    }


@router.get("/liveness")
async def liveness_probe() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/readiness")
async def readiness_probe() -> dict[str, Any]:
    try:
        current_time = time.time()
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": current_time,
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready") from e


@router.get("/detailed")
async def detailed_health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": {
            "name": "EDD Cloud Run Backend Resource",
            "version": "1.0.0",
            "description": "Employment Development Department backend resource for hackathon 2025",
        },
        "environment": {
            "port": os.getenv("PORT", "8080"),
            "python_version": os.getenv("PYTHON_VERSION", "3.11"),
        },
        "system": {"uptime_seconds": time.time()},
    }
