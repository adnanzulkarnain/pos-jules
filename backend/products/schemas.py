from pydantic import BaseModel
from typing import Optional, List

# Base schema for Product properties
class ProductBase(BaseModel):
    nama: str
    harga: float # Matching the Float type in the model for now
    stok: int
    kategori_id: Optional[int] = None

# Schema for product creation (inherits ProductBase)
class ProductCreate(ProductBase):
    pass # No additional fields needed for creation beyond ProductBase

# Schema for product update (all fields optional for partial updates)
class ProductUpdate(BaseModel):
    nama: Optional[str] = None
    harga: Optional[float] = None
    stok: Optional[int] = None
    kategori_id: Optional[int] = None

# Schema for representing a product retrieved from DB (inherits ProductBase, adds id)
class ProductInDB(ProductBase): # Or simply name it 'Product'
    id: int

    class Config:
        from_attributes = True # For Pydantic V2 ( FastAPI typically uses this)

# You might also want a schema for a list of products, though List[ProductInDB] is often used directly.
# class ProductList(BaseModel):
#     products: List[ProductInDB]
#     total: int
