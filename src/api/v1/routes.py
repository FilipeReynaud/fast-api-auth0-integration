from fastapi import APIRouter

from src.api.v1.controllers import auth, base

api_router = APIRouter()
api_router.include_router(base.router, prefix="/healthcheck", tags=["healthcheck"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authorization"])
