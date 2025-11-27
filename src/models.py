from .database import Base          # SQLAlchemy Models
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"     # Name we want to give the table in postgres.
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
class Post(Base):
    __tablename__ = "posts"     # Name we want to give the table in postgres.
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # Refers to the table name "users"
    owner = relationship("User") # Return the class from another model (User). Fetch the User attributes based on the owner_id and return it. 
    
    
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True,nullable=False) # Composite key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True,nullable=False) # Composite key