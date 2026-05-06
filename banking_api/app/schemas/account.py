from pydantic import BaseModel

class AccountCreate(BaseModel):
    name: str
    balance: float

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "balance": 100.0
            }
        }
