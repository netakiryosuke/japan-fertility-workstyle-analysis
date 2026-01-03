# Backend - Japan Fertility Workstyle Analysis

FastAPIを使用したバックエンドアプリケーションです。パネルデータ分析（固定効果モデル）の実行と結果の提供を行います。

## 要件
- Python 3.12以上
- uv

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
  -F "csv_file=@sample_panel_data.csv" \
  -F "dependent_var=TFR" \
  -F "independent_vars=unmarried" \
  -F "independent_vars=employment_rate"
```

### レスポンスサンプル
```json
{
  "nobs": 188,
  "params": {
    "unmarried": 0.29768307486717155,
    "employment_rate": 0.7343018266432476
  },
  "std_errors": {
    "unmarried": 0.30456531864726294,
    "employment_rate": 0.6792216004861323
  },
  "tstats": {
    "unmarried": 0.9774030614823148,
    "employment_rate": 1.0810931603436835
  },
  "pvalues": {
    "unmarried": 0.33006766101841034,
    "employment_rate": 0.28152777124812634
  },
  "rsquared_within": 0.1367670242557425,
  "rsquared_between": 0.5950317103982381,
  "rsquared_overall": 0.5939171626936461,
  "dropped_vars": []
}
```
