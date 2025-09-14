import logging
import os
from functools import lru_cache

from fastapi import HTTPException, UploadFile
from google import genai
from google.genai import types

from app.models.gemini import GeminiAnalyzeResponse

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_gemini_client() -> genai.Client:
    """
    Vertex AI経由でGemini APIクライアントを取得（キャッシュ付き）

    Returns:
        Gemini APIクライアント

    Raises:
        HTTPException: クライアント初期化エラー
    """
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT環境変数が設定されていません")

        location = os.getenv("VERTEX_AI_LOCATION")
        if not location:
            raise ValueError("VERTEX_AI_LOCATION環境変数が設定されていません")

        client = genai.Client(vertexai=True, project=project_id, location=location)

        logger.info(
            f"Gemini client initialized for project: {project_id}, location: {location}"
        )
        return client

    except Exception as e:
        logger.error(f"Gemini client initialization failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Gemini API初期化エラー: {e!s}"
        ) from e


async def analyze_image(file: UploadFile, prompt: str) -> GeminiAnalyzeResponse:
    """
    画像とプロンプトを使用してGemini 2.5 Proで分析を実行

    Args:
        file: アップロードされた画像ファイル
        prompt: 分析用テキストプロンプト

    Returns:
        分析結果レスポンス

    Raises:
        HTTPException: Gemini API呼び出しエラー
    """
    try:
        client = get_gemini_client()

        # 画像をバイナリで読み込み
        image_bytes = await file.read()

        # ファイルポインタを先頭に戻す（必要に応じて）
        if hasattr(file.file, "seek"):
            file.file.seek(0)

        # 画像をPartに変換
        image_part = types.Part.from_bytes(
            data=image_bytes, mime_type=file.content_type or "image/jpeg"
        )

        # Gemini 2.5 Proを呼び出し
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(
                    role="user", parts=[types.Part.from_text(text=prompt), image_part]
                )
            ],
        )

        # レスポンステキストを取得
        result_text = (
            response.text if response.text else "分析結果を取得できませんでした"
        )

        logger.info(f"Gemini analysis completed successfully for file: {file.filename}")

        return GeminiAnalyzeResponse(result=result_text, status="success")

    except Exception as e:
        logger.error(f"Gemini analysis error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Gemini API分析エラー: {e!s}"
        ) from e


def health_check() -> bool:
    """
    Gemini API接続確認

    Returns:
        接続状態（True: 正常, False: 異常）
    """
    try:
        get_gemini_client()
        return True
    except Exception as e:
        logger.error(f"Gemini health check failed: {e}")
        return False
