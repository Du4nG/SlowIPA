from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapi',
                                port=5432,
                                user='postgres', password=1,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected!')
        break
    except Exception as error:
        print('Error:', error)
        time.sleep(2)
 
my_posts = [{'id':1,'title':'title of post 1', 'content':'content of post 1'}, 
            {'id':2,'title':'title of post 2', 'content':'content of post 2'}] 
    
    
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    
def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index
    
@app.get('/')
def root():
    return {'home'}


@app.get('/posts')
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    
    new_post = models.Post(**dict(post)) # unpack all parameters
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"new_post": new_post}


@app.get('/posts/latest')
def get_latest_post():
    latest_post = my_posts[-1]
    return {'Latest': latest_post}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='not found')
    return {'post_detail': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    post.delete(synchronize_session=False)
    db.commit()

@app.put('/posts/{id}')
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET (title, content, published)
    #                = (%s, %s, %s) WHERE id = %s RETURNING *""",
    # #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
                    
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post = query_post.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    query_post.update(dict(updated_post), synchronize_session=False)
    db.commit()
    return {'data':updated_post}