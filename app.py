from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vlo import router as vlo
from hwinfo import router as hwinfo
from articles import router as articles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vlo)
app.include_router(articles)
app.include_router(hwinfo)