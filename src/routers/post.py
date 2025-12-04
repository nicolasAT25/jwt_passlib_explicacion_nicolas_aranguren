from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import get_db

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",  # Evita indicar la raíz del "path operation"
    tags = ["Posts"]    # Crea una sección en la documentación de Swagger
    )

@router.get("/", response_model=List[schemas.PostOut])   # Path operation
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str]=""):
    posts = db.query(models.Post, func.count(models.Voto.post_id).label("votes")) \
            .join(models.Voto, models.Voto.post_id == models.Post.id, isouter=True) \
            .group_by(models.Post.id) \
            .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Voto.post_id).label("votes")) \
            .join(models.Voto, models.Voto.post_id == models.Post.id, isouter=True) \
            .group_by(models.Post.id) \
            .filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post con ID {id} no existe.")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)   # Esta es toda la query, no el post
    post_to_delete = post_query.first()
    
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post con ID {id} no existe.")
        
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail='No autorizad@ para realizar esta acción.')
        
    post_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post_to_update = post_query.first()
    
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post con ID {id} no existe.")
        
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail='No autorizad@ para realizar esta acción.')
        
    post_query.update(**post.model_dump(), synchronize_session=False)  # Here, post is the data the user passes to update.
    db.commit()
    
    return post_query.first()