# Japan Fertility Workstyle Analysis

都道府県レベルのパネルデータを用いて、日本における働き方改革が出生率に与える影響を評価する分析ツールです。


## プロジェクト概要

本プロジェクトは、日本の働き方改革と出生率の関係性を統計的に分析するためのWebアプリケーションです。ユーザーは都道府県別・年次別のパネルデータをCSVファイルとしてアップロードし、固定効果モデル（Fixed Effects Model）を用いた回帰分析を実行できます。


## 要件
- Python 3.12
- Node.js 25
- Docker


## 起動方法

1. **リポジトリのクローン**
```bash
git clone https://github.com/netakiryosuke/japan-fertility-workstyle-analysis.git
cd japan-fertility-workstyle-analysis
```

2. **フロントエンドのビルド**
```bash
(cd frontend/ && \
npm install && \
npm run build)
```

3. **Docker Composeで起動**
```bash
docker compose up --build
```

4. **アクセス**
- フロントエンド: http://localhost
- バックエンドAPI: http://localhost:8000
- APIドキュメント: http://localhost:8000/docs


## 固定効果モデルについて

### 固定効果モデルとは
固定効果モデル（Fixed Effects Model）は、パネルデータ分析において個体固有の特性（観測できない異質性）をコントロールするための統計手法です。本プロジェクトでは、各都道府県固有の特性（文化、地理的要因など）を固定効果として考慮します。

### モデルの数式
```
Y_it = β₀ + β₁X₁_it + β₂X₂_it + ... + αi + εit
```
- `Y_it`: 都道府県iの時点tにおける従属変数（例：出生率）
- `X_it`: 都道府県iの時点tにおける独立変数（例：総労働時間、生涯未婚率）
- `αi`: 都道府県iの固定効果
- `εit`: 誤差項

### 使用理由
1. **観測できない異質性の制御**: 都道府県ごとの文化や伝統など、測定が困難だが重要な要因を制御
2. **因果推論への接近**: 個体固有の時不変な要因を除去することで、より因果関係に近い推定が可能
3. **バイアスの軽減**: 欠落変数バイアスを軽減


## ドキュメント

- [バックエンド詳細](./backend/README.md)
- [フロントエンド詳細](./frontend/README.md)
