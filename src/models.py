from .database import Base          # SQLAlchemy Models
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"     # Nombre que queremos dar a la tabla en postgres.
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False) # Hace referencia ala tabla "Usuarios"
    owner = relationship("User") # Retorna la clase de otro modelo (Usuario). Trae los atributos de Usuario con base en owner_id.
    
    
class Voto(Base):
    __tablename__ = "votos"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True,nullable=False) # Composite key
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True,nullable=False) # Composite key