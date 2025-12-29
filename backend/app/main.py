from fastapi import FastAPI

from backend.app.api.global_exception_handler import handle_value_error, handle_unexpected_exception
from backend.app.api.main import api_router

app = FastAPI(
    title="Japan Fertility Workstyle Analysis API",
)

app.include_router(api_router)
app.add_exception_handler(ValueError, handle_value_error)
app.add_exception_handler(Exception, handle_unexpected_exception)

@app.get("/health")
def health_check():
    return {"status": "ok"}
