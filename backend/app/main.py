from fastapi import FastAPI

from backend.app.api.main import api_router

app = FastAPI(
    title="Japan Fertility Workstyle Analysis API",
)

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
