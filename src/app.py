from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.routes import api_router
from src.core.settings import settings

"""
    Instance shared accross entire project.
"""
app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json")

origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(api_router, prefix=settings.API_V1_STR)
