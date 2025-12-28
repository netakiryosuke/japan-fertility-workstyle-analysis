from fastapi import FastAPI

app = FastAPI(
    title="Japan Fertility Work style Analysis API",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
