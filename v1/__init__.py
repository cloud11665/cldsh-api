from fastapi import APIRouter

from .vlo import router as vlo

router = APIRouter(prefix="/v1")

router.include_router(vlo)
