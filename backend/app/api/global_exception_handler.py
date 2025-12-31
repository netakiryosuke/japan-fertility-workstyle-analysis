from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.application.exception.missing_columns_exception import MissingColumnsException

def handle_value_error(request: Request, e: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "type": "about:blank",
            "title": "Invalid request",
            "status": status.HTTP_400_BAD_REQUEST,
            "detail": str(e),
            "instance": str(request.url.path),
        },
    )
    
def handle_missing_columns_exception(request: Request, e: MissingColumnsException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "type": "about:blank",
            "title": "Unprocessable entity",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": str(e),
            "instance": str(request.url.path),
        },
    )

def handle_unexpected_exception(request: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "type": "about:blank",
            "title": "Internal server error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "Unexpected error",
            "instance": str(request.url.path),
        },
    )
