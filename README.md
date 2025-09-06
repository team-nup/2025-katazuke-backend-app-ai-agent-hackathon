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

## 📁 プロジェクト構造

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIメインアプリケーション
│   └── routers/
│       ├── __init__.py
│       └── health.py        # ヘルスチェックエンドポイント
├── requirements.txt         # Python依存関係
├── Dockerfile              # コンテナイメージ定義
├── .dockerignore           # Docker無視ファイル
├── .gitignore              # Git無視ファイル
├── .env.template           # 環境変数テンプレート
├── .env.sample             # 環境変数サンプル
├── deploy.sh               # Cloud Runデプロイスクリプト
├── local-test.sh           # ローカルテストスクリプト
├── README.md               # このファイル
└── CLAUDE.md               # Claude Code用設定ファイル
```

## 🔧 ローカル開発

### 前提条件

- Docker
- Python 3.11+（ローカル開発の場合）
- Google Cloud SDK（デプロイの場合）

### ローカルでの実行

#### 方法1: Docker使用（推奨）

```bash
# ビルド、実行、テストを一括で実行
./local-test.sh

# 個別コマンド
./local-test.sh build   # Dockerイメージをビルド
./local-test.sh run     # コンテナを実行
./local-test.sh test    # APIエンドポイントをテスト
./local-test.sh stop    # コンテナを停止
./local-test.sh clean   # クリーンアップ
./local-test.sh logs    # ログを表示
```

#### 方法2: Python直接実行

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

### APIエンドポイント

アプリケーションが起動したら、以下のエンドポイントにアクセスできます：

- **ルート**: http://localhost:8080/
- **API情報**: http://localhost:8080/api/v1/info
- **ヘルスチェック**: http://localhost:8080/api/v1/health/
- **Liveness Probe**: http://localhost:8080/api/v1/health/liveness
- **Readiness Probe**: http://localhost:8080/api/v1/health/readiness
- **詳細ヘルス**: http://localhost:8080/api/v1/health/detailed
- **API Documentation**: http://localhost:8080/docs
- **ReDoc Documentation**: http://localhost:8080/redoc

## ☁️ Cloud Runへのデプロイ

### 前提条件

1. Google Cloud SDKをインストール
2. Google Cloudプロジェクトを作成
3. 必要な権限を持つアカウントでログイン

### 設定ファイルの準備

環境設定を管理するために`.env`ファイルを使用できます：

```bash
# .env.templateをコピーして設定
cp .env.template .env

# .envファイルを編集してあなたの設定を入力
# 最低限PROJECT_IDは設定してください
```

`.env`ファイルの例：
```bash
PROJECT_ID=my-edd-hackathon-project-123
REGION=us-central1
SERVICE_NAME=edd-backend-resource
MEMORY=2Gi
CPU=2
MAX_INSTANCES=20
```

### デプロイ手順

```bash
# 方法1: .envファイルを使用（推奨）
cp .env.template .env
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

Cloud Runでは以下の環境変数が設定されます：

- `PORT`: Cloud Runが自動設定（通常8080）
- `PYTHON_VERSION`: Python バージョン情報

## 🧪 テスト

```bash
# ローカルテストスクリプトでAPIをテスト
./local-test.sh test

# または手動でcurlを使用
curl http://localhost:8080/api/v1/health/
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

## 🔒 セキュリティ

- 非rootユーザーでコンテナを実行
- マルチステージDockerビルド
- 最小限のベースイメージ使用
- 機密情報の環境変数管理

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトは2025年EDDハッカソン用です。

## 📞 サポート

問題や質問がある場合は、GitHubのIssuesを使用してください。