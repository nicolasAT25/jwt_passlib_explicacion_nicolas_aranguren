# FastAPI
from fastapi import Response, status, HTTPException, Depends, APIRouter

 
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",  # Avoid to indicate the path operation root
    tags = ["Votos"]    # Create section in Swagger documentation
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post con ID {vote.post_id} no existe.')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) # Filters separated by ','
    found_vote = vote_query.first()
    
    if vote.vote_dir == True:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'Usuario {current_user.id} ya ha votado en el post {vote.post_id}.')
            
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Voto añadido con éxito!'}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El voto no existe.')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Voto eliminado con éxito.'}