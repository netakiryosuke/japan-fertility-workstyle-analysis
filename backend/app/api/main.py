from fastapi import APIRouter
from app.api.routes.analysis import router as analysis

api_router = APIRouter()
api_router.include_router(analysis)
