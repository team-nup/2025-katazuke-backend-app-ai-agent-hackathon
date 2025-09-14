from pydantic import BaseModel, Field


class Feature(BaseModel):
    """Vision API機能指定"""

    type: str = Field(..., description="検出タイプ (WEB_DETECTION等)")
    maxResults: int | None = Field(None, description="最大結果数")


class Image(BaseModel):
    """画像データ（Base64エンコードのみサポート）"""

    content: str = Field(..., description="Base64エンコードされた画像データ")


class VisionRequest(BaseModel):
    """Vision APIリクエスト"""

    image: Image
    features: list[Feature]


class VisionBatchRequest(BaseModel):
    """Vision APIバッチリクエスト"""

    requests: list[VisionRequest]


class WebEntity(BaseModel):
    """Web検出エンティティ"""

    entityId: str | None = None
    score: float | None = None
    description: str | None = None


class WebImage(BaseModel):
    """Web画像"""

    url: str | None = None


class WebPage(BaseModel):
    """Webページ情報"""

    url: str | None = None
    pageTitle: str | None = None
    fullMatchingImages: list[WebImage] = []
    partialMatchingImages: list[WebImage] = []


class BestGuessLabel(BaseModel):
    """推測ラベル"""

    label: str | None = None
    languageCode: str | None = None


class WebDetection(BaseModel):
    """Web検出結果"""

    webEntities: list[WebEntity] = []
    fullMatchingImages: list[WebImage] = []
    partialMatchingImages: list[WebImage] = []
    pagesWithMatchingImages: list[WebPage] = []
    visuallySimilarImages: list[WebImage] = []
    bestGuessLabels: list[BestGuessLabel] = []


class ErrorInfo(BaseModel):
    """エラー情報"""

    code: int
    message: str


class VisionResponse(BaseModel):
    """Vision APIレスポンス"""

    webDetection: WebDetection | None = None
    error: ErrorInfo | None = None


class VisionBatchResponse(BaseModel):
    """Vision APIバッチレスポンス"""

    responses: list[VisionResponse]
