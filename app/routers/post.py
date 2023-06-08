from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = '/posts',
    tags=['Posts']
    
)

@router.get('/', response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    
    print(current_user.email)
    new_post = models.Post(**dict(post)) # unpack all parameters
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    post.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET (title, content, published)
    #                = (%s, %s, %s) WHERE id = %s RETURNING *""",
    # #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
                    
    query_post = db.query(models.Post).filter(models.Post.id==id)
    post = query_post.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    query_post.update(dict(updated_post), synchronize_session=False)
    db.commit()
    
    return post