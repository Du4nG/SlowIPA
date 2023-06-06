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

@app.get('/sqlalchemy')
def test(db: Session = Depends(get_db)):
    return {'status}': 'success'}

@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published)
                   VALUES (%s, %s, %s) RETURNING *""", 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get('/posts/latest')
def get_latest_post():
    latest_post = my_posts[-1]
    return {'Latest': latest_post}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='not found')
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    return {status.HTTP_204_NO_CONTENT}

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET (title, content, published)
                   = (%s, %s, %s) WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
                    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    
    return {'updated_data': updated_post}
    