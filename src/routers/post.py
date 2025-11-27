from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import get_db

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",  # Avoid to indicate the path operation root
    tags = ["Posts"]    # Create section in Swagger documentation
    )

@router.get("/", response_model=List[schemas.PostOut])   # Path operation
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str]=""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
            .group_by(models.Post.id) \
            .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()     # This version is to retrieve only own posts.
    return posts

@router.get("/{id}", response_model=schemas.PostOut)   # Path operation
def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
            .group_by(models.Post.id) \
            .filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
        
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform requested action")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)   # Path operation
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())   # The owner_id (from the model) is added here because this field is not requested to the user in the front-end
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)   # This is the whole query, not the post
    post_to_delete = post_query.first()
    
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
        
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
        
    post_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)   # Query.
    post_to_update = post_query.first()     # Find the post we want to update.
    
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
        
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
        
    post_query.update(**post.model_dump(),synchronize_session=False)  # Here, post is the data the user passes to update.
    db.commit()
    
    return post_query.first()