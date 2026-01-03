from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.web_config import web_config

from app.api.global_exception_handler import handle_missing_columns_exception, handle_value_error, handle_unexpected_exception
from app.api.main import api_router
from app.application.exception.missing_columns_exception import MissingColumnsException

app = FastAPI(
    title="Japan Fertility Workstyle Analysis API",
)

if web_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=web_config.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

app.include_router(api_router)
app.add_exception_handler(ValueError, handle_value_error)
app.add_exception_handler(MissingColumnsException, handle_missing_columns_exception)
app.add_exception_handler(Exception, handle_unexpected_exception)

@app.get("/health")
def health_check():
    return {"status": "ok"}
