import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use DB_URL from environment variable, fallback to a local SQLite DB for development/testing
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "sqlite:///./test.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args are specific to SQLite for enabling foreign keys and thread safety
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_db_and_tables():
    # This is where you would import your models
    # For now, we know User model is in backend.users.models
    # In a larger app, you might import all models here or have Base know about them
    # through their definition.
    # from backend.users.models import User # Example if Base was defined elsewhere
    Base.metadata.create_all(bind=engine)
