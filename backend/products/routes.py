from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional # Optional needed for query params

from backend.products.models import Product as ProductModel
from backend.products.schemas import ProductCreate, ProductUpdate, ProductInDB
from backend.config.database import get_db

router = APIRouter()

@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump()) # Pydantic V2 use model_dump()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductInDB])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductInDB)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductInDB)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Pydantic V2: product.model_dump(exclude_unset=True)
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.add(db_product) # or db.merge(db_product) if you want to handle detached instances
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", response_model=ProductInDB) # Or some success message schema
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(db_product)
    db.commit()
    # After deletion, the object is no longer in the session, so returning it directly
    # might cause issues if it was expired from the session.
    # It's common to return the deleted object (if still accessible) or a success message.
    # For ProductInDB response model, it implies the object is returned.
    return db_product # This works if the object is not expired from session or if ProductInDB can be constructed.
                     # Alternatively, return a message: return {"message": "Product deleted successfully"}
                     # If returning the object, ensure it's handled correctly by the ORM after delete.
