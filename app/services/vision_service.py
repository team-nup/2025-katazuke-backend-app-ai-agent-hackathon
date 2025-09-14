import base64

from fastapi import HTTPException
from google.cloud import vision

from app.models.vision import (
    BestGuessLabel,
    ErrorInfo,
    VisionBatchRequest,
    VisionBatchResponse,
    VisionResponse,
    WebDetection,
    WebEntity,
    WebImage,
    WebPage,
)


class VisionService:
    """Vision API呼び出しサービス"""

    def __init__(self):
        """Vision APIクライアントを初期化"""
        self.client = vision.ImageAnnotatorClient()

    async def web_detection(self, request: VisionBatchRequest) -> VisionBatchResponse:
        """
        Web Detection機能を実行

        Args:
            request: バッチリクエスト

        Returns:
            バッチレスポンス

        Raises:
            HTTPException: Vision API呼び出しエラー
        """
        try:
            # リクエストの変換
            vision_requests = self._convert_to_vision_requests(request)

            # Vision API呼び出し
            response = self.client.batch_annotate_images(requests=vision_requests)

            # レスポンスの変換
            return self._convert_to_response(response)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Vision API呼び出しエラー: {e!s}"
            ) from e

    def _convert_to_vision_requests(
        self, request: VisionBatchRequest
    ) -> list[vision.AnnotateImageRequest]:
        """リクエストをVision API形式に変換"""
        vision_requests = []

        for req in request.requests:
            # 画像の設定（Base64のみサポート）
            image = vision.Image()
            try:
                image.content = base64.b64decode(req.image.content)
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Base64デコードエラー: {e!s}"
                ) from e

            # 機能の設定
            features = []
            for feature in req.features:
                vision_feature = vision.Feature()
                try:
                    vision_feature.type_ = getattr(vision.Feature.Type, feature.type)
                except AttributeError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"サポートされていない機能タイプ: {feature.type}",
                    ) from None

                if feature.maxResults:
                    vision_feature.max_results = feature.maxResults
                features.append(vision_feature)

            # リクエスト作成
            vision_request = vision.AnnotateImageRequest(image=image, features=features)
            vision_requests.append(vision_request)

        return vision_requests

    def _convert_to_response(self, response) -> VisionBatchResponse:
        """Vision APIレスポンスをアプリケーション形式に変換"""
        responses = []

        for image_response in response.responses:
            vision_response = VisionResponse()

            # エラーチェック
            if image_response.error.message:
                vision_response.error = ErrorInfo(
                    code=image_response.error.code, message=image_response.error.message
                )
            # Web Detection結果の変換
            elif image_response.web_detection:
                vision_response.webDetection = self._convert_web_detection(
                    image_response.web_detection
                )

            responses.append(vision_response)

        return VisionBatchResponse(responses=responses)

    def _convert_web_detection(self, web_detection) -> WebDetection:
        """Web Detection結果を変換"""
        return WebDetection(
            webEntities=[
                WebEntity(
                    entityId=entity.entity_id,
                    score=entity.score,
                    description=entity.description,
                )
                for entity in web_detection.web_entities
            ],
            fullMatchingImages=[
                WebImage(url=img.url) for img in web_detection.full_matching_images
            ],
            partialMatchingImages=[
                WebImage(url=img.url) for img in web_detection.partial_matching_images
            ],
            pagesWithMatchingImages=[
                WebPage(
                    url=page.url,
                    pageTitle=page.page_title,
                    fullMatchingImages=[
                        WebImage(url=img.url) for img in page.full_matching_images
                    ],
                    partialMatchingImages=[
                        WebImage(url=img.url) for img in page.partial_matching_images
                    ],
                )
                for page in web_detection.pages_with_matching_images
            ],
            visuallySimilarImages=[
                WebImage(url=img.url) for img in web_detection.visually_similar_images
            ],
            bestGuessLabels=[
                BestGuessLabel(label=label.label, languageCode=label.language_code)
                for label in web_detection.best_guess_labels
            ],
        )

    def health_check(self) -> bool:
        """Vision API接続確認"""
        try:
            # Vision APIクライアントの初期化テスト
            vision.ImageAnnotatorClient()
            return True
        except Exception:
            return False
