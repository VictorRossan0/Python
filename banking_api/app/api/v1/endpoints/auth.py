from fastapi import APIRouter, Depends, HTTPException
from app.core.security import create_access_token, verify_password
from app.schemas.auth import Token, LoginRequest
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.account import Account

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    query = await db.execute("SELECT * FROM accounts WHERE name = :name", {"name": request.username})
    user = query.fetchone()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
