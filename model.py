from pydantic import BaseModel

class Transaction(BaseModel):
    value: float