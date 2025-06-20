from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship # Optional: if you define a Category model later
from backend.config.database import Base # Assuming Base is in backend.config.database

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True, nullable=False)
    # Using Float for price, consider Integer if dealing with cents/smallest currency unit
    # For simplicity here, Float is used. For financial apps, Decimal or Integer is safer.
    harga = Column(Float, nullable=False)
    stok = Column(Integer, nullable=False, default=0)

    # Optional: Foreign key to a categories table
    # kategori_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    # category = relationship("Category", back_populates="products") # Example relationship

    # For now, kategori_id will be a simple Integer column without a direct FK constraint
    # to avoid needing a Category model immediately. It can be added later.
    kategori_id = Column(Integer, nullable=True)
