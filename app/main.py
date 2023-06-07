from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    
app.include_router(post.router)
app.include_router(user.router)    
    
@app.get('/')
def root():
    return {'home'}