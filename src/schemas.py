from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

################# USUARIOS #################
# Data recivida del usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# Data enviada al usuario
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
# Data recivida del usuario
class PostBase(BaseModel):
    title: str      
    content: str    
    published: bool = True

class PostCreate(PostBase):
    pass

# Data enviada al usuario
class Post(PostBase):
    id: int
    created_at: datetime
    owner: User

    class Config:
        from_attributes = True

# Data enviada al usuario with votes
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

################# LOGIN #################
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# Data recivida del usuario y enviada al usuario
class Token(BaseModel):
    access_token : str
    token_type: str
    
# Usada para verificar el TOKEN en oauth2.py
class TokenData(BaseModel):
    id: Optional[int] = None
    
################# VOTES #################
# Data recivida del usuario
class Vote(BaseModel):
    post_id: int
    vote_dir: Optional[bool]