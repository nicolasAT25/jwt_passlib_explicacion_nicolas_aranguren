from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

################# USERS #################
# Data recieved from the user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# Data sent to the user
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
################# POSTS #################
# Data recieved from the user
class PostBase(BaseModel):
    title: str      
    content: str    
    published: bool = True

class PostCreate(PostBase):
    pass                # Inherits all from PostBase

# Data sent to the user
class Post(PostBase): # Inherit the other fields to return
    id: int
    created_at: datetime
    owner: User

    class Config:
        from_attributes = True #This solves the issue when we send a ORM object as a responde (pydantic BaseModel).

# Data sent to the user with votes
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

################# LOGIN #################
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# Data recieved from the user and sent to the user
class Token(BaseModel):
    access_token : str
    token_type: str
    
# Used to verify the token in oauth2.py
class TokenData(BaseModel):
    id: Optional[int] = None
    
################# VOTES #################
# Data recieved from user
class Vote(BaseModel):
    post_id: int
    vote_dir: Optional[bool]
    # vote_dir: conint(ge=0, le=1)  # vote direction validates 0 or 1.