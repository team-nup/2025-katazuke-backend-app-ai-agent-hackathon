# EDD Cloud Run Backend Resource

Employment Development Department backend resource for hackathon 2025 - A FastAPI-based microservice designed to run on Google Cloud Run.

## 📋 概要

このプロジェクトは、2025年EDDハッカソン用のGoogle Cloud Runバックエンドリソースです。FastAPIを使用して構築された、高性能でスケーラブルなマイクロサービスです。

## 🚀 機能

- **FastAPI**: 高性能な非同期APIフレームワーク
- **自動APIドキュメント**: Swagger UI (`/docs`) と ReDoc (`/redoc`)
- **ヘルスチェック**: Kubernetesスタイルの liveness/readiness プローブ
- **Cloud Run最適化**: コンテナ化とCloud Runでの実行に最適化
- **セキュリティ**: 非rootユーザーでの実行とマルチステージDockerビルド
- **Vision API**: Google Cloud Vision APIによる画像解析（Web Detection）
- **Gemini API**: Gemini 2.5 Proによるマルチモーダル画像分析

## 📁 プロジェクト構造

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIメインアプリケーション
│   ├── api/
│   │   └── routers/
│   │       ├── health.py    # ヘルスチェックエンドポイント
│   │       ├── vision.py    # Vision APIエンドポイント
│   │       └── gemini.py    # Gemini APIエンドポイント
│   ├── services/
│   │   ├── vision_service.py # Vision APIビジネスロジック
│   │   └── gemini_service.py # Gemini APIビジネスロジック
│   └── models/
│       ├── vision.py        # Vision APIデータモデル
│       └── gemini.py        # Gemini APIデータモデル
├── requirements.txt         # Python依存関係
├── Dockerfile              # コンテナイメージ定義
├── .dockerignore           # Docker無視ファイル
├── .gitignore              # Git無視ファイル
├── .env.example            # 環境変数テンプレート
├── deploy.sh               # Cloud Runデプロイスクリプト
└── README.md               # このファイル
```

## 🔧 ローカル開発

### 前提条件

- Docker
- Python 3.12+（ローカル開発の場合）
- Google Cloud SDK（デプロイの場合）

### ローカルでの実行

```bash
# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\\Scripts\\activate   # Windows

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを実行
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### APIドキュメント

- **API Documentation**: http://localhost:8080/docs

## ☁️ Cloud Runへのデプロイ

### 前提条件

1. Google Cloud SDKをインストール
2. Google Cloudプロジェクトを作成
3. 必要な権限を持つアカウントでログイン

### 設定ファイルの準備

環境設定を管理するために`.env`ファイルを使用できます：

```bash
# .env.exampleをコピーして設定
cp .env.example .env

# .envファイルを編集してあなたの設定を入力
# 最低限PROJECT_IDは設定してください
```

`.env`ファイルの例：
```bash
PROJECT_ID=your-actual-project-id
REGION=us-central1
SERVICE_NAME=your-service-name
MEMORY=2Gi
CPU=2
MAX_INSTANCES=20
```

### デプロイ手順

```bash
# 方法1: .envファイルを使用（推奨）
cp .env.example .env
# .envを編集後
./deploy.sh

# 方法2: コマンドライン引数を使用
./deploy.sh YOUR_PROJECT_ID us-central1 your-service-name

# 方法3: .envとコマンドライン引数の組み合わせ（コマンドライン引数が優先）
./deploy.sh MY_PROJECT_ID  # REGIONとSERVICE_NAMEは.envから読み込み
```

デプロイスクリプトは以下を自動実行します：

1. 必要なGCP APIの有効化
2. Artifact Registryリポジトリの作成
3. Cloud Buildを使用したDockerイメージのビルドとプッシュ
4. Cloud Runサービスのデプロイ
5. デプロイメントのテスト

### 環境変数

必要な環境変数：

- `GOOGLE_CLOUD_PROJECT`: Google CloudプロジェクトID
- `VERTEX_AI_LOCATION`: Vertex AIのリージョン

## 🧪 テスト

```bash
# ヘルスチェック
curl https://YOUR-SERVICE-URL/api/v1/health/

# APIドキュメント
https://YOUR-SERVICE-URL/docs
```

## 📚 開発ガイド

### 新しいエンドポイントの追加

1. `app/routers/` に新しいルーターファイルを作成
2. `app/main.py` でルーターをインクルード
3. ローカルでテスト
4. デプロイ

### 依存関係の追加

1. `requirements.txt` に新しい依存関係を追加
2. Dockerイメージを再ビルド
3. テストとデプロイ

