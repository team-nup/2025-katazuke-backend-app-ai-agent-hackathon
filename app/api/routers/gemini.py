from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.gemini import GeminiAnalyzeResponse, GeminiHealthResponse
from app.services import gemini_service

router = APIRouter(prefix="/api/v1/gemini", tags=["gemini"])

# 定数定義
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_PROMPT_LENGTH = 2000


@router.post("/analyze", response_model=GeminiAnalyzeResponse)
async def analyze_image(
    file: UploadFile = File(..., description="分析対象の画像ファイル"),
    prompt: str = Form(..., description="画像分析用のテキストプロンプト"),
) -> GeminiAnalyzeResponse:
    """
    Gemini 2.5 Proを使用して画像とプロンプトから分析結果を生成

    - **file**: 分析対象の画像ファイル（JPEG, PNG等）
    - **prompt**: 画像に対する分析指示（例：「この画像について説明してください」）

    Returns:
        - **result**: AI分析結果テキスト
        - **status**: 処理ステータス
    """

    # ファイル形式チェック
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="画像ファイルのみサポートしています"
        )

    # ファイルサイズチェック
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="ファイルサイズは10MB以下にしてください"
        )

    # プロンプトの長さチェック
    if len(prompt.strip()) == 0:
        raise HTTPException(status_code=400, detail="プロンプトが空です")

    if len(prompt) > MAX_PROMPT_LENGTH:
        raise HTTPException(
            status_code=400, detail="プロンプトは2000文字以下にしてください"
        )

    return await gemini_service.analyze_image(file, prompt)


@router.get("/health", response_model=GeminiHealthResponse)
async def gemini_health() -> GeminiHealthResponse:
    """Gemini APIの接続確認"""
    is_healthy = gemini_service.health_check()

    if not is_healthy:
        raise HTTPException(status_code=503, detail="Gemini API接続エラー")

    return GeminiHealthResponse(
        status="healthy", service="Google Gemini 2.5 Pro via Vertex AI"
    )
