from fastapi import FastAPI

from v1 import router as v1

app = FastAPI()
app.include_router(v1)