from fastapi import FastAPI
from backend.config.database import create_db_and_tables, engine # Added engine for potential direct use if needed
from backend.users.routes import router as users_router
# Ensure User model is loaded before create_db_and_tables is called if using Base.metadata.create_all
# This happens implicitly if users.models imports Base from database.py and defines User model
import backend.users.models

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Create database tables if they don't exist
    # Note: In a production app, you'd typically use Alembic for migrations.
    create_db_and_tables()

app.include_router(users_router, prefix="/users", tags=["users"]) # Added prefix and tags

@app.get("/")
async def root():
    return {"message": "POS backend ready"}
