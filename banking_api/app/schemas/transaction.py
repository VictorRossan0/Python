from pydantic import BaseModel

class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    description: str

    class Config:
        schema_extra = {
            "example": {
                "account_id": 1,
                "amount": 50.0,
                "description": "Grocery shopping"
            }
        }