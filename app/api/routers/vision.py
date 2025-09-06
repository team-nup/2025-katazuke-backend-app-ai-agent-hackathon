from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from app.models.vision import VisionBatchRequest, VisionBatchResponse
from app.services.vision_service import VisionService

router = APIRouter(prefix="/api/v1/vision", tags=["vision"])


def get_vision_service() -> VisionService:
    """Vision Serviceの依存性注入"""
    return VisionService()


@router.post("/web-detection", response_model=VisionBatchResponse)
async def web_detection(
    request: VisionBatchRequest,
    vision_service: VisionService = Depends(get_vision_service)
) -> VisionBatchResponse:
    """
    Cloud Vision APIのWeb Detection機能を使用して画像解析を行う
    
    Base64エンコードされた画像データのみサポート
    """
    return await vision_service.web_detection(request)


@router.get("/health")
async def vision_health(
    vision_service: VisionService = Depends(get_vision_service)
) -> Dict[str, Any]:
    """Vision APIの接続確認"""
    is_healthy = vision_service.health_check()
    
    if not is_healthy:
        raise HTTPException(
            status_code=503, 
            detail="Vision API接続エラー"
        )
    
    return {
        "status": "healthy", 
        "service": "Google Cloud Vision API"
    }