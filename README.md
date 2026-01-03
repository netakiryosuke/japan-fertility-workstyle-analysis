# Japan Fertility Workstyle Analysis

都道府県レベルのパネルデータを用いて、日本における働き方改革が出生率に与える影響を評価する分析ツールです。

## 📋 プロジェクト概要

本プロジェクトは、日本の働き方改革と出生率の関係性を統計的に分析するためのWebアプリケーションです。ユーザーは都道府県別・年次別のパネルデータをCSVファイルとしてアップロードし、固定効果モデル（Fixed Effects Model）を用いた回帰分析を実行できます。

### 主な機能
- CSVファイルのアップロードと検証
- 従属変数・独立変数の動的選択
- 固定効果モデルによるパネルデータ分析
- 分析結果の可視化（係数、標準誤差、t統計量、p値、R²）
- 完全共線性により除外された変数の表示

## 🏗️ システムアーキテクチャ

本システムは以下の3層構造で構成されています：

```
┌─────────────────────────────────────────┐
│         Frontend (React/TypeScript)      │
│  - ユーザーインターフェース              │
│  - データアップロード                    │
│  - 分析結果の表示                        │
└─────────────────┬───────────────────────┘
                  │ HTTP API
┌─────────────────▼───────────────────────┐
│         Backend (FastAPI/Python)         │
│  - データ検証とCSV読み込み               │
│  - 固定効果モデル分析                    │
│  - 結果の返却                            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Analysis Engine (linearmodels)      │
│  - PanelOLS（固定効果モデル）            │
│  - 統計計算                              │
└─────────────────────────────────────────┘
```

### バックエンド (backend/)
- **言語**: Python 3.12
- **フレームワーク**: FastAPI
- **主要ライブラリ**: 
  - linearmodels: パネルデータ分析
  - pandas: データ処理
  - pydantic: データ検証
- **アーキテクチャ**: Domain-Driven Design (DDD)
  - `domain/`: ビジネスロジックとモデル
  - `application/`: アプリケーションサービス
  - `infrastructure/`: データローダー
  - `api/`: REST APIエンドポイント

### フロントエンド (frontend/)
- **言語**: TypeScript
- **フレームワーク**: React 19
- **ビルドツール**: Vite
- **スタイリング**: Tailwind CSS 4
- **主な機能**:
  - CSV ファイルアップロード
  - 変数選択フォーム
  - 分析結果の表示

## 📊 固定効果モデルについて

### 固定効果モデルとは
固定効果モデル（Fixed Effects Model）は、パネルデータ分析において個体固有の特性（観測できない異質性）をコントロールするための統計手法です。本プロジェクトでは、各都道府県固有の特性（文化、地理的要因など）を固定効果として考慮します。

### モデルの数式
```
Y_it = β₀ + β₁X₁_it + β₂X₂_it + ... + αi + εit
```
- `Y_it`: 都道府県iの時点tにおける従属変数（例：出生率）
- `X_it`: 都道府県iの時点tにおける独立変数（例：労働時間、育児休業取得率）
- `αi`: 都道府県iの固定効果（時間を通じて不変の特性）
- `εit`: 誤差項

### 使用理由
1. **観測できない異質性の制御**: 都道府県ごとの文化や伝統など、測定が困難だが重要な要因を制御
2. **因果推論への接近**: 個体固有の時不変な要因を除去することで、より因果関係に近い推定が可能
3. **バイアスの軽減**: 欠落変数バイアスを軽減

### 分析結果の解釈における注意点

#### 1. 係数の解釈
- 係数は「個体内での変化」を表す
- 例：労働時間の係数が-0.05の場合、「同じ都道府県内で労働時間が1時間増加すると、出生率が0.05ポイント減少する」と解釈

#### 2. R²の種類
- **R² Within**: 個体内の変動の説明力（主要な指標）
- **R² Between**: 個体間の変動の説明力
- **R² Overall**: 全体的な説明力

固定効果モデルでは **R² Within** を重視してください。

#### 3. 完全共線性（Multicollinearity）
固定効果の導入により、一部の変数が完全共線性を持つ場合、自動的に除外されます。除外された変数は分析結果の `droppedVars` に表示されます。

#### 4. 因果関係の推論における限界
- 固定効果モデルは因果推論に有用ですが、完全な因果関係を証明するものではありません
- 時間変動する交絡因子は制御されません
- 逆因果（reverse causality）の可能性を常に考慮してください

#### 5. データの要件
- **パネルデータ**: 複数の個体を複数の時点で観測したデータが必要
- **バランスパネル推奨**: すべての個体がすべての時点で観測されていることが望ましい
- **十分なサンプルサイズ**: 個体数と時点数が十分に大きい必要があります

## 🚀 起動方法

### 前提条件
- Docker と Docker Compose がインストールされていること

### 手順

1. **リポジトリのクローン**
```bash
git clone https://github.com/netakiryosuke/japan-fertility-workstyle-analysis.git
cd japan-fertility-workstyle-analysis
```

2. **フロントエンドのビルド**
```bash
cd frontend
npm install
npm run build
cd ..
```

3. **Docker Composeで起動**
```bash
docker-compose up --build
```

4. **アクセス**
- フロントエンド: http://localhost
- バックエンドAPI: http://localhost:8000
- APIドキュメント: http://localhost:8000/docs

### ローカル開発環境（Docker不使用）

#### バックエンド
```bash
cd backend
# Python 3.12以上が必要
pip install uv
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

#### フロントエンド
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173 で起動
```

## 📁 ディレクトリ構造

```
japan-fertility-workstyle-analysis/
├── backend/              # バックエンドアプリケーション
│   ├── app/
│   │   ├── api/          # REST APIエンドポイント
│   │   ├── application/  # アプリケーションサービス
│   │   ├── domain/       # ドメインモデルとサービス
│   │   ├── infrastructure/ # データローダー
│   │   ├── config/       # 設定
│   │   └── main.py       # アプリケーションエントリーポイント
│   ├── tests/            # テスト
│   ├── pyproject.toml    # Python依存関係
│   └── Dockerfile
├── frontend/             # フロントエンドアプリケーション
│   ├── src/
│   │   ├── components/   # Reactコンポーネント
│   │   ├── pages/        # ページコンポーネント
│   │   ├── hooks/        # カスタムフック
│   │   ├── api/          # APIクライアント
│   │   └── types/        # TypeScript型定義
│   ├── package.json      # npm依存関係
│   └── vite.config.ts    # Vite設定
├── docker-compose.yml    # Docker Compose設定
└── README.md             # このファイル
```

## 🧪 テスト

### バックエンド
```bash
cd backend
uv run pytest
```

### フロントエンド
```bash
cd frontend
npm run lint
npm run typecheck
```

## 🛠️ 技術スタック

### バックエンド
| カテゴリ | 技術 |
|---------|------|
| 言語 | Python 3.12 |
| Webフレームワーク | FastAPI |
| 統計分析 | linearmodels, pandas, numpy |
| データ検証 | Pydantic |
| パッケージ管理 | uv |
| テスト | pytest |

### フロントエンド
| カテゴリ | 技術 |
|---------|------|
| 言語 | TypeScript |
| フレームワーク | React 19 |
| ビルドツール | Vite |
| スタイリング | Tailwind CSS 4 |
| リンター | ESLint |

### インフラ
| カテゴリ | 技術 |
|---------|------|
| コンテナ | Docker |
| オーケストレーション | Docker Compose |
| Webサーバー | Nginx (Frontend) |

## 📖 ドキュメント

- [バックエンド詳細](./backend/README.md)
- [フロントエンド詳細](./frontend/README.md)

## 📝 ライセンス

このプロジェクトのライセンスについては、リポジトリの管理者にお問い合わせください。

## 🤝 貢献

バグ報告や機能提案は、GitHubのIssuesからお願いします。
