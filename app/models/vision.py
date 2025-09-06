from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Feature(BaseModel):
    """Vision API機能指定"""
    type: str = Field(..., description="検出タイプ (WEB_DETECTION等)")
    maxResults: Optional[int] = Field(None, description="最大結果数")


class Image(BaseModel):
    """画像データ（Base64エンコードのみサポート）"""
    content: str = Field(..., description="Base64エンコードされた画像データ")


class VisionRequest(BaseModel):
    """Vision APIリクエスト"""
    image: Image
    features: List[Feature]


class VisionBatchRequest(BaseModel):
    """Vision APIバッチリクエスト"""
    requests: List[VisionRequest]


class WebEntity(BaseModel):
    """Web検出エンティティ"""
    entityId: Optional[str] = None
    score: Optional[float] = None
    description: Optional[str] = None


class WebImage(BaseModel):
    """Web画像"""
    url: Optional[str] = None


class WebPage(BaseModel):
    """Webページ情報"""
    url: Optional[str] = None
    pageTitle: Optional[str] = None
    fullMatchingImages: List[WebImage] = []
    partialMatchingImages: List[WebImage] = []


class BestGuessLabel(BaseModel):
    """推測ラベル"""
    label: Optional[str] = None
    languageCode: Optional[str] = None


class WebDetection(BaseModel):
    """Web検出結果"""
    webEntities: List[WebEntity] = []
    fullMatchingImages: List[WebImage] = []
    partialMatchingImages: List[WebImage] = []
    pagesWithMatchingImages: List[WebPage] = []
    visuallySimilarImages: List[WebImage] = []
    bestGuessLabels: List[BestGuessLabel] = []


class ErrorInfo(BaseModel):
    """エラー情報"""
    code: int
    message: str


class VisionResponse(BaseModel):
    """Vision APIレスポンス"""
    webDetection: Optional[WebDetection] = None
    error: Optional[ErrorInfo] = None


class VisionBatchResponse(BaseModel):
    """Vision APIバッチレスポンス"""
    responses: List[VisionResponse]