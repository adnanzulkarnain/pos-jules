from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # For server-side default timestamp
from backend.config.database import Base
# Import User and Product models if direct FK constraints are made,
# or at least for relationship reference if needed.
# from backend.users.models import User
# from backend.products.models import Product

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    # Assuming kasir_id refers to a User. A direct FK can be added:
    # kasir_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    kasir_id = Column(Integer, nullable=False) # Simplified for now
    waktu = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Float, nullable=False) # Match Product.harga type (Float for now)

    items = relationship("TransactionItem", back_populates="transaction")
    # user = relationship("User", back_populates="transactions") # If User model has 'transactions' relationship

class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    # Assuming produk_id refers to a Product. A direct FK can be added:
    # produk_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    produk_id = Column(Integer, nullable=False) # Simplified for now
    qty = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False) # Match Product.harga type

    transaction = relationship("Transaction", back_populates="items")
    # product = relationship("Product") # Define how Product relates back if needed, or simple FK is enough
                                      # For stock updates, we'll fetch Product separately.
