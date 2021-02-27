from fastapi import FastAPI

from vlo import router as vlo
from hwinfo import router as hwinfo
from articles import router as articles

app = FastAPI()
app.include_router(vlo)
app.include_router(articles)
app.include_router(hwinfo)