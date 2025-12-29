from fastapi import APIRouter
from app.api.routes.analysis import router

api_router = APIRouter()
api_router.include_router(analysis)
