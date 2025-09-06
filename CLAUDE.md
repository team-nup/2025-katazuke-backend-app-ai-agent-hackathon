# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based Google Cloud Run backend resource project for a 2025 EDD (Employment Development Department) hackathon. The project provides a high-performance, async API service optimized for Cloud Run deployment.

## Development Commands

### Local Development
- **Build Docker image**: `./local-test.sh build`
- **Run locally**: `./local-test.sh run` (starts container on port 8080)
- **Test endpoints**: `./local-test.sh test`
- **Stop container**: `./local-test.sh stop`
- **View logs**: `./local-test.sh logs`
- **Full test cycle**: `./local-test.sh` (build + run + test)

### Python Direct Development
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Cloud Run Deployment
- **Deploy to Cloud Run**: `./deploy.sh [PROJECT_ID] [REGION] [SERVICE_NAME]`
- **Default deploy**: `./deploy.sh` (uses default project settings)

## Architecture

### Core Structure
```
app/
├── main.py              # FastAPI application with CORS, exception handling
├── routers/
    └── health.py        # Health check endpoints for K8s-style probes
```

### Key Components
- **FastAPI**: Async Python web framework with automatic API documentation
- **Health Checks**: Liveness/readiness probes for Cloud Run
- **CORS**: Configured for cross-origin requests  
- **Error Handling**: Global exception handler for production safety
- **Docker**: Multi-stage build with non-root user for security

### API Endpoints
- `/` - Root endpoint with service info
- `/api/v1/info` - Detailed API information
- `/api/v1/health/` - Basic health check
- `/api/v1/health/liveness` - Liveness probe
- `/api/v1/health/readiness` - Readiness probe  
- `/api/v1/health/detailed` - Detailed health with system info
- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation

### Environment Variables
- `PORT`: Cloud Run automatically sets this (default: 8080)
- `PYTHON_VERSION`: Python version info for health checks

## Development Notes

- FastAPI uses async/await patterns - maintain async consistency
- Health endpoints are crucial for Cloud Run deployment
- Docker builds use Python 3.11 slim with multi-stage optimization
- Non-root user execution for security
- Port 8080 is Cloud Run standard and configured in Dockerfile
- Requirements.txt includes production-ready FastAPI stack with uvicorn ASGI server