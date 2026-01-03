# Backend - Japan Fertility Workstyle Analysis

FastAPIを使用したバックエンドアプリケーションです。パネルデータ分析（固定効果モデル）の実行と結果の提供を行います。

## 要件
- Python 3.12以上
- uv（推奨）


## 起動方法
```bash
uv sync --all-extras
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

サーバーが起動したら、以下のURLで確認できます：
- 対話的APIドキュメント (Swagger UI): http://localhost:8000/docs
- 代替APIドキュメント (ReDoc): http://localhost:8000/redoc

## APIリクエストサンプル
```bash
curl -X POST http://localhost:8000/analysis \
  -F "csv_file=@sample.csv" \
  -F "dependent_var=TFR" \
  -F "independent_vars=unmarried" \
  -F "independent_vars=employment_rate"
```
