from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor

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
def get_post():
    return {'Posts': my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = dict(post)
    post_dict['id'] = randrange(0,99)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/latest')
def get_latest_post():
    latest_post = my_posts[-1]
    return {'Latest': latest_post}

@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='not found')
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    my_posts.pop(index)
    return {status.HTTP_204_NO_CONTENT}

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id doesn\'t exist')
    post_dict = dict(post)
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return {'data': post_dict}
    