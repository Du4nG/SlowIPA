from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix = '/users',
    tags=['Users']
)


@router.get('/', response_model=List[schemas.UserOut])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**dict(user)) # unpack all parameters
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user doesn\'t exist')
    return user