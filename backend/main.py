from fastapi import FastAPI
from backend.config.database import create_db_and_tables
from backend.users.routes import router as users_router
from backend.products.routes import router as products_router # New import

# Ensure models are imported so Base registers them before table creation
import backend.users.models
import backend.products.models # New import

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

# Include User routes
app.include_router(users_router, prefix="/users", tags=["users"])

# Include Product routes
app.include_router(products_router, prefix="/products", tags=["products"]) # New router

@app.get("/")
async def root():
    return {"message": "POS backend ready"}
