from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schema for data to be encoded in JWT
class TokenData(BaseModel):
    email: Optional[str] = None

# Base schema for User properties
class UserBase(BaseModel):
    email: EmailStr

# Schema for user creation (inherits UserBase, adds password)
class UserCreate(UserBase):
    password: str

# Schema for user login
class UserLogin(BaseModel): # Explicitly defining fields for clarity
    email: EmailStr
    password: str

# Schema for representing a user retrieved from DB (inherits UserBase, adds id)
# This schema should NOT include the password.
class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True

# Schema for public user representation (if different from UserInDB)
class User(UserBase): # Example, might be same as UserInDB for this scope
    id: int

    class Config:
        from_attributes = True
