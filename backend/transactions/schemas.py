from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime # For response model

# --- TransactionItem Schemas ---
class TransactionItemBase(BaseModel):
    produk_id: int
    qty: int

    @validator('qty')
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be a positive integer")
        return value

class TransactionItemCreate(TransactionItemBase):
    pass # No additional fields for creation beyond base

class TransactionItemInDB(TransactionItemBase):
    id: int
    transaction_id: int # Or not, if only shown nested under TransactionInDB
    subtotal: float # Assuming float to match model, will be calculated

    class Config:
        from_attributes = True

# --- Transaction Schemas ---
class TransactionBase(BaseModel):
    # kasir_id will be derived from authenticated user in a real app,
    # or passed if kasir assignment is manual by an admin.
    # For this iteration, let's assume it's passed.
    kasir_id: int

class TransactionCreate(TransactionBase):
    items: List[TransactionItemCreate]

    @validator('items')
    def must_have_at_least_one_item(cls, value):
        if not value:
            raise ValueError("Transaction must have at least one item")
        return value

class TransactionInDB(TransactionBase):
    id: int
    waktu: datetime
    total: float # Will be calculated
    items: List[TransactionItemInDB] # Nested list of items

    class Config:
        from_attributes = True
