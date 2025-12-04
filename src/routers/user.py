from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db

from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/", response_model=List[schemas.User])   # Path operation
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Usuario).all()
    return users

@router.get("/{id}", response_model=schemas.User)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Usuario con ID {id} no existe.")
    
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.Usuario(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}", response_model=schemas.User)
def delete_user(id:int, db: Session = Depends(get_db)):
    user_query = db.query(models.Usuario).filter(models.Usuario.id == id)
    user_to_delete = user_query.first()
    
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Usuario con ID {id} no existe.")
        
    user_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.User)
def update_user(id:int, user:schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.Usuario).filter(models.Usuario.id == id)
    user_to_update = user_query.first()
    
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Usuario con ID {id} no existe.")
        
    user_query.update(**user.model_dump(), synchronize_session=False)
    print(user_to_update)
    db.commit()
    
    return user_query.first()