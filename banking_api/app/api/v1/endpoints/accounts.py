from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.account import Account
from app.db.session import get_db

router = APIRouter()

@router.post("/create/")
async def create_account(name: str, db: AsyncSession = Depends(get_db)):
    new_account = Account(name=name)
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account

@router.get("/{account_id}")
async def get_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
