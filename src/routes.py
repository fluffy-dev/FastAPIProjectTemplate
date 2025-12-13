"""
This module defines the main project endpoints
"""

from fastapi import APIRouter
from src.auth.router import router as auth_router

router = APIRouter(prefix="/v1", tags=["v1"])

# register here apps routers

router.include_router(auth_router)
