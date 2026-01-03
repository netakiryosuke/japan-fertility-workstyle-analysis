# Backend - Japan Fertility Workstyle Analysis

FastAPIを使用したバックエンドアプリケーション。パネルデータ分析（固定効果モデル）の実行と結果の提供を行います。

## 📋 概要

このバックエンドは以下の責務を担っています：

- CSVファイルの受信と検証
- パネルデータの前処理
- 固定効果モデル（PanelOLS）による統計分析の実行
- 分析結果（係数、標準誤差、統計量、R²）のJSON形式での返却
- エラーハンドリング（欠損カラム、不正なデータ形式）

## 🛠️ 技術スタック

| カテゴリ | 技術 | バージョン | 用途 |
|---------|------|----------|------|
| 言語 | Python | 3.12+ | メイン言語 |
| Webフレームワーク | FastAPI | 0.128.0+ | REST API |
| 統計分析 | linearmodels | 7.0+ | パネルデータ分析（PanelOLS） |
| データ処理 | pandas | 2.3.3+ | データフレーム操作 |
| 数値計算 | numpy | 2.4.0+ | 数値演算 |
| データ検証 | pydantic | 2.12.5+ | リクエスト/レスポンス検証 |
| サーバー | uvicorn | 0.40.0+ | ASGIサーバー |
| パッケージ管理 | uv | - | 高速パッケージマネージャ |
| テスト | pytest | 8.3.0+ | ユニット・統合テスト |

## 🏗️ アーキテクチャ

Domain-Driven Design (DDD) の原則に基づいた階層型アーキテクチャを採用しています。

```
app/
├── api/                      # プレゼンテーション層
│   ├── routes/
│   │   └── analysis.py       # 分析エンドポイント
│   ├── global_exception_handler.py
│   └── main.py               # ルーター集約
├── application/              # アプリケーション層
│   ├── dependencies.py       # DIコンテナ
│   ├── exception/            # アプリケーション例外
│   └── fertility_analysis_application_service.py  # ユースケース実装
├── domain/                   # ドメイン層
│   ├── model/
│   │   └── fixed_effects_result.py  # 分析結果モデル
│   └── service/
│       └── fixed_effects_analysis_service.py  # ドメインサービス
├── infrastructure/           # インフラストラクチャ層
│   └── csv_dataframe_loader.py  # CSV読み込み
├── config/                   # 設定
│   └── web_config.py         # CORS等の設定
└── main.py                   # アプリケーションエントリーポイント
```

### 各層の責務

#### 1. API層 (`api/`)
- HTTPリクエストの受信
- リクエストボディのバリデーション
- レスポンスの返却
- エラーハンドリング

#### 2. Application層 (`application/`)
- ユースケースの実装
- トランザクション境界の管理
- ドメインサービスの呼び出し
- データの正規化

#### 3. Domain層 (`domain/`)
- ビジネスロジックの実装
- `FixedEffectsAnalysisService`: 固定効果モデルによる分析ロジック
- `FixedEffectsResult`: 分析結果のドメインモデル

#### 4. Infrastructure層 (`infrastructure/`)
- 外部システムとの連携
- CSVファイルの読み込み・パース

## 🚀 セットアップ

### 前提条件
- Python 3.12以上
- uv（推奨）または pip

### インストール

#### uvを使用（推奨）
```bash
# uvのインストール（未インストールの場合）
pip install uv

# プロジェクトのルートディレクトリで
cd backend

# 依存関係のインストール
uv sync

# 開発用依存関係を含める場合
uv sync --all-extras
```

#### pipを使用
```bash
cd backend
pip install -e .
# テスト用
pip install -e ".[test]"
```

## 🏃 実行方法

### 開発サーバーの起動

#### uvを使用
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### pipを使用
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

サーバーが起動したら、以下のURLでアクセスできます：
- API: http://localhost:8000
- 対話的APIドキュメント (Swagger UI): http://localhost:8000/docs
- 代替APIドキュメント (ReDoc): http://localhost:8000/redoc

### Dockerを使用
```bash
# リポジトリルートから
docker-compose up backend
```

## 🧪 テスト

### テストの実行

```bash
# すべてのテスト
uv run pytest

# 詳細な出力
uv run pytest -v

# カバレッジ付き
uv run pytest --cov=app --cov-report=html

# 特定のテストファイル
uv run pytest tests/test_main.py

# 特定のテスト関数
uv run pytest tests/test_main.py::test_health_check
```

### テスト構造
```
tests/
├── api/                      # APIエンドポイントのテスト
├── application/              # アプリケーションサービスのテスト
├── domain/                   # ドメインサービスのテスト
├── infrastructure/           # インフラストラクチャのテスト
└── test_main.py              # メインアプリケーションのテスト
```

## 📡 API仕様

### エンドポイント一覧

#### 1. ヘルスチェック
```
GET /health
```
**レスポンス**:
```json
{
  "status": "ok"
}
```

#### 2. パネルデータ分析
```
POST /analysis
Content-Type: multipart/form-data
```

**リクエストパラメータ**:
- `csv_file` (file): パネルデータのCSVファイル
- `dependent_var` (string): 従属変数のカラム名
- `independent_vars` (array[string]): 独立変数のカラム名の配列

**CSVフォーマット要件**:
```csv
prefecture,year,fertility_rate,working_hours,childcare_leave_rate
Tokyo,2015,1.15,160,0.05
Tokyo,2016,1.17,158,0.06
Osaka,2015,1.25,162,0.04
Osaka,2016,1.27,160,0.05
...
```

必須カラム:
- `prefecture`: 都道府県名（エンティティ変数）
- `year`: 年（時間変数）
- 従属変数と独立変数として指定したカラム

**レスポンス例**:
```json
{
  "nobs": 470,
  "params": {
    "working_hours": -0.0123,
    "childcare_leave_rate": 0.0456
  },
  "std_errors": {
    "working_hours": 0.0034,
    "childcare_leave_rate": 0.0189
  },
  "tstats": {
    "working_hours": -3.617,
    "childcare_leave_rate": 2.413
  },
  "pvalues": {
    "working_hours": 0.0003,
    "childcare_leave_rate": 0.0159
  },
  "rsquared_within": 0.456,
  "rsquared_between": 0.234,
  "rsquared_overall": 0.312,
  "dropped_vars": []
}
```

**エラーレスポンス例**:
```json
{
  "detail": "Missing columns: fertility_rate, working_hours"
}
```

### CORS設定

環境変数 `BACKEND_CORS_ORIGINS` で許可するオリジンを設定できます。

```bash
# 例
export BACKEND_CORS_ORIGINS="http://localhost,http://localhost:5173"
```

## 🔧 設定

### 環境変数

| 変数名 | デフォルト値 | 説明 |
|-------|------------|------|
| `BACKEND_CORS_ORIGINS` | `"http://localhost"` | CORS許可オリジン（カンマ区切り） |

### 設定ファイル

`app/config/web_config.py` で設定を管理しています。

## 🐛 デバッグ

### ログレベルの変更
```bash
uv run uvicorn app.main:app --log-level debug
```

### インタラクティブデバッグ
```python
# コード内に挿入
import pdb; pdb.set_trace()
```

## 📊 統計分析の詳細

### 使用モデル: PanelOLS（固定効果モデル）

`linearmodels.panel.PanelOLS` を使用しています。

```python
from linearmodels.panel import PanelOLS

# モデルの構築
model = PanelOLS(y, X, entity_effects=True, drop_absorbed=True)
result = model.fit()
```

**パラメータ**:
- `entity_effects=True`: エンティティ固定効果を含める
- `drop_absorbed=True`: 完全共線性のある変数を自動除外

### 結果の解釈

- **params**: 推定係数（独立変数の従属変数への影響）
- **std_errors**: 標準誤差（推定の不確実性）
- **tstats**: t統計量（係数の有意性の検定統計量）
- **pvalues**: p値（帰無仮説を棄却できる確率、0.05未満で有意）
- **rsquared_within**: 個体内変動の説明力（固定効果モデルで重視）
- **rsquared_between**: 個体間変動の説明力
- **rsquared_overall**: 全体的な説明力
- **dropped_vars**: 完全共線性により除外された変数

## 🚨 エラーハンドリング

### カスタム例外

#### MissingColumnsException
CSVファイルに必要なカラムが存在しない場合に発生します。

```python
raise MissingColumnsException(missing_columns=["fertility_rate"])
```

### グローバル例外ハンドラ
- `ValueError`: 400 Bad Request
- `MissingColumnsException`: 400 Bad Request
- `Exception`: 500 Internal Server Error

## 🔒 セキュリティ

- ファイルサイズ制限: FastAPIのデフォルト設定に従う
- CSVファイルのバリデーション: pandasによるパース時に検証
- CORS: 必要なオリジンのみ許可

## 🎯 今後の拡張案

- [ ] 認証・認可の追加
- [ ] データベースへの分析履歴の保存
- [ ] 複数のモデル（ランダム効果モデル等）のサポート
- [ ] 非同期処理による大規模データ対応
- [ ] キャッシュ機構の導入

## 📚 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [linearmodels公式ドキュメント](https://bashtage.github.io/linearmodels/)
- [pandas公式ドキュメント](https://pandas.pydata.org/)
