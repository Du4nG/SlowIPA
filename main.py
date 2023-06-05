from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 
my_posts = [{'id':1,'title':'title of post 1', 'content':'content of post 1'}, 
            {'id':2,'title':'title of post 2', 'content':'content of post 2'}] 
    
    
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    
@app.get('/')
def root():
    return {'home'}

@app.get('/posts')
def get_post():
    return {'Posts': my_posts}

@app.post('/posts')
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,99)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/latest')
def get_latest_post():
    latest_post = my_posts[-1]
    return {'Latest': latest_post}

@app.get('/posts/{id}')
def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='not found')
    return {'post_detail': post}

    
    
