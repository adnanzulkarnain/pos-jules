from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.transactions.models import Transaction as TransactionModel, TransactionItem as TransactionItemModel
from backend.products.models import Product as ProductModel # For stock updates
from backend.transactions.schemas import TransactionCreate, TransactionInDB, TransactionItemCreate

router = APIRouter()

@router.post("/", response_model=TransactionInDB, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    overall_total = 0
    db_transaction_items = []

    # Start a database transaction block if not already handled by FastAPI/SQLAlchemy per request
    # For complex operations like this, explicit transaction management can be safer,
    # but SQLAlchemy sessions often manage this implicitly for single request scopes.
    # We'll rely on the session's atomicity for now.

    for item_data in transaction_data.items:
        product = db.query(ProductModel).filter(ProductModel.id == item_data.produk_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item_data.produk_id} not found."
            )

        if product.stok < item_data.qty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.nama}. Available: {product.stok}, Requested: {item_data.qty}"
            )

        subtotal = product.harga * item_data.qty
        overall_total += subtotal

        # Decrease stock
        product.stok -= item_data.qty
        db.add(product) # Mark product for update

        # Prepare transaction item for DB, linking to transaction later
        db_item = TransactionItemModel(
            produk_id=item_data.produk_id,
            qty=item_data.qty,
            subtotal=subtotal
            # transaction_id will be set once TransactionModel is created and has an ID,
            # or by SQLAlchemy relationship back-population if items are added to transaction.items
        )
        db_transaction_items.append(db_item)

    if not db_transaction_items: # Should be caught by Pydantic validator, but good to double check
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No items in transaction")

    # Create the main transaction record
    db_transaction = TransactionModel(
        kasir_id=transaction_data.kasir_id,
        total=overall_total
        # waktu is server_default
    )

    # Add items to the transaction's item list for SQLAlchemy to handle relationships
    # This should also set transaction_id on each item when flushed.
    db_transaction.items.extend(db_transaction_items)

    db.add(db_transaction)

    try:
        db.commit()
        db.refresh(db_transaction) # To get generated ID, waktu, and load items correctly
        # If items are not automatically refreshed with transaction_id, a second refresh might be needed
        # or ensure relationships are set up for eager loading if needed immediately.
        # For now, this should be sufficient as TransactionInDB schema expects items.
        # To be absolutely sure items are loaded with all fields for the response:
        for item in db_transaction.items:
            db.refresh(item)

    except Exception as e:
        db.rollback()
        # Log the exception e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not process transaction.")

    return db_transaction


@router.get("/{transaction_id}", response_model=TransactionInDB)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    # Use options for joinedload to fetch items along with the transaction to avoid N+1 queries
    # from sqlalchemy.orm import joinedload
    # db_transaction = db.query(TransactionModel).options(joinedload(TransactionModel.items)).filter(TransactionModel.id == transaction_id).first()

    # Simpler query for now, SQLAlchemy might do implicit loading based on relationship access
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()

    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return db_transaction
