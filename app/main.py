import logging
import os
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers import gemini, health, vision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EDD Cloud Run Backend Resource API",
    description="Employment Development Department backend resource for hackathon 2025",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(vision.router)
app.include_router(gemini.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "EDD Cloud Run Backend Resource API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/api/v1/info")
async def get_api_info() -> dict[str, Any]:
    return {
        "api_name": "EDD Cloud Run Backend Resource API",
        "version": "1.0.0",
        "description": "Employment Development Department backend resource for hackathon 2025",
        "endpoints": {
            "root": "/",
            "health": "/api/v1/health",
            "info": "/api/v1/info",
            "vision_web_detection": "/api/v1/vision/web-detection",
            "vision_health": "/api/v1/vision/health",
            "gemini_analyze": "/api/v1/gemini/analyze",
            "gemini_health": "/api/v1/gemini/health",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }


@app.exception_handler(Exception)
async def global_exception_handler(_request, exc):
    logger.error(f"Global exception handler: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    # 開発環境のみで使用（本番環境では外部から起動される）
    host = os.getenv("HOST", "127.0.0.1")  # ローカル開発用
    logger.info(f"Starting development server on {host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
