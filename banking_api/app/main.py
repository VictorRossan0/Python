from fastapi import FastAPI
from app.api.v1.endpoints import accounts

app = FastAPI(title="Banking API", version="1.0")

app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
