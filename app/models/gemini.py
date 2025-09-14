from pydantic import BaseModel, Field


class GeminiAnalyzeResponse(BaseModel):
    """Gemini 2.5 Pro分析結果レスポンス"""

    result: str = Field(..., description="AI分析結果テキスト")
    status: str = Field(default="success", description="処理ステータス")


class GeminiHealthResponse(BaseModel):
    """Gemini APIヘルスチェックレスポンス"""

    status: str = Field(..., description="ヘルスチェック結果")
    service: str = Field(..., description="サービス名")


class ErrorResponse(BaseModel):
    """エラーレスポンス"""

    detail: str = Field(..., description="エラー詳細")
    status: str = Field(default="error", description="ステータス")
